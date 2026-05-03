from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from clients.drive_client import DriveClient
from clients.google_client import build_credentials
from clients.n8n_client import N8nClient
from clients.sheets_client import SheetsClient
from config import load_config
from models.types import AuditEvent, TriggerRequest
from services.audit_service import AuditService
from services.intake_service import IntakeService

st.set_page_config(page_title="Holden Finance Intake Ops v2", layout="wide")


@st.cache_resource
def bootstrap():
    cfg = load_config()
    creds = build_credentials(cfg.google_service_account_file)

    drive = DriveClient(creds)
    sheets = SheetsClient(creds, cfg.ledger_spreadsheet_id)
    n8n = N8nClient(
        cfg.n8n_base_url,
        cfg.n8n_api_key,
        cfg.n8n_trigger_endpoint,
        timeout_seconds=cfg.request_timeout_sec,
        tls_verify=cfg.n8n_tls_verify,
        ca_bundle=cfg.n8n_ca_bundle,
    )
    intake = IntakeService(drive, n8n, cfg.max_upload_mb, cfg.max_batch_files)
    audit = AuditService(sheets, cfg.audit_sheet_name, cfg.runtime_audit_log_path)

    return cfg, drive, sheets, n8n, intake, audit


def _record(audit: AuditService, **kwargs):
    audit.record(AuditEvent(**kwargs))


def _execution_table(rows: list[dict]):
    if not rows:
        st.info("No executions found.")
        return
    formatted = []
    for row in rows:
        formatted.append(
            {
                "id": str(row.get("id") or row.get("executionId") or ""),
                "status": row.get("status") or row.get("finished") or "unknown",
                "startedAt": row.get("startedAt") or row.get("started_at") or "",
                "stoppedAt": row.get("stoppedAt") or row.get("stopped_at") or "",
                "mode": row.get("mode") or "",
            }
        )
    st.dataframe(formatted, use_container_width=True)


def run():
    try:
        cfg, drive, sheets, n8n, intake, audit = bootstrap()
    except Exception as exc:
        st.title("Holden Capital Finance Operator Dashboard v2")
        st.error("Startup failed: Google service account credentials are invalid or missing.")
        st.code(str(exc))
        st.markdown(
            "Remediation: replace `/home/dank/.config/holden-capital/google-service-account.json` "
            "with a real Google service account key JSON, then restart the container."
        )
        st.stop()

    st.title("Holden Capital Finance Operator Dashboard v2")
    st.caption("Drive-first intake, n8n run control, hard-stop, retry, and audit logging")

    tabs = st.tabs(["Inbox", "Run Control", "Execution Monitor", "Review/Retry", "Diagnostics", "Audit"])

    with tabs[0]:
        st.subheader("Upload to 00_INBOX")
        uploads = st.file_uploader(
            "Upload one or more finance documents",
            type=["pdf", "png", "jpg", "jpeg", "csv", "txt"],
            accept_multiple_files=True,
        )
        if st.button("Upload Files", type="primary"):
            if not uploads:
                st.warning("Select at least one file.")
            else:
                uploaded = intake.upload_files(cfg.inbox_folder_id, uploads)
                st.success(f"Uploaded {len(uploaded)} file(s) to inbox.")
                st.dataframe(uploaded, use_container_width=True)
                _record(
                    audit,
                    event_type="upload",
                    operator_id="internal_operator",
                    status="ok",
                    reason="dashboard_upload",
                    file_ids=[row.get("id", "") for row in uploaded],
                )

        st.markdown("### Current Inbox Files")
        st.dataframe(drive.list_folder_files(cfg.inbox_folder_id, page_size=200), use_container_width=True)

    with tabs[1]:
        st.subheader("Start / Stop")
        all_files = drive.list_folder_files(cfg.inbox_folder_id, page_size=200)
        options = {f"{item.get('name')} ({item.get('id')})": item.get("id") for item in all_files}
        selected_labels = st.multiselect("Select files to process", options=list(options.keys()))
        selected_ids = [options[label] for label in selected_labels]

        operator_id = st.text_input("Operator ID", value="internal_operator")
        reason = st.text_input("Reason", value="manual_batch_process")
        dry_run = st.checkbox("Dry run", value=False)

        if st.button("Start Batch", type="primary"):
            payload = TriggerRequest(
                file_ids=selected_ids,
                operator_id=operator_id,
                reason=reason,
                dry_run=dry_run,
            )
            result = intake.trigger(payload)
            execution_id = str(result.get("executionId") or result.get("id") or "")
            st.success("Triggered n8n workflow")
            st.json(result)
            _record(
                audit,
                event_type="start",
                operator_id=operator_id,
                status="ok",
                reason=reason,
                file_ids=selected_ids,
                execution_id=execution_id,
                metadata={"dry_run": dry_run},
            )

        st.markdown("### Hard Stop")
        running = n8n.list_executions(limit=30, status="running")
        run_options = {
            f"{row.get('id') or row.get('executionId')} | {row.get('startedAt') or row.get('started_at')}": str(
                row.get("id") or row.get("executionId")
            )
            for row in running
        }
        selected_run = st.selectbox("Running execution", options=[""] + list(run_options.keys()))
        if st.button("Stop Execution"):
            if not selected_run:
                st.warning("Select a running execution.")
            else:
                execution_id = run_options[selected_run]
                result = n8n.stop_execution(execution_id)
                st.success(f"Stop requested for execution {execution_id}")
                st.json(result)
                _record(
                    audit,
                    event_type="stop",
                    operator_id=operator_id,
                    status="ok",
                    reason="hard_terminate",
                    execution_id=execution_id,
                )

    with tabs[2]:
        st.subheader("Execution Monitor")
        status_filter = st.selectbox("Status", options=["all", "running", "success", "error", "canceled"])
        rows = n8n.list_executions(limit=50, status=None if status_filter == "all" else status_filter)
        _execution_table(rows)
        if st.button("Refresh Executions"):
            st.rerun()

    with tabs[3]:
        st.subheader("Retry Failed / Review")
        all_rows = drive.list_multi_folder({"30_REVIEW": cfg.review_folder_id, "99_ERROR": cfg.error_folder_id}, page_size=200)
        if not all_rows:
            st.info("No files in review/error folders")
        else:
            table = [
                {
                    "select": False,
                    "file_id": row.get("id"),
                    "file_name": row.get("name"),
                    "folder": row.get("dashboard_folder"),
                    "created": row.get("createdTime"),
                    "link": row.get("webViewLink"),
                }
                for row in all_rows
            ]
            edited = st.data_editor(
                table,
                hide_index=True,
                disabled=["file_id", "file_name", "folder", "created", "link"],
                use_container_width=True,
            )
            selected_ids = [row["file_id"] for row in edited if row.get("select")]
            retry_reason = st.text_input("Retry reason", value="manual_retry_from_dashboard")
            if st.button("Retry Selected"):
                result = intake.retry(selected_ids, operator_id="internal_operator", reason=retry_reason)
                execution_id = str(result.get("executionId") or result.get("id") or "")
                st.success(f"Retried {len(selected_ids)} file(s)")
                st.json(result)
                _record(
                    audit,
                    event_type="retry",
                    operator_id="internal_operator",
                    status="ok",
                    reason=retry_reason,
                    file_ids=selected_ids,
                    execution_id=execution_id,
                )

    with tabs[4]:
        st.subheader("Diagnostics")
        checks = []
        try:
            n8n.list_executions(limit=1)
            checks.append({"component": "n8n", "status": "ok", "detail": "reachable"})
        except Exception as exc:
            checks.append({"component": "n8n", "status": "error", "detail": str(exc)})

        try:
            drive.list_folder_files(cfg.inbox_folder_id, page_size=1)
            checks.append({"component": "drive", "status": "ok", "detail": "readable"})
        except Exception as exc:
            checks.append({"component": "drive", "status": "error", "detail": str(exc)})

        try:
            sheets.read_rows(cfg.audit_sheet_name, max_rows=2)
            checks.append({"component": "sheets", "status": "ok", "detail": "readable"})
        except Exception as exc:
            checks.append({"component": "sheets", "status": "error", "detail": str(exc)})

        st.dataframe(checks, use_container_width=True)

    with tabs[5]:
        st.subheader("Audit Events")
        rows = sheets.read_rows(cfg.audit_sheet_name, max_rows=250)
        st.dataframe(rows, use_container_width=True)
        st.caption(f"Local runtime log path: {cfg.runtime_audit_log_path}")
        st.caption(f"Last refresh: {datetime.now(timezone.utc).isoformat()}")
