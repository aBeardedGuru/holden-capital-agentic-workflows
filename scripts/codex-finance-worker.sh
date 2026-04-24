#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="${ROOT_DIR}/runtime/finance-document-intake"
INBOX_DIR="${RUNTIME_DIR}/inbox"
PROCESSING_DIR="${RUNTIME_DIR}/processing"
COMPLETE_DIR="${RUNTIME_DIR}/complete"
FAILED_DIR="${RUNTIME_DIR}/failed"
OUTPUT_DIR="${RUNTIME_DIR}/outputs"
PROMPT_FILE="${ROOT_DIR}/prompts/extract-finance-document.md"

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
  local output_path
  local tmp_prompt
  local tmp_output

  base_name="$(basename "$source_job")"
  processing_job="${PROCESSING_DIR}/${base_name}"

  mv "$source_job" "$processing_job"

  job_id="$(json_get "$processing_job" "job_id")"
  text_path="$(json_get "$processing_job" "extracted_text_path")"
  requested_output_path="$(json_get "$processing_job" "output_path")"
  output_path="${requested_output_path:-${OUTPUT_DIR}/${job_id}.json}"
  mkdir -p "$(dirname "$output_path")"

  if [[ ! -f "$text_path" ]]; then
    printf 'Extracted text file not found: %s\n' "$text_path" >&2
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
    -C "$ROOT_DIR" \
    --output-schema "${ROOT_DIR}/schemas/finance-extraction.schema.json" \
    --output-last-message "$tmp_output" \
    "$(cat "$tmp_prompt")" >/dev/null; then
    printf 'Codex execution failed for job: %s\n' "$job_id" >&2
    rm -f "$tmp_prompt" "$tmp_output"
    mv "$processing_job" "${FAILED_DIR}/${base_name}"
    return 1
  fi

  python3 - "$tmp_output" "$output_path" <<'PY'
import json
import sys

raw_path, output_path = sys.argv[1], sys.argv[2]
raw = open(raw_path, "r", encoding="utf-8").read().strip()

if raw.startswith("```"):
    lines = raw.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    raw = "\n".join(lines).strip()

data = json.loads(raw)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, sort_keys=True)
    f.write("\n")
PY

  validate_json "$output_path"
  rm -f "$tmp_prompt" "$tmp_output"
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
