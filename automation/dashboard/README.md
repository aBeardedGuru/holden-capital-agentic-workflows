# Holden Finance Operator Dashboard v2

This is the only supported Streamlit dashboard implementation for operator control of finance intake workflows.

## Capabilities

- Upload files to Drive `00_INBOX`.
- Start manual batch processing via n8n webhook using selected Drive file IDs.
- Hard stop running n8n executions from the dashboard.
- Retry files in `30_REVIEW` and `99_ERROR`.
- Monitor recent execution status.
- Run diagnostics for n8n, Drive, and Sheets.
- Persist operator audit events to both Google Sheets and local JSONL.

## Environment

Copy `.env.example` to `.env` and populate values.

For this repo's secure local setup, the app will automatically load `N8N_BASE_URL` and `N8N_API_KEY` from:

`/home/dank/.config/holden-capital/n8n.env`

You can override with `N8N_ENV_FILE=/custom/path.env`.
Keep secrets in `.config` only; do not store them in tracked files.

In Docker, the compose file mounts `/home/dank/.config/holden-capital` to `/run/holden-config` (read-only). Use container paths in `.env`:

- `N8N_ENV_FILE=/run/holden-config/n8n.env`
- `GOOGLE_SERVICE_ACCOUNT_FILE=/run/holden-config/google-service-account.json`

If your n8n endpoint uses a private/self-signed CA, add the CA file under `.config` and set:

- `N8N_CA_BUNDLE=/run/holden-config/<ca-file>.pem`
- keep `N8N_TLS_VERIFY=true`

## Local Run

```bash
pip install -r automation/dashboard/requirements.txt
streamlit run automation/dashboard/app.py
```

## Container Run

```bash
cd automation/dashboard
cp .env.example .env
# Fill real values in .env

docker compose up --build
```

## Live Dev In Docker

The compose setup bind-mounts `automation/dashboard` into `/app` and runs Streamlit with polling watcher mode, so local file edits are reflected in the container automatically.

Start dev container with live updates:

```bash
cd automation/dashboard
docker compose up --build
```

After first build, run without rebuild:

```bash
cd automation/dashboard
docker compose up
```

When dependencies change (`requirements.txt`), rebuild image:

```bash
cd automation/dashboard
docker compose up --build
```

## Required Audit Sheet Headers

The `AUDIT_LOG_SHEET_NAME` tab must include this header row:

```text
event_id,event_type,operator_id,file_ids,execution_id,status,reason,timestamp,metadata
```

## Security

- Never commit secrets or service-account files.
- Keep runtime logs under `automation/dashboard/runtime/` only.
- Dashboard actions do not delete source documents.
