# Finance Document Intake

## Purpose

Define the contract and runtime flow for Google Drive based finance document intake, OpenRouter-powered extraction in n8n, Google Sheets updates, review routing, and audit-safe file handling.

Use this document with the detailed operating contract in [finance-ledger-operating-contract.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/finance-ledger-operating-contract.md).

## Flow Summary

```text
Google Drive Holden Capital/Finance Automation/00_INBOX
  -> n8n lists and downloads source files
  -> n8n sends bounded payloads to an OpenRouter model node
  -> model response is parsed and normalized to strict extraction JSON
  -> n8n validates output and updates Google Sheets
  -> n8n moves the Drive file to processed, review, or error
```

Current live variant for simple personal-drive triage:

```text
Google Drive Holden Capital/Finance Automation/00_INBOX
  -> n8n lists all files in 00_INBOX
  -> n8n downloads and extracts text
  -> AI Intake Classifier node (prompt-driven) classifies each document type
  -> only document_type=invoice rows are appended to the Expenses sheet
  -> files are moved to 10_DONE_INVOICES, 20_DONE_BANK_STATEMENTS, 30_DONE_OTHER, 90_REVIEW, or 99_ERROR
```

Workflow artifact for this variant:

- [automation/workflows/google-drive-download-for-processing.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/workflows/google-drive-download-for-processing.json)

Design constraints:

- Google Drive is the intake and filing surface.
- Google Sheets is the first ledger, review queue, and run log surface.
- OpenRouter-backed model inference runs in n8n using model-specific credentials.
- Source documents are never deleted.
- Runtime operational data stays under `runtime/` and is never committed.

## Required Google Integrations

Required n8n credentials:

```text
Google Drive account
Google Sheets account
OpenRouter API credential
```

## Contract References

- Operating contract: [finance-ledger-operating-contract.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/finance-ledger-operating-contract.md)
- Job schema: [automation/schemas/finance-job.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/finance-job.schema.json)
- Extraction schema: [automation/schemas/finance-extraction.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/finance-extraction.schema.json)
- Primary n8n workflow: [automation/workflows/google-drive-download-for-processing.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/workflows/google-drive-download-for-processing.json)

## Required Drive And Sheet Setup

Before activation:

1. Create the simple Drive folder tree used by the live workflow:

```text
Holden Capital/
  Finance Automation/
    00_INBOX/
    10_DONE_INVOICES/
    20_DONE_BANK_STATEMENTS/
    30_DONE_OTHER/
    90_REVIEW/
    99_ERROR/
```

2. Create the `Holden Finance Ledger` spreadsheet with `Transactions`, `Documents`, `Review Queue`, and `Run Log` tabs.
3. Record only placeholder IDs in workflow config nodes or environment-local config.
4. Do not store credentials, live folder IDs tied to secrets workflows, or full account numbers in tracked files.

## Job Lifecycle

1. n8n detects a file in the Drive inbox.
2. n8n downloads the source file and prepares bounded classifier input.
3. n8n calls an OpenRouter model node with strict JSON response instructions.
4. n8n parses and normalizes model output against extraction contracts.
5. n8n writes rows and logs:
   - appends `Transactions` and `Documents` rows
   - appends a `Review Queue` row when `review.queue_entry_required` is true
   - appends a `Run Log` row for batch visibility
   - moves the Drive file to the correct processed, review, or error folder

## Model Behavior

The OpenRouter classifier step runs in n8n and must:

- accept bounded file content and metadata from upstream nodes
- enforce strict JSON schema-compatible output formatting
- write JSON output that matches the extraction schema
- on failure, emit a machine-readable failure reason and route the file to `99_ERROR`
- never delete the original source document

## Review Queue Rules

Create a `Review Queue` row when any of these are true:

- confidence is below the chosen review threshold
- required fields are missing
- the document is ambiguous
- the job failed
- duplicate handling needs a human decision

Required review statuses:

- `pending`
- `approved`
- `corrected`
- `rejected`
- `needs_more_info`

When a human corrects a value, preserve the original suggested value, corrected value, reviewer, timestamp, and reason in the audit trail.

## Duplicate And Audit Rules

Every processed item must be traceable through:

- `flow_name`
- `job_id`
- source ID or path
- source URL when available
- idempotency key
- output JSON path
- processing timestamp
- final status

Duplicate decisions must record:

- whether the item is a duplicate
- idempotency key
- duplicate reason
- prior job reference when known

## Safety Rules

- Do not store bank login credentials, API keys, or n8n credentials in job packets, prompts, schemas, samples, or workflows.
- Do not store full account numbers anywhere in the contract chain.
- Keep only `account_last4` when account metadata is needed.
- Keep production posting and external reminders out of this flow.
- Keep n8n responsible for Drive and Sheets side effects.
- Keep OpenRouter model nodes responsible for structured extraction only.

## Manual Validation

1. Upload one sample finance document to `00_INBOX`.
2. Run one manual execution of `google-drive-download-for-processing.json` in n8n.
3. Confirm classifier output is valid strict JSON and mapped to sheet rows.
4. Confirm expected rows are created in `Transactions`, `Documents`, and optionally `Review Queue`.
5. Confirm `Run Log` captures counts and error reasons when applicable.

### One-file ingest smoke test

1. Upload one invoice PDF into `00_INBOX`.
2. Run one manual execution of the workflow in n8n.
3. Confirm one expense row was appended in the configured `Expenses` sheet tab.
4. Confirm the source file moved from `00_INBOX` to `10_DONE_INVOICES`.
5. Repeat with a bank statement and confirm move to `20_DONE_BANK_STATEMENTS` without an expense-sheet append.
