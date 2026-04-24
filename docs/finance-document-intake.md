# Finance Document Intake

This project contains the n8n/Codex bridge for finance document automation.

Goal:

1. Put receipts, invoices, statements, and finance documents in Google Drive.
2. Let n8n create a local job packet.
3. Let Codex CLI classify and extract structured data without OpenAI API billing.
4. Let n8n validate the JSON, update Google Sheets, and move the Drive file.

## Architecture

```text
Google Drive 00_Inbox
  -> n8n Google Drive node
  -> local job JSON + extracted text
  -> scripts/codex-finance-worker.sh
  -> Codex CLI
  -> JSON result
  -> n8n Google Sheets node
  -> Google Drive processed/review/error folder
```

Codex is used through the local CLI session. n8n does not store ChatGPT credentials and does not use the OpenAI API.

## Required n8n Credentials

Existing credentials on the server:

```text
Google Drive account
Google Sheets account
```

No OpenAI API credential is required for this design.

## Required Google Drive Folders

Create these folders and record their IDs in the n8n workflow config node:

```text
Holden Finance Automation/
  00_Inbox/
  10_Processed/
    Receipts/
    Invoices/
    Bank Statements/
    Credit Card Statements/
    Tax Documents/
    Insurance/
    Loan Documents/
    Utilities/
    Payroll/
    Income/
    Unknown/
  90_Needs Review/
  99_Errors/
```

## Required Google Sheet

Create a spreadsheet named `Holden Finance Ledger` with these tabs:

```text
Transactions
Documents
Review Queue
Run Log
```

### Transactions Columns

```text
processed_at
document_date
vendor_or_payee
document_type
category
property_or_entity
amount
currency
payment_method
account_last4
invoice_number
due_date
tax_relevant
confidence
summary
drive_file_id
drive_file_url
source_file_name
status
review_reason
```

### Documents Columns

```text
processed_at
job_id
drive_file_id
drive_file_url
source_file_name
mime_type
document_type
classification_confidence
codex_output_path
raw_extraction_json
```

### Review Queue Columns

```text
created_at
job_id
drive_file_id
drive_file_url
source_file_name
reason
suggested_document_type
suggested_amount
suggested_vendor
confidence
status
```

### Run Log Columns

```text
run_at
status
files_seen
jobs_created
jobs_completed
jobs_needing_review
jobs_failed
notes
```

## Local Worker Directories

The worker script creates these directories under `runtime/finance-document-intake/`:

```text
inbox/
processing/
complete/
failed/
outputs/
```

Files in `runtime/` are operational data and should not be committed.

## Job Contract

n8n writes one JSON job file per document:

```text
runtime/finance-document-intake/inbox/<job_id>.json
```

The job must match `schemas/finance-job.schema.json`.

Codex writes:

```text
runtime/finance-document-intake/outputs/<job_id>.json
```

The output must match `schemas/finance-extraction.schema.json`.

## First Manual Test

1. Place one receipt PDF or text-extracted sample in the job inbox.
2. Run:

```bash
scripts/codex-finance-worker.sh --once
```

3. Confirm output exists:

```bash
ls runtime/finance-document-intake/outputs/
```

4. Validate the output:

```bash
python3 -m json.tool runtime/finance-document-intake/outputs/<job_id>.json >/dev/null
```

5. Import or recreate `workflows/finance-document-intake-codex-assisted.blueprint.json` in n8n and wire the folder/sheet IDs.

## Safety Rules

- Do not put bank login credentials in job JSON.
- Do not store full account numbers. Last four digits only.
- Do not delete source documents.
- Keep n8n responsible for Drive and Sheets changes.
- Keep Codex responsible only for classification and extraction JSON.
