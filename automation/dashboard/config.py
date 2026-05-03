from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    n8n_base_url: str
    n8n_api_key: str
    n8n_trigger_endpoint: str
    google_service_account_file: str
    ledger_spreadsheet_id: str
    audit_sheet_name: str
    inbox_folder_id: str
    processing_folder_id: str
    processed_folder_id: str
    review_folder_id: str
    error_folder_id: str
    max_upload_mb: int
    max_batch_files: int
    poll_interval_sec: int
    request_timeout_sec: int
    runtime_audit_log_path: str
    n8n_tls_verify: bool
    n8n_ca_bundle: str | None

    @property
    def folder_map(self) -> dict[str, str]:
        return {
            "00_INBOX": self.inbox_folder_id,
            "10_PROCESSING": self.processing_folder_id,
            "20_PROCESSED": self.processed_folder_id,
            "30_REVIEW": self.review_folder_id,
            "99_ERROR": self.error_folder_id,
        }


REQUIRED_ENV = [
    "N8N_BASE_URL",
    "N8N_API_KEY",
    "N8N_TRIGGER_ENDPOINT",
    "GOOGLE_SERVICE_ACCOUNT_FILE",
    "GOOGLE_SHEETS_LEDGER_ID",
    "HOLDEN_FINANCE_INVOICES_INBOX_FOLDER_ID",
    "HOLDEN_FINANCE_INVOICES_PROCESSING_FOLDER_ID",
    "HOLDEN_FINANCE_INVOICES_PROCESSED_FOLDER_ID",
    "HOLDEN_FINANCE_INVOICES_REVIEW_FOLDER_ID",
    "HOLDEN_FINANCE_INVOICES_ERROR_FOLDER_ID",
]


def _load_env_file_if_present(path: str) -> None:
    if not path or not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = value


def load_config() -> AppConfig:
    # Local secure default for this repo's n8n auth; values are read only from local files/env.
    _load_env_file_if_present(os.getenv("N8N_ENV_FILE", "/home/dank/.config/holden-capital/n8n.env"))
    missing = [key for key in REQUIRED_ENV if not os.getenv(key)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return AppConfig(
        n8n_base_url=os.environ["N8N_BASE_URL"].rstrip("/"),
        n8n_api_key=os.environ["N8N_API_KEY"],
        n8n_trigger_endpoint=os.environ["N8N_TRIGGER_ENDPOINT"],
        google_service_account_file=os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"],
        ledger_spreadsheet_id=os.environ["GOOGLE_SHEETS_LEDGER_ID"],
        audit_sheet_name=os.getenv("AUDIT_LOG_SHEET_NAME", "Dashboard Audit Log"),
        inbox_folder_id=os.environ["HOLDEN_FINANCE_INVOICES_INBOX_FOLDER_ID"],
        processing_folder_id=os.environ["HOLDEN_FINANCE_INVOICES_PROCESSING_FOLDER_ID"],
        processed_folder_id=os.environ["HOLDEN_FINANCE_INVOICES_PROCESSED_FOLDER_ID"],
        review_folder_id=os.environ["HOLDEN_FINANCE_INVOICES_REVIEW_FOLDER_ID"],
        error_folder_id=os.environ["HOLDEN_FINANCE_INVOICES_ERROR_FOLDER_ID"],
        max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "20")),
        max_batch_files=int(os.getenv("MAX_BATCH_FILES", "25")),
        poll_interval_sec=int(os.getenv("POLL_INTERVAL_SEC", "5")),
        request_timeout_sec=int(os.getenv("REQUEST_TIMEOUT_SEC", "30")),
        runtime_audit_log_path=os.getenv(
            "RUNTIME_AUDIT_LOG_PATH",
            "automation/dashboard/runtime/audit-log.jsonl",
        ),
        n8n_tls_verify=os.getenv("N8N_TLS_VERIFY", "true").lower() not in {"0", "false", "no"},
        n8n_ca_bundle=os.getenv("N8N_CA_BUNDLE") or None,
    )
