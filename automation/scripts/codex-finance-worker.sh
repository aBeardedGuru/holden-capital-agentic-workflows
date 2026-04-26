#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AUTOMATION_DIR="${REPO_DIR}/automation"
RUNTIME_DIR="${REPO_DIR}/runtime/finance-document-intake"
INBOX_DIR="${RUNTIME_DIR}/inbox"
PROCESSING_DIR="${RUNTIME_DIR}/processing"
COMPLETE_DIR="${RUNTIME_DIR}/complete"
FAILED_DIR="${RUNTIME_DIR}/failed"
OUTPUT_DIR="${RUNTIME_DIR}/outputs"
PROMPT_FILE="${AUTOMATION_DIR}/prompts/extract-finance-document.md"

usage() {
  printf 'Usage: %s [--once] [--job path/to/job.json]\n' "$0"
}

ensure_dirs() {
  mkdir -p "$INBOX_DIR" "$PROCESSING_DIR" "$COMPLETE_DIR" "$FAILED_DIR" "$OUTPUT_DIR"
}

json_get() {
  local file="$1"
  local key="$2"
  python3 - "$file" "$key" <<'PY'
import json
import sys

path, key = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
value = data
for part in key.split("."):
    value = value[part]
print(value)
PY
}

validate_json() {
  local file="$1"
  python3 -m json.tool "$file" >/dev/null
}

timestamp_utc() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

update_job_processing() {
  local file="$1"
  local status="$2"
  local started_at="${3:-}"
  local completed_at="${4:-}"

  python3 - "$file" "$status" "$started_at" "$completed_at" <<'PY'
import json
import sys

path, status, started_at, completed_at = sys.argv[1:5]
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

processing = data.setdefault("processing", {})
processing["status"] = status

if started_at:
    processing["processing_started_at"] = started_at
if completed_at:
    processing["processing_completed_at"] = completed_at

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, sort_keys=True)
    f.write("\n")
PY
}

write_failure_output() {
  local job_file="$1"
  local output_path="$2"
  local reason_code="$3"
  local reason_text="$4"
  local processed_at="$5"

  python3 - "$job_file" "$output_path" "$reason_code" "$reason_text" "$processed_at" <<'PY'
import json
import sys

job_path, output_path, reason_code, reason_text, processed_at = sys.argv[1:6]
with open(job_path, "r", encoding="utf-8") as f:
    job = json.load(f)

result = {
    "schema_version": "1.1",
    "job_id": job["job_id"],
    "flow_name": job["flow_name"],
    "status": "failed",
    "source": {
        "system": job["source"]["system"],
        "drive_file_id": job["source"]["drive_file_id"],
        "drive_file_name": job["source"]["drive_file_name"],
        "drive_file_url": job["source"]["drive_file_url"],
        "mime_type": job["source"]["mime_type"],
    },
    "document_type": "unknown",
    "vendor_or_payee": None,
    "document_date": None,
    "amount": None,
    "currency": None,
    "payment_method": None,
    "account_last4": None,
    "invoice_number": None,
    "due_date": None,
    "confidence": 0,
    "suggested_category": None,
    "suggested_property_or_entity": None,
    "summary": "Document processing failed before extraction completed.",
    "review": {
        "queue_entry_required": True,
        "reason": reason_text,
        "recommended_action": "Inspect the failed job, correct the source issue, and rerun.",
        "status": "pending",
        "resolution_notes": None,
    },
    "duplicate_check": {
        "idempotency_key": job["processing"]["idempotency_key"],
        "is_duplicate": False,
        "duplicate_reason": None,
        "duplicate_of_job_id": None,
    },
    "audit": {
        "processed_at": processed_at,
        "output_path": output_path,
        "final_status": "failed",
        "failure_reason_code": reason_code,
        "failure_reason": reason_text,
        "reviewer": None,
        "reviewed_at": None,
        "original_value": None,
        "corrected_value": None,
        "correction_reason": None,
    },
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, sort_keys=True)
    f.write("\n")
PY
}

pick_job() {
  find "$INBOX_DIR" -maxdepth 1 -type f -name '*.json' -print | sort | head -n 1
}

run_job() {
  local source_job="$1"
  local base_name
  local processing_job
  local job_id
  local text_path
  local requested_output_path
  local failure_output_path
  local output_path
  local tmp_prompt
  local tmp_output
  local started_at
  local completed_at

  base_name="$(basename "$source_job")"
  processing_job="${PROCESSING_DIR}/${base_name}"

  mv "$source_job" "$processing_job"

  job_id="$(json_get "$processing_job" "job_id")"
  text_path="$(json_get "$processing_job" "paths.extracted_text_path")"
  requested_output_path="$(json_get "$processing_job" "paths.output_path")"
  failure_output_path="$(json_get "$processing_job" "paths.failure_output_path")"
  output_path="${requested_output_path:-${OUTPUT_DIR}/${job_id}.json}"
  mkdir -p "$(dirname "$output_path")"
  mkdir -p "$(dirname "$failure_output_path")"

  started_at="$(timestamp_utc)"
  update_job_processing "$processing_job" "processing" "$started_at" ""

  if [[ "$text_path" == "None" || ! -f "$text_path" ]]; then
    printf 'Extracted text file not found: %s\n' "$text_path" >&2
    completed_at="$(timestamp_utc)"
    write_failure_output "$processing_job" "$failure_output_path" "missing_extracted_text" "Extracted text file not found at the expected path." "$completed_at"
    validate_json "$failure_output_path"
    update_job_processing "$processing_job" "failed" "$started_at" "$completed_at"
    mv "$processing_job" "${FAILED_DIR}/${base_name}"
    return 1
  fi

  tmp_prompt="$(mktemp)"
  tmp_output="$(mktemp)"

  {
    cat "$PROMPT_FILE"
    printf '\n\n## Job JSON\n\n'
    cat "$processing_job"
    printf '\n\n## Extracted Document Text\n\n'
    cat "$text_path"
  } > "$tmp_prompt"

  if ! codex exec \
    --skip-git-repo-check \
    --ephemeral \
    --sandbox read-only \
    -C "$REPO_DIR" \
    --output-schema "${AUTOMATION_DIR}/schemas/finance-extraction.schema.json" \
    --output-last-message "$tmp_output" \
    "$(cat "$tmp_prompt")" >/dev/null; then
    printf 'Codex execution failed for job: %s\n' "$job_id" >&2
    completed_at="$(timestamp_utc)"
    write_failure_output "$processing_job" "$failure_output_path" "codex_exec_failed" "Codex CLI execution failed before a valid extraction was returned." "$completed_at"
    validate_json "$failure_output_path"
    rm -f "$tmp_prompt" "$tmp_output"
    update_job_processing "$processing_job" "failed" "$started_at" "$completed_at"
    mv "$processing_job" "${FAILED_DIR}/${base_name}"
    return 1
  fi

  python3 - "$tmp_output" "$output_path" "$processing_job" "$(timestamp_utc)" <<'PY'
import json
import sys

raw_path, output_path, job_path, processed_at = sys.argv[1:5]
raw = open(raw_path, "r", encoding="utf-8").read().strip()
job = json.load(open(job_path, "r", encoding="utf-8"))

if raw.startswith("```"):
    lines = raw.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    raw = "\n".join(lines).strip()

data = json.loads(raw)
data["schema_version"] = "1.1"
data["job_id"] = job["job_id"]
data["flow_name"] = job["flow_name"]
data["source"] = {
    "system": job["source"]["system"],
    "drive_file_id": job["source"]["drive_file_id"],
    "drive_file_name": job["source"]["drive_file_name"],
    "drive_file_url": job["source"]["drive_file_url"],
    "mime_type": job["source"]["mime_type"],
}

duplicate_check = data.setdefault("duplicate_check", {})
duplicate_check["idempotency_key"] = job["processing"]["idempotency_key"]
duplicate_check.setdefault("is_duplicate", False)
duplicate_check.setdefault("duplicate_reason", None)
duplicate_check.setdefault("duplicate_of_job_id", None)

review = data.setdefault("review", {})
review.setdefault("queue_entry_required", data.get("status") in {"needs_review", "failed"})
review.setdefault("reason", None)
review.setdefault("recommended_action", None)
review.setdefault("status", "pending" if review["queue_entry_required"] else "not_needed")
review.setdefault("resolution_notes", None)

audit = data.setdefault("audit", {})
audit["processed_at"] = processed_at
audit["output_path"] = output_path
audit["final_status"] = data["status"]
audit.setdefault("failure_reason_code", None)
audit.setdefault("failure_reason", None)
audit.setdefault("reviewer", None)
audit.setdefault("reviewed_at", None)
audit.setdefault("original_value", None)
audit.setdefault("corrected_value", None)
audit.setdefault("correction_reason", None)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, sort_keys=True)
    f.write("\n")
PY

  validate_json "$output_path"
  completed_at="$(timestamp_utc)"
  rm -f "$tmp_prompt" "$tmp_output"
  update_job_processing "$processing_job" "complete" "$started_at" "$completed_at"
  mv "$processing_job" "${COMPLETE_DIR}/${base_name}"
  printf '%s\n' "$output_path"
}

main() {
  local mode="once"
  local explicit_job=""
  local job=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --once)
        mode="once"
        shift
        ;;
      --job)
        explicit_job="${2:-}"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        usage >&2
        exit 2
        ;;
    esac
  done

  ensure_dirs

  if [[ -n "$explicit_job" ]]; then
    job="$explicit_job"
  else
    job="$(pick_job || true)"
  fi

  if [[ -z "$job" ]]; then
    printf 'No finance document jobs found in %s\n' "$INBOX_DIR"
    exit 0
  fi

  run_job "$job"

  if [[ "$mode" != "once" ]]; then
    printf 'Only --once mode is currently implemented.\n' >&2
    exit 2
  fi
}

main "$@"
