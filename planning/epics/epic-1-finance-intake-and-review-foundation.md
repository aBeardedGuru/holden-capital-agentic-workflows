# Epic 1: Finance Intake And Review Foundation

Enable the operator to capture finance documents, run local extraction, update Google Sheets, route files, and manage one review queue with audit trail.

## Implementation Status

Status date: 2026-04-26

- Story 1.1: complete in `docs/finance-ledger-operating-contract.md` and `docs/finance-document-intake.md`.
- Story 1.2: complete in `automation/schemas/finance-job.schema.json`, `automation/schemas/finance-extraction.schema.json`, and aligned samples.
- Story 1.3: complete in `automation/scripts/codex-finance-worker.sh` and runtime directory contract docs.
- Story 1.4: contract complete in docs and schema fields; workflow blueprints include review-queue integration notes.
- Story 1.5: complete in extraction schema and docs with duplicate and audit fields.

Conformance note:
- The live n8n workflow `Google Drive INGEST Classification + Expense Sheet` was refactored to emit v1.1 job packets and invoice-only expense-sheet writes.
- The repo workflow artifact `automation/workflows/google-drive-download-for-processing.json` was refactored to the same v1.1 contract and placeholder-safe credential references.

## Story 1.1: Define Finance Ledger And Drive Operating Contract

As a Holden Capital operator,
I want a documented Google Drive and Google Sheets operating contract,
So that finance automation has a stable intake, ledger, and review surface before workflow implementation.

**Acceptance Criteria:**

**Given** the finance document intake requirements
**When** the operating contract is documented
**Then** it specifies the required Drive folder tree for inbox, processed, review, and error states
**And** it specifies the required Google Sheet tabs and columns for `Transactions`, `Documents`, `Review Queue`, and `Run Log`.

**Given** the MVP safety requirements
**When** the operating contract is documented
**Then** it states that source documents are never deleted
**And** it states that full account numbers, bank credentials, API keys, and n8n credentials must not be stored in job JSON or repo files.

**Given** future implementation agents need setup context
**When** the story is complete
**Then** the contract is linked from the finance automation docs
**And** it includes placeholders for Drive folder IDs and Google Sheet ID without storing secrets.

## Story 1.2: Define Job Packet And Extraction Output Schemas

As a workflow implementer,
I want explicit job and extraction schemas,
So that n8n and Codex exchange predictable finance data.

**Acceptance Criteria:**

**Given** n8n creates a document-processing job
**When** the job JSON is validated
**Then** it conforms to `automation/schemas/finance-job.schema.json`
**And** it includes job ID, Drive file metadata, source file path or ID, MIME type, extracted text path when available, and processing timestamps.

**Given** Codex completes classification/extraction
**When** output JSON is validated
**Then** it conforms to `automation/schemas/finance-extraction.schema.json`
**And** it includes document type, vendor/payee, date, amount, currency, confidence, suggested category, suggested property/entity, status, and review reason when applicable.

**Given** privacy requirements apply
**When** schemas are reviewed
**Then** they reject full account numbers
**And** allow only account last four digits when account metadata is needed.

## Story 1.3: Document Local Codex Worker Runtime Contract

As a workflow operator,
I want a local worker contract for Codex-assisted extraction,
So that document processing can run without OpenAI API billing or credential storage in n8n.

**Acceptance Criteria:**

**Given** a job JSON file exists in `runtime/finance-document-intake/inbox/`
**When** the local worker runs once
**Then** it reads the job packet, invokes local Codex CLI according to the contract, and writes output JSON to `runtime/finance-document-intake/outputs/`.

**Given** runtime data is operational data
**When** the worker contract is documented
**Then** it defines `inbox`, `processing`, `complete`, `failed`, and `outputs` directories
**And** it states runtime files must not be committed.

**Given** a worker failure occurs
**When** the job cannot be completed
**Then** the contract defines how the job moves to failed state with a machine-readable reason.

## Story 1.4: Define Review Queue Lifecycle

As a Holden Capital operator,
I want one review queue for unresolved finance items,
So that uncertain expenses, invoices, and reports do not disappear into separate workflows.

**Acceptance Criteria:**

**Given** any flow cannot confidently classify an item
**When** the flow completes
**Then** it writes a row to the `Review Queue` tab with flow name, source reference, reason, suggested values, confidence, status, and recommended action.

**Given** a review queue row exists
**When** the operator reviews it
**Then** status can be updated to approved, corrected, rejected, or needs more info
**And** the resolution notes can capture the reason for the decision.

**Given** a review item is approved
**When** production actions are later enabled
**Then** the approved item can be promoted from draft to action without reclassifying the original source document.

## Story 1.5: Define Shared Audit And Duplicate Decision Logging

As a bookkeeper or operator,
I want every finance automation decision to be traceable,
So that I can explain where each row, exception, or skipped duplicate came from.

**Acceptance Criteria:**

**Given** a document or source record is processed
**When** processing completes
**Then** the system records source ID or path, source URL when available, processing timestamp, confidence, output JSON location, final status, and flow name.

**Given** a duplicate source record is detected
**When** the item is skipped or merged
**Then** the duplicate decision is logged with the idempotency key and reason.

**Given** a human changes a classification
**When** the change is saved
**Then** the original value, new value, reviewer, timestamp, and reason are captured in the audit trail.

## Implementation Links

- Story 1.1 operating contract: [docs/finance-ledger-operating-contract.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/finance-ledger-operating-contract.md)
- Story 1.1 and 1.3 flow doc: [docs/finance-document-intake.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/finance-document-intake.md)
- Story 1.2 job schema: [automation/schemas/finance-job.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/finance-job.schema.json)
- Story 1.2 and 1.5 extraction schema: [automation/schemas/finance-extraction.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/finance-extraction.schema.json)
- Story 1.3 worker contract implementation: [automation/scripts/codex-finance-worker.sh](/home/dank/Projects/holden-capital-agentic-workflows/automation/scripts/codex-finance-worker.sh)
- Story 1.2 through 1.5 workflow blueprint notes: [automation/workflows/finance-document-intake-codex-assisted.blueprint.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/workflows/finance-document-intake-codex-assisted.blueprint.json)
- Sample packets and outputs: [automation/samples/finance-job.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/finance-job.sample.json), [automation/samples/finance-extraction.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/finance-extraction.sample.json), [automation/samples/finance-extraction.failed.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/finance-extraction.failed.sample.json)
