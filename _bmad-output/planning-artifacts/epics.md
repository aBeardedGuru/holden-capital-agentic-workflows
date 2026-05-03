---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - planning/prd-financial-operations-automation.md
  - planning/epics/requirements-inventory.md
  - _bmad-output/planning-artifacts/architecture.md
---

# holden-capital-agentic-workflows - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for holden-capital-agentic-workflows, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Support Drive-first finance document intake that creates one processing job for each supported document placed in `Holden Capital/Finance Automation/00_INBOX`.

FR2: Run OpenRouter-backed classification/extraction in n8n for each finance job and write structured JSON output to the expected output path.

FR3: Process valid extraction output through n8n so Google Sheets is updated and the source document is moved to processed, review, or error folders.

FR4: Generate periodic financial summary drafts (weekly and monthly) from normalized income, expense, invoice, and exception inputs.

FR5: Include property-level breakdowns in periodic summaries when property-level data is available.

FR6: Surface uncategorized expenses, material variances, overdue invoices, and other recommended review actions in periodic summaries.

FR7: Log report source inputs and generation timestamp when a periodic summary is stored or sent.

FR8: Classify invoice records as new, open, paid, partial, overdue, disputed, or review required.

FR9: Prepare overdue invoice reminder drafts without sending them unless approval is explicitly granted.

FR10: Mark paid invoices complete and avoid queuing follow-up.

FR11: Mark invoice/payment amount mismatches as reconciliation exceptions.

FR12: Suggest category, property/entity, confidence, and review status for each expense source record.

FR13: Route low-confidence expense classifications to human review instead of posting.

FR14: Route receipt-required expenses to review when the receipt is missing.

FR15: Prevent duplicate draft entries when the same source record appears more than once.

FR16: Provide one review queue for flow exceptions.

FR17: Allow review queue statuses to be updated to approved, corrected, rejected, or needs more info.

FR18: Promote approved review items from draft to action when production actions are later enabled.

FR19: Record audit details for every processed document or source record, including source ID/path, timestamp, confidence, output JSON location, and final status.

FR20: Log duplicate detection decisions.

FR21: Capture human classification changes and reasons.

FR22: Classify billing and deposit-related inbound communications by operational priority and send internal alerts for high-priority finance items.

FR23: Provide one unified operator command surface that shows finance intake status, review queue status, invoice follow-up drafts, and periodic summary status in one workflow session.

FR24: Define and version cross-repo contracts between `holden-capital-agentic-workflows` finance artifacts and `holden-capital-mono` runtime/UI surfaces.

FR25: Provide an end-to-end daily close run path that can be executed without manual repo-to-repo data stitching.

FR26: Require bridge-level acceptance checks proving that finance workflow outputs are visible and actionable in the operator-facing monorepo experience.

### NonFunctional Requirements

NFR1: No live financial posting or external reminders without explicit approval in MVP.

NFR2: Do not store full account numbers; last four digits only.

NFR3: Do not store bank credentials, API keys, or n8n credentials in repo files or job JSON.

NFR4: Failed jobs must move to an error state with a reason, and source documents must never be deleted.

NFR5: Every output row must be traceable back to a source document or source record.

NFR6: Use OpenRouter-backed model calls in n8n with bounded payload size and deterministic JSON output constraints.

NFR7: Runtime files must remain under ignored `runtime/` paths and must not be committed.

### Additional Requirements

- Use Google Drive as the document intake and file lifecycle surface.
- Use Google Sheets as the first review and ledger surface with `Transactions`, `Documents`, `Review Queue`, and `Run Log` tabs.
- Use n8n as the single orchestration surface for intake, classification, routing, and logging.
- Use OpenRouter-backed models from n8n and enforce deterministic structured JSON output.
- Use `automation/schemas/finance-job.schema.json` and `automation/schemas/finance-extraction.schema.json` as canonical contracts.
- Preserve contract synchronization across `planning -> docs -> automation`.
- Keep external reminders/accounting posts behind explicit approval gates.
- Apply idempotency and duplicate decision logging in every flow.
- Validate model output against schema before any side effects.
- Fail closed for external actions and emit machine-readable reason codes.
- Keep runtime data local/ignored under `runtime/`.
- Introduce cross-repo promotion gates so design-contract changes align with monorepo runtime/UI behavior.

### UX Design Requirements

No dedicated UX design document was found in planning artifacts. Current implied UX surface is Google Drive + Google Sheets; unification work requires a dedicated operator UX contract.

### FR Coverage Map

FR1: Epic 1 - Finance intake foundation.
FR2: Epic 1 - OpenRouter extraction and output contract.
FR3: Epic 1 - Sheets update and file routing.
FR4: Epic 4 - Periodic summary generation.
FR5: Epic 4 - Property-level reporting.
FR6: Epic 4 - Exception and review action surfacing.
FR7: Epic 4 - Summary run logging.
FR8: Epic 3 - Invoice status classification.
FR9: Epic 3 - Approval-gated overdue reminder drafts.
FR10: Epic 3 - Paid invoice completion handling.
FR11: Epic 3 - Reconciliation exception detection.
FR12: Epic 2 - Expense categorization suggestion.
FR13: Epic 2 - Low-confidence review routing.
FR14: Epic 2 - Missing-receipt review routing.
FR15: Epic 2 - Duplicate expense prevention.
FR16: Epic 1 - Shared review queue foundation.
FR17: Epic 1 - Review queue status lifecycle.
FR18: Epic 1 - Draft-to-action promotion model.
FR19: Epic 1 - Shared audit trail.
FR20: Epic 1 - Duplicate decision logging.
FR21: Epic 1 - Human correction audit logging.
FR22: Epic 3 - Billing/deposit communication triage and alerts.
FR23: Epic 5 - Unified operator command surface.
FR24: Epic 5 - Cross-repo contract versioning.
FR25: Epic 5 - End-to-end daily close loop.
FR26: Epic 5 - Bridge acceptance checks.

## Epic List

### Epic 1: Finance Intake And Review Foundation
Enable the operator to capture finance documents, run extraction, route outcomes, and manage one auditable review queue.
**FRs covered:** FR1, FR2, FR3, FR16, FR17, FR18, FR19, FR20, FR21

### Epic 2: Expense Intake And Categorization
Enable the operator/bookkeeper to turn expense records into categorized draft entries with confidence-based review routing and duplicate protection.
**FRs covered:** FR12, FR13, FR14, FR15

### Epic 3: Invoice Collection Queue
Enable the operator to classify invoice states, identify reconciliation issues, and prepare approval-gated follow-up drafts with internal priority alerts.
**FRs covered:** FR8, FR9, FR10, FR11, FR22

### Epic 4: Periodic Financial Summarization
Enable the operator to generate weekly/monthly summaries with portfolio and property-level visibility, exception surfacing, and run traceability.
**FRs covered:** FR4, FR5, FR6, FR7

### Epic 5: Unified Operator Front And Cross-Repo Bridge
Enable one daily operator close flow across repos with explicit promotion contracts, shared status/event schemas, and end-to-end acceptance validation.
**FRs covered:** FR23, FR24, FR25, FR26


## Epic 1: Finance Intake And Review Foundation

Enable the operator to capture finance documents, run OpenRouter-powered extraction in n8n, update Google Sheets, route files, and manage one review queue with audit trail.

## Implementation Status

Status date: 2026-04-26

- Story 1.1: complete in `docs/finance-ledger-operating-contract.md` and `docs/finance-document-intake.md`.
- Story 1.2: complete in `automation/schemas/finance-job.schema.json`, `automation/schemas/finance-extraction.schema.json`, and aligned samples.
- Story 1.3: complete in n8n workflow contracts and runtime directory contract docs.
- Story 1.4: contract complete in docs and schema fields; workflow blueprints include review-queue integration notes.
- Story 1.5: complete in extraction schema and docs with duplicate and audit fields.

Conformance note:
- The live n8n workflow `Google Drive INGEST Classification + Expense Sheet` was refactored to emit v1.1 job packets and invoice-only expense-sheet writes.
- The repo workflow artifact `automation/workflows/google-drive-download-for-processing.json` was refactored to the same v1.1 contract and placeholder-safe credential references.

### Story 1.1: Define Finance Ledger And Drive Operating Contract

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

### Story 1.2: Define Job Packet And Extraction Output Schemas

As a workflow implementer,
I want explicit job and extraction schemas,
So that n8n workflow nodes and model responses exchange predictable finance data.

**Acceptance Criteria:**

**Given** n8n creates a document-processing job
**When** the job JSON is validated
**Then** it conforms to `automation/schemas/finance-job.schema.json`
**And** it includes job ID, Drive file metadata, source file path or ID, MIME type, extracted text path when available, and processing timestamps.

**Given** OpenRouter model classification/extraction completes in n8n
**When** output JSON is validated
**Then** it conforms to `automation/schemas/finance-extraction.schema.json`
**And** it includes document type, vendor/payee, date, amount, currency, confidence, suggested category, suggested property/entity, status, and review reason when applicable.

**Given** privacy requirements apply
**When** schemas are reviewed
**Then** they reject full account numbers
**And** allow only account last four digits when account metadata is needed.

### Story 1.3: Document OpenRouter n8n Runtime Contract

As a workflow operator,
I want a runtime contract for OpenRouter-assisted extraction in n8n,
So that document processing runs in one orchestration surface with explicit model and credential boundaries.

**Acceptance Criteria:**

**Given** a job JSON file exists in `runtime/finance-document-intake/inbox/`
**When** the n8n flow runs once
**Then** it invokes an OpenRouter model node according to the contract and writes output JSON to `runtime/finance-document-intake/outputs/`.

**Given** runtime data is operational data
**When** the runtime contract is documented
**Then** it defines `inbox`, `processing`, `complete`, `failed`, and `outputs` directories
**And** it states runtime files must not be committed.

**Given** an n8n extraction failure occurs
**When** the job cannot be completed
**Then** the contract defines how the job moves to failed state with a machine-readable reason.

### Story 1.4: Define Review Queue Lifecycle

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

### Story 1.5: Define Shared Audit And Duplicate Decision Logging

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
- Story 1.3 runtime implementation: [automation/workflows/google-drive-download-for-processing.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/workflows/google-drive-download-for-processing.json)
- Sample packets and outputs: [automation/samples/finance-job.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/finance-job.sample.json), [automation/samples/finance-extraction.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/finance-extraction.sample.json), [automation/samples/finance-extraction.failed.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/finance-extraction.failed.sample.json)

## Epic 2: Expense Intake And Categorization

Enable the operator/bookkeeper to turn expense documents and source records into categorized, property-attributed draft entries while routing uncertain or missing-receipt items to review.

### Story 2.1: Define Expense Source Record Contract

As a bookkeeper,
I want a normalized expense source record contract,
So that receipts, bank transactions, card transactions, and manual uploads can be classified consistently.

**Acceptance Criteria:**

**Given** an expense source record is prepared
**When** it is validated
**Then** it includes source record ID, amount, currency, occurred date, merchant, description, and source system.

**Given** optional attribution data exists
**When** the source record is validated
**Then** it can include property ID, receipt URL, payment account last four, tax hint, and existing category hint.

**Given** a required field is missing
**When** validation runs
**Then** the item is rejected or queued for review with the missing field names.

### Story 2.2: Classify Expense Category And Property Drafts

As a Holden Capital operator,
I want expense records to receive category and property suggestions,
So that bookkeeping review starts from a useful draft instead of a blank spreadsheet row.

**Acceptance Criteria:**

**Given** a valid expense source record
**When** the categorization flow runs
**Then** it suggests an accounting category, property/entity, confidence score, and review status.

**Given** known vendor, memo, or property alias rules match the expense
**When** classification completes
**Then** the suggested category and property/entity reflect the matched rule
**And** the rule or source of confidence is recorded.

**Given** no confident rule or extraction result exists
**When** classification completes
**Then** the item is marked review required instead of approved.

### Story 2.3: Route Low-Confidence And Missing-Receipt Expenses To Review

As a bookkeeper,
I want risky expense items routed to review automatically,
So that uncertain or unsupported entries are not silently accepted.

**Acceptance Criteria:**

**Given** category or property confidence is below threshold
**When** the expense flow runs
**Then** the item is added to the `Review Queue`
**And** no accounting draft is marked approved.

**Given** an expense exceeds the receipt-required threshold
**When** no receipt URL or document reference exists
**Then** the item is added to the `Review Queue` with reason `missing_receipt`.

**Given** an item is queued for review
**When** the queue row is created
**Then** it includes suggested category, suggested property/entity, amount, merchant, confidence, and recommended action.

### Story 2.4: Prevent Duplicate Expense Drafts

As a Holden Capital operator,
I want repeated expense source records to be detected,
So that duplicate draft entries do not pollute the ledger.

**Acceptance Criteria:**

**Given** an expense source record has already been processed
**When** the same source record ID appears again
**Then** the flow skips creating a new draft transaction
**And** logs the duplicate decision.

**Given** a near-duplicate expense has the same merchant, amount, date, and payment account last four
**When** the flow detects the match
**Then** it queues the item for review instead of auto-approving it.

**Given** duplicate detection runs
**When** it creates an idempotency key
**Then** the key is stored with the transaction or review row.

### Story 2.5: Produce Expense Categorization Dry-Run Output

As a workflow implementer,
I want a dry-run output format for expense categorization,
So that the operator can approve behavior before any accounting system posting exists.

**Acceptance Criteria:**

**Given** a valid expense item is processed
**When** the dry-run flow completes
**Then** it returns or records source record ID, suggested category, suggested property/entity, confidence, exceptions, and recommended action.

**Given** the item is approved by rules
**When** dry-run output is created
**Then** it is marked as draft-approved, not production-posted.

**Given** the item requires review
**When** dry-run output is created
**Then** it references the created review queue row.

## Epic 3: Invoice Collection Queue

Enable the operator to classify invoices, triage high-priority billing communications, identify overdue or mismatched items, and prepare approved follow-up actions without sending unapproved reminders.

### Story 3.1: Define Invoice Source Record Contract

As a Holden Capital operator,
I want invoice records normalized at intake,
So that invoice status and collection rules can run consistently.

**Acceptance Criteria:**

**Given** an invoice source record is prepared
**When** it is validated
**Then** it includes invoice ID, invoice number when available, counterparty name, amount due, currency, issue date, due date, and status.

**Given** an invoice has optional payment or attachment context
**When** it is validated
**Then** it can include payment reference, attachment URL, counterparty email, property/entity, and notes.

**Given** required invoice fields are missing
**When** validation runs
**Then** the invoice is routed to review with specific missing field reasons.

### Story 3.2: Classify Invoice Payment Status

As a Holden Capital operator,
I want invoices classified by collection status,
So that I can see which invoices need no action, review, or follow-up.

**Acceptance Criteria:**

**Given** an invoice has amount due and due date
**When** the invoice classification flow runs
**Then** it classifies the invoice as new, open, paid, partial, overdue, disputed, or review required.

**Given** an invoice status is paid
**When** classification completes
**Then** the invoice is marked complete
**And** no follow-up reminder is queued.

**Given** invoice data is ambiguous or disputed
**When** classification completes
**Then** it is routed to the `Review Queue` with reason and recommended next action.

### Story 3.3: Detect Invoice Payment Reconciliation Exceptions

As a bookkeeper,
I want invoice and payment mismatches flagged,
So that collection status does not rely on bad assumptions.

**Acceptance Criteria:**

**Given** an invoice has a matching payment record
**When** the invoice amount and payment amount match
**Then** the invoice can be marked paid or complete according to the status rule.

**Given** invoice amount and matching payment amount do not match
**When** classification runs
**Then** the invoice is marked as a reconciliation exception.

**Given** a reconciliation exception is created
**When** the review row is written
**Then** it includes invoice amount, matched payment amount, difference, source references, and recommended action.

### Story 3.4: Prepare Overdue Invoice Reminder Drafts

As a Holden Capital operator,
I want overdue invoice reminders drafted but not sent,
So that I can approve external follow-up before it leaves the system.

**Acceptance Criteria:**

**Given** an invoice is overdue and amount due is greater than zero
**When** the reminder draft flow runs
**Then** it creates a reminder draft with recipient, subject, body, invoice number, amount due, and days overdue.

**Given** reminder approval has not been granted
**When** the draft is created
**Then** no external email, SMS, or payment request is sent.

**Given** a reminder draft is created
**When** it is logged
**Then** the audit trail records invoice ID, draft timestamp, approval status, and source classification.

### Story 3.5: Prevent Duplicate Invoice Follow-Up Drafts

As a Holden Capital operator,
I want duplicate reminder drafts prevented,
So that counterparties are not spammed when production sending is later enabled.

**Acceptance Criteria:**

**Given** an overdue invoice already has an open reminder draft for the same follow-up window
**When** the invoice flow runs again
**Then** it does not create a second draft
**And** it logs the duplicate reminder decision.

**Given** invoice status changes after a draft is created
**When** the flow runs
**Then** paid invoices cancel or suppress further reminder drafts.

**Given** a reminder draft is suppressed
**When** audit logging occurs
**Then** the suppression reason is visible in the invoice audit record.

### Story 3.6: Triage Billing Communication Priority And Internal Alerts

As a Holden Capital operator,
I want billing and deposit-related messages triaged by priority,
So that urgent finance items are surfaced immediately without relying on manual inbox scanning.

**Acceptance Criteria:**

**Given** a billing-related inbound communication is detected
**When** the triage flow runs
**Then** it classifies the communication as `high_priority_finance`, `finance_routine`, or `non_finance`
**And** records the confidence and reason for that classification.

**Given** a message is classified as `high_priority_finance`
**When** triage completes
**Then** an internal operator alert is sent to the configured channel (for example Telegram)
**And** the alert references sender, subject, due date when available, and recommended next action.

**Given** a message lacks enough data for confident triage
**When** classification completes
**Then** the message is routed to the `Review Queue` with reason `needs_priority_review`
**And** no external reminder is sent.

## Epic 4: Periodic Financial Summarization

Enable the operator to produce periodic (weekly and monthly) financial summaries that cover income, expenses, invoice status, property breakdowns, and review actions.

### Story 4.1: Define Periodic Summary Input Contract

As a Holden Capital operator,
I want a normalized periodic report input contract,
So that financial summaries can be generated from reviewed ledger data.

**Acceptance Criteria:**

**Given** a periodic summary run is requested
**When** input validation runs
**Then** it requires reporting period start, reporting period end, income total, expense total, open invoice count, overdue invoice count, and exception count.

**Given** optional property-level data exists
**When** input validation runs
**Then** it accepts property breakdowns, cash balance, uncategorized expense count, and large variance items.

**Given** required report inputs are missing
**When** validation runs
**Then** the summary is not generated
**And** the missing inputs are logged.

### Story 4.2: Generate Weekly Financial Summary Draft

As a Holden Capital operator,
I want a weekly summary draft,
So that I can review business performance without manually assembling the basics.

**Acceptance Criteria:**

**Given** valid weekly summary inputs exist
**When** the summary flow runs
**Then** it generates a summary with income, expenses, net, open invoices, overdue invoices, and exception count.

**Given** expense and invoice data includes review statuses
**When** the summary is generated
**Then** it identifies how many items still need review before the report is owner-ready.

**Given** the report is generated
**When** dry-run output is saved
**Then** it is clearly marked as draft and not final accounting output.

### Story 4.3: Add Property-Level Breakdown To Weekly Snapshot

As a Holden Capital operator,
I want weekly results broken down by property or entity,
So that I can see which assets are driving income, expenses, and exceptions.

**Acceptance Criteria:**

**Given** property-level data is available
**When** the weekly snapshot is generated
**Then** it includes income, expenses, net, uncategorized expenses, and exceptions by property/entity.

**Given** a transaction lacks property/entity attribution
**When** property breakdowns are generated
**Then** the item is counted in an unattributed bucket
**And** the report recommends review.

**Given** property breakdowns are unavailable
**When** the report is generated
**Then** the report still produces the portfolio-level summary
**And** logs that property-level detail was unavailable.

### Story 4.4: Surface Variances And Recommended Review Actions

As a Holden Capital operator,
I want the weekly snapshot to highlight exceptions,
So that I spend review time on what actually needs attention.

**Acceptance Criteria:**

**Given** uncategorized expenses exist
**When** the snapshot is generated
**Then** it includes a recommended action to review uncategorized expenses.

**Given** overdue invoices exist
**When** the snapshot is generated
**Then** it includes a recommended action to review or approve invoice follow-up drafts.

**Given** material variance items exceed configured thresholds
**When** the snapshot is generated
**Then** it lists the variance item, category or property, threshold crossed, and suggested review action.

### Story 4.5: Log Periodic Summary Sources And Generation Metadata

As a bookkeeper or operator,
I want every periodic summary to be traceable,
So that report numbers can be explained later.

**Acceptance Criteria:**

**Given** a periodic summary is generated
**When** it is stored or sent
**Then** the run log records flow name, reporting period, source window, generation timestamp, input source references, and output location.

**Given** the same reporting period is regenerated
**When** a new snapshot is created
**Then** the run log preserves the prior run and records the new run separately.

**Given** source validation errors occur
**When** the summary run completes
**Then** validation errors are captured in the `Run Log`
**And** the summary status reflects draft, blocked, or review required.

### Story 4.6: Generate Monthly Financial Summary Draft

As a Holden Capital operator,
I want a month-end summary draft,
So that bookkeeping and reconciliation work can start from a complete monthly view.

**Acceptance Criteria:**

**Given** valid monthly summary inputs exist
**When** the month-end summary flow runs
**Then** it generates monthly totals for income, expenses, net, open invoices, overdue invoices, and exception count.

**Given** monthly data includes prior-period comparables
**When** the month-end summary is generated
**Then** it includes period-over-period deltas for key totals
**And** flags material changes for review.

**Given** the month-end report is generated
**When** dry-run output is saved
**Then** it is clearly marked as draft and not final accounting output.

## Epic 5: Unified Operator Front And Cross-Repo Bridge

Enable the operator to run one daily finance-and-portfolio review loop from a single command surface with explicit contracts between planning artifacts and monorepo runtime surfaces.

### Story 5.1: Define Cross-Repo Boundary And Promotion Contract

As a Holden Capital operator and platform owner,
I want a clear boundary contract between planning/design and runtime implementation repos,
So that finance workflow behavior does not drift across repos.

**Acceptance Criteria:**

**Given** changes are made in `planning/`, `docs/`, or `automation/` in this repo
**When** a flow is promoted to implementation
**Then** the promotion checklist defines required updates in `holden-capital-mono`
**And** ownership is explicit for docs authority and runtime authority.

**Given** a contract change is proposed
**When** review occurs
**Then** the change records schema version, affected workflow IDs, and impacted monorepo integration points.

### Story 5.2: Define Unified Operator UX Contract

As a Holden Capital operator,
I want one defined daily operating path,
So that intake review, exception triage, invoice follow-up, and summary checks happen in one session.

**Acceptance Criteria:**

**Given** the unified-front UX contract is drafted
**When** it is reviewed
**Then** it documents entry point, required actions, status indicators, and completion criteria for one daily close session.

**Given** a finance exception exists
**When** the operator runs the daily loop
**Then** the workflow shows where the exception is surfaced and how it is resolved or deferred.

### Story 5.3: Publish Bridge Event And Status Schema

As a workflow implementer,
I want shared bridge schemas for status and events,
So that repo-level and app-level components exchange consistent state.

**Acceptance Criteria:**

**Given** a finance flow run is in progress or complete
**When** status is emitted
**Then** it conforms to a versioned bridge schema with flow ID, run ID, status, timestamps, confidence summary, and review queue count.

**Given** integration updates are applied
**When** schema validation runs
**Then** contract tests confirm compatibility between this repo artifacts and monorepo runtime consumers.

### Story 5.4: Add Daily Close Workflow Runbook And Acceptance Checks

As a Holden Capital operator,
I want a runbook and acceptance checks for a daily close loop,
So that I can reliably execute the workflow and confirm it is working end-to-end.

**Acceptance Criteria:**

**Given** the daily close runbook exists
**When** the operator follows it
**Then** the runbook covers intake verification, review queue resolution, invoice follow-up review, and summary validation.

**Given** acceptance checks are run
**When** the loop completes
**Then** they verify that each step completed without manual repo-to-repo stitching
**And** they record pass/fail status in an auditable log.
