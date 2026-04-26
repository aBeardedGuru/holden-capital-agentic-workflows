# Finance Ledger And Drive Operating Contract

## Purpose

Define the stable Google Drive, Google Sheets, runtime, review, and audit contract for the finance document intake foundation.

Use this contract before enabling or changing any finance automation workflow in this repo.

## Linked Flow

- Primary flow doc: [finance-document-intake.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/finance-document-intake.md)
- Epic source: [epic-1-finance-intake-and-review-foundation.md](/home/dank/Projects/holden-capital-agentic-workflows/planning/epics/epic-1-finance-intake-and-review-foundation.md)

## Safety And Privacy Rules

- Source documents are never deleted by automation.
- Runtime files under `runtime/` are local operational data and must not be committed.
- Job packets, samples, prompts, schemas, and workflows must not store bank credentials, Google credentials, API keys, or n8n credentials.
- Full account or card numbers must not be stored in repo files, runtime job JSON, extraction output JSON, or Google Sheets tabs.
- If account metadata is needed, only `account_last4` is allowed.
- Automation may prepare draft rows and review items, but it must not silently post into accounting software or send reminders without explicit approval.

## Google Drive Contract

Create one root folder and record the placeholder IDs in workflow config, not in tracked secrets files.

```text
Holden Finance Automation/
  00_INBOX/
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

### Required Drive Placeholders

- `HOLDEN_FINANCE_ROOT_FOLDER_ID`
- `HOLDEN_FINANCE_INBOX_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_RECEIPTS_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_INVOICES_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_BANK_STATEMENTS_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_CREDIT_CARD_STATEMENTS_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_TAX_DOCUMENTS_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_INSURANCE_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_LOAN_DOCUMENTS_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_UTILITIES_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_PAYROLL_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_INCOME_FOLDER_ID`
- `HOLDEN_FINANCE_PROCESSED_UNKNOWN_FOLDER_ID`
- `HOLDEN_FINANCE_REVIEW_FOLDER_ID`
- `HOLDEN_FINANCE_ERROR_FOLDER_ID`

## Google Sheets Contract

Create one spreadsheet named `Holden Finance Ledger`.

Store only the spreadsheet ID placeholder in workflow config:

- `HOLDEN_FINANCE_LEDGER_SPREADSHEET_ID`

Required tabs:

- `Transactions`
- `Documents`
- `Review Queue`
- `Run Log`

### Transactions Tab

Purpose: draft transaction-level extraction results for operator or bookkeeper review.

Required columns:

| Column | Purpose |
| --- | --- |
| `processed_at` | Processing completion timestamp. |
| `flow_name` | Source workflow name, initially `finance_document_intake`. |
| `job_id` | Job packet identifier. |
| `idempotency_key` | Duplicate detection key used for this source. |
| `document_date` | Extracted transaction or document date. |
| `vendor_or_payee` | Extracted vendor or payee name. |
| `document_type` | Receipt, invoice, statement, or other finance document type. |
| `suggested_category` | Suggested bookkeeping category from extraction. |
| `suggested_property_or_entity` | Suggested property or entity from extraction. |
| `amount` | Extracted amount. |
| `currency` | Extracted currency. |
| `payment_method` | Optional payment descriptor. |
| `account_last4` | Last four digits only when visible and needed. |
| `invoice_number` | Invoice or statement reference when present. |
| `due_date` | Due date for invoices or similar documents. |
| `confidence` | Overall extraction confidence. |
| `summary` | Short factual summary. |
| `status` | `processed`, `needs_review`, `duplicate`, or `failed`. |
| `review_reason` | Blocking or escalation reason when review is needed. |
| `recommended_action` | Operator action suggested by extraction or routing. |
| `approval_status` | Human decision state when later reviewed. |
| `approved_by` | Reviewer identity when human approval occurs. |
| `approved_at` | Approval timestamp when human approval occurs. |
| `drive_file_id` | Google Drive file ID. |
| `drive_file_url` | Google Drive file URL. |
| `source_file_name` | Original source file name. |
| `output_json_path` | Local output JSON path. |

### Documents Tab

Purpose: one row per processed source document for auditability and reruns.

Required columns:

| Column | Purpose |
| --- | --- |
| `processed_at` | Processing completion timestamp. |
| `flow_name` | Source workflow name. |
| `job_id` | Job packet identifier. |
| `idempotency_key` | Duplicate detection key. |
| `drive_file_id` | Google Drive file ID. |
| `drive_file_url` | Google Drive file URL. |
| `source_file_name` | Original file name. |
| `mime_type` | Source MIME type. |
| `document_type` | Extracted document type. |
| `classification_confidence` | Overall classification confidence. |
| `status` | Final workflow status. |
| `review_queue_status` | `not_needed`, `pending`, `approved`, `corrected`, `rejected`, or `needs_more_info`. |
| `review_reason` | Review reason when applicable. |
| `duplicate_detected` | Duplicate flag. |
| `duplicate_reason` | Duplicate decision reason when applicable. |
| `duplicate_of_job_id` | Earlier job that won duplicate resolution when applicable. |
| `model_output_path` | JSON output path captured from n8n model-processing nodes. |
| `raw_extraction_json` | Serialized JSON or reference to stored output. |
| `failure_reason_code` | Machine-readable failure code when status is `failed`. |
| `failure_reason` | Human-readable failure reason when status is `failed`. |

### Review Queue Tab

Purpose: one shared queue for unresolved finance items from any flow.

Required columns:

| Column | Purpose |
| --- | --- |
| `created_at` | Review item creation timestamp. |
| `flow_name` | Source workflow name. |
| `job_id` | Job packet identifier. |
| `source_reference` | Drive file ID or other source identifier. |
| `drive_file_url` | Source URL when available. |
| `source_file_name` | Original file name. |
| `reason` | Why the item requires human review. |
| `suggested_document_type` | Extracted or inferred document type. |
| `suggested_vendor` | Extracted vendor or payee. |
| `suggested_amount` | Extracted amount. |
| `suggested_category` | Suggested bookkeeping category. |
| `suggested_property_or_entity` | Suggested property or entity. |
| `confidence` | Overall extraction confidence. |
| `recommended_action` | Suggested next operator action. |
| `status` | `pending`, `approved`, `corrected`, `rejected`, or `needs_more_info`. |
| `resolution_notes` | Human decision notes. |
| `reviewed_by` | Reviewer identity. |
| `reviewed_at` | Review completion timestamp. |

### Run Log Tab

Purpose: batch-level run visibility and troubleshooting.

Required columns:

| Column | Purpose |
| --- | --- |
| `run_at` | Workflow run timestamp. |
| `flow_name` | Name of the flow that ran. |
| `status` | Run status. |
| `files_seen` | Count of source files seen. |
| `jobs_created` | Count of jobs created. |
| `jobs_completed` | Count of completed jobs. |
| `jobs_needing_review` | Count of review-routed jobs. |
| `jobs_failed` | Count of failed jobs. |
| `duplicates_detected` | Count of duplicate decisions. |
| `validation_errors` | Validation or schema errors observed. |
| `notes` | Short run summary. |

## Runtime Contract

Base runtime path:

```text
runtime/finance-document-intake/
```

Required directories:

```text
inbox/
processing/
complete/
failed/
outputs/
```

Behavior:

- `inbox/` holds queued job packets when file-based runtime staging is enabled.
- `processing/` holds the job packet currently being worked when file-based staging is enabled.
- `complete/` holds the processed job packet after a valid output is written when file-based staging is enabled.
- `failed/` holds the processed job packet after a terminal error when file-based staging is enabled.
- `outputs/` holds the machine-readable extraction result or failure result for each job.

## Job Packet Contract

The queueing workflow must write one job packet per source document to:

```text
runtime/finance-document-intake/inbox/<job_id>.json
```

The job packet must validate against:

- [automation/schemas/finance-job.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/finance-job.schema.json)

The packet must include:

- `job_id`
- `flow_name`
- Google Drive file metadata
- Drive file ID and URL
- MIME type
- source file path when locally staged
- extracted text path when available
- output and failure output paths
- idempotency key
- queue and processing timestamps

## Extraction Output Contract

The n8n extraction/classification path must write one output file to:

```text
runtime/finance-document-intake/outputs/<job_id>.json
```

The output must validate against:

- [automation/schemas/finance-extraction.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/finance-extraction.schema.json)

The output must include:

- `document_type`
- `vendor_or_payee`
- `document_date`
- `amount`
- `currency`
- `confidence`
- `suggested_category`
- `suggested_property_or_entity`
- `status`
- `review.reason` when review is needed
- duplicate decision details
- audit details including final status and output path

## Review Queue Lifecycle

Entry rule:

- Any flow that cannot confidently classify or safely advance an item must create a `Review Queue` row.

Required lifecycle states:

- `pending`
- `approved`
- `corrected`
- `rejected`
- `needs_more_info`

Required behaviors:

- `approved` means the item can later be promoted from draft to production action without reclassifying the original source.
- `corrected` means a human changed one or more suggested values.
- `rejected` means the draft result should not be used.
- `needs_more_info` means the source or metadata is still insufficient.

Required resolution capture:

- original suggested value when corrected
- new approved value when corrected
- reviewer identity
- review timestamp
- resolution notes

## Audit And Duplicate Logging

Every processed source must preserve a traceable record with:

- source ID or source path
- source URL when available
- flow name
- idempotency key
- processing timestamp
- confidence
- output JSON path
- final status

Duplicate decisions must capture:

- whether the item is a duplicate
- the idempotency key used
- the duplicate reason
- the winning prior job or source reference when known

Human corrections must capture:

- original value
- corrected value
- reviewer
- timestamp
- reason
