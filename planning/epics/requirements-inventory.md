# Requirements Inventory

## Functional Requirements

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

FR22: Classify billing and deposit-related inbound communications by operational priority and send internal alerts for high-priority finance items.

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

FR23: Provide one unified operator command surface that shows finance intake status, review queue status, invoice follow-up drafts, and periodic summary status in one workflow session.

FR24: Define and version cross-repo contracts between `holden-capital-agentic-workflows` finance artifacts and `holden-capital-mono` runtime/UI surfaces.

FR25: Provide an end-to-end daily close run path that can be executed without manual repo-to-repo data stitching.

FR26: Require bridge-level acceptance checks proving that finance workflow outputs are visible and actionable in the operator-facing monorepo experience.

## NonFunctional Requirements

NFR1: No live financial posting or external reminders without explicit approval in MVP.

NFR2: Do not store full account numbers; last four digits only.

NFR3: Do not store bank credentials, API keys, or n8n credentials in repo files or job JSON.

NFR4: Failed jobs must move to an error state with a reason, and source documents must never be deleted.

NFR5: Every output row must be traceable back to a source document or source record.

NFR6: Use OpenRouter-backed model calls in n8n with bounded payload size and deterministic JSON output constraints.

NFR7: Runtime files must remain under ignored `runtime/` paths and must not be committed.

## Additional Requirements

- Use Google Drive as the document intake and filing surface.
- Use n8n for Google Drive, Google Sheets, and workflow orchestration.
- Use OpenRouter-backed models in n8n for classification/extraction.
- Use Google Sheets as the first review ledger with `Transactions`, `Documents`, `Review Queue`, and `Run Log` tabs.
- Use `automation/schemas/finance-job.schema.json` for n8n-created job packets.
- Use `automation/schemas/finance-extraction.schema.json` for model-generated output.
- Use runtime directories under `runtime/finance-document-intake/`.
- Maintain explicit approval gates before any external reminder or accounting post.
- Architecture artifacts exist for finance workflow contracts; dedicated unified-front UX documentation is still required.
- Cross-repo promotion gates are required so planning/doc contract updates in this repo align with runtime/UI behavior in `holden-capital-mono`.

## UX Design Requirements

No dedicated UX design specification was provided. The initial UX surface is Google Drive folders and Google Sheets tabs. Review usability requirements are captured through sheet columns, statuses, and review workflow stories.

## FR Coverage Map

FR1: Epic 1 - Finance document intake.

FR2: Epic 1 - OpenRouter extraction in n8n.

FR3: Epic 1 - Sheets update and Drive file routing.

FR4: Epic 4 - Periodic summary generation.

FR5: Epic 4 - Property-level reporting.

FR6: Epic 4 - Exception and recommendation surfacing.

FR7: Epic 4 - Report audit logging.

FR8: Epic 3 - Invoice classification.

FR9: Epic 3 - Overdue reminder draft queue.

FR10: Epic 3 - Paid invoice completion handling.

FR11: Epic 3 - Reconciliation exception handling.

FR22: Epic 3 - Billing and deposit communication priority triage with internal alerts.

FR12: Epic 2 - Expense classification.

FR13: Epic 2 - Low-confidence expense review routing.

FR14: Epic 2 - Missing receipt review routing.

FR15: Epic 2 - Expense duplicate prevention, reused by later flows.

FR16: Epic 1 - Shared review queue foundation.

FR17: Epic 1 - Review status lifecycle.

FR18: Epic 1 - Approved draft promotion model.

FR19: Epic 1 - Shared audit trail.

FR20: Epic 1 - Duplicate decision logging.

FR21: Epic 1 - Human correction audit trail.

FR23: Epic 5 - Unified operator command surface.

FR24: Epic 5 - Cross-repo contract versioning and boundary ownership.

FR25: Epic 5 - End-to-end daily close execution path.

FR26: Epic 5 - Bridge acceptance validation for unified workflow.
