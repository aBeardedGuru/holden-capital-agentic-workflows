---
title: Financial Operations Automation PRD
project: holden-capital-agentic-workflows
status: draft
owner: dank
created: 2026-04-23
sourceDocuments:
  - docs/finance-document-intake.md
  - docs/sample-flow-setup-guide.md
  - docs/holden-capital-mono-business-review.md
---

# Financial Operations Automation PRD

## 1. Product Thesis

Holden Capital needs a lightweight financial operations automation layer that reduces manual bookkeeping work before it tries to become a full accounting platform.

The first useful product is not "automated accounting." That is too broad and too risky. The first useful product is a review-first workflow system that:

1. Collects finance documents and source records.
2. Extracts structured financial data.
3. Classifies invoices, expenses, and reporting inputs.
4. Queues uncertain items for review.
5. Produces weekly financial visibility without manual spreadsheet assembly.

Why this matters: financial work gets painful when documents, invoices, receipts, and transaction context live in different places. The product should make the weekly review faster, make missing invoices visible, and keep expenses categorized with enough audit trail to support bookkeeping and tax work.

## 2. Primary User

Primary user: Holden Capital operator/owner.

Jobs to be done:

- When finance documents arrive, I want them captured and classified so I do not manually file and transcribe them.
- When invoices are open or overdue, I want a clear queue so I can collect or follow up before they become surprises.
- When expenses hit bank or card accounts, I want suggested categories and property attribution so bookkeeping stays current.
- When I review the business weekly, I want income, expenses, invoice status, and exceptions summarized in one place.

Secondary users:

- Bookkeeper or CPA reviewing categorized transactions and source documents.
- Future implementation agent converting approved flow specs into n8n workflows.

## 3. Problem Statement

Current financial operations are likely split across Drive files, invoices, receipts, bank/card data, Google Sheets, and manual review. That creates four practical problems:

1. Financial reports require manual assembly.
2. Invoices can be missed, duplicated, or followed up late.
3. Expenses can remain uncategorized or detached from the right property/entity.
4. There is no consistent audit trail from source document to classified record to human review decision.

The product must solve these without introducing silent financial posting risk.

## 4. MVP Scope

The MVP is documentation and dry-run workflow design for three financial flows:

| Flow | User Value | MVP Behavior |
| --- | --- | --- |
| Weekly Financial Snapshot | Operator sees cash flow and exceptions faster | Assemble a dry-run weekly report from normalized source data. |
| Invoice Collection Queue | Operator sees open/overdue invoices and follow-up actions | Classify invoice status and queue reminder drafts for approval. |
| Expense Intake and Categorization | Operator/bookkeeper sees categorized expense drafts | Extract, classify, and route low-confidence items to review. |

The MVP must integrate with the existing finance document intake direction:

- Google Drive is the document intake and filing surface.
- n8n handles Drive, Sheets, and workflow orchestration.
- OpenRouter-backed models run inside n8n for classification and extraction.
- Google Sheets acts as the first ledger/review system.

## 5. Out Of Scope

These are explicitly not MVP:

- Direct bank login automation.
- Automatic production posting to QuickBooks, Xero, or another accounting system.
- Tax filing or CPA judgment.
- Payment initiation.
- Unapproved external invoice reminders.
- Full BI dashboarding.
- Multi-user permissions beyond basic owner/operator review.

Why exclude these? Because the highest-risk failure is silently doing the wrong financial thing. The MVP should prepare, classify, and queue decisions before it posts or sends.

## 6. Functional Requirements

### FR1: Finance Document Intake

The system must support the existing Drive-first intake model.

Acceptance criteria:

- Given a supported document is placed in `Holden Capital/Finance Automation/00_INBOX`, when intake runs, then the workflow creates a processing record.
- Given a processing record is created, when OpenRouter classification completes, then strict JSON output is written to the expected output path.
- Given output is valid, when n8n processes it, then Google Sheets is updated and the source file is moved to the correct processed/review/error folder.

### FR2: Weekly Financial Snapshot Dry Run

The system must generate a weekly financial snapshot draft.

Acceptance criteria:

- Given normalized income, expense, invoice, and exception inputs for a reporting period, when the flow runs, then it returns a weekly summary with income, expenses, net, open invoices, overdue invoices, and exception count.
- Given property-level data is available, when the flow runs, then the report includes property breakdowns.
- Given uncategorized expenses or material variances exist, when the flow runs, then the report lists recommended review actions.
- Given the report is generated, when it is stored or sent, then the source inputs and generation timestamp are logged.

### FR3: Invoice Collection Queue Dry Run

The system must classify invoices and prepare collection actions.

Acceptance criteria:

- Given an invoice record with amount due and due date, when the flow runs, then it classifies the invoice as new, open, paid, partial, overdue, disputed, or review required.
- Given an overdue invoice with amount due greater than zero, when the flow runs, then it prepares a reminder draft but does not send it without approval.
- Given a paid invoice, when the flow runs, then it marks the invoice complete and does not queue follow-up.
- Given invoice and payment amounts do not match, when the flow runs, then it marks the item as a reconciliation exception.

### FR4: Expense Intake And Categorization Dry Run

The system must classify expense records and route uncertain items.

Acceptance criteria:

- Given an expense source record, when the flow runs, then it suggests category, property/entity, confidence, and review status.
- Given confidence is below threshold, when the flow runs, then the expense is queued for human review instead of posting.
- Given an expense is above the receipt-required threshold and no receipt exists, when the flow runs, then the item is queued for review.
- Given the same source record appears twice, when the flow runs, then it does not create duplicate draft entries.

### FR5: Review Queue

The system must provide one review queue for exceptions.

Acceptance criteria:

- Given a flow cannot confidently classify an item, when it completes, then a row is added to the `Review Queue` sheet.
- Given a row enters the review queue, when it is reviewed, then status can be updated to approved, corrected, rejected, or needs more info.
- Given an item is approved, when production posting is later enabled, then it can be promoted from draft to action.

### FR6: Audit Trail

The system must preserve enough audit trail to explain every financial decision.

Acceptance criteria:

- Given any processed document or source record, when processing completes, then the system records source ID, source URL/path, processing timestamp, classification confidence, output JSON location, and final status.
- Given a duplicate is detected, when processing completes, then the duplicate decision is logged.
- Given a human changes a classification, when saved, then the changed value and reason are captured.

## 7. Non-Functional Requirements

| Requirement | Target |
| --- | --- |
| Safety | No live financial posting or external reminders without explicit approval in MVP. |
| Privacy | Do not store full account numbers; last four digits only. |
| Secret handling | No bank credentials, API keys, or n8n credentials in repo or job JSON. |
| Reliability | Failed jobs move to error state with reason. Source documents are never deleted. |
| Traceability | Every output row can be traced back to source document or source record. |
| Cost | Use OpenRouter model routing in n8n with bounded payloads and model selection controls. |
| Operability | Runtime files remain under ignored `runtime/` paths and are not committed. |

## 8. Data Model

Use the existing `Holden Finance Ledger` Google Sheet as the first system of record.

Tabs:

- `Transactions`
- `Documents`
- `Review Queue`
- `Run Log`

Additional recommended columns:

### Transactions

- `flow_name`
- `idempotency_key`
- `property_confidence`
- `category_confidence`
- `approval_status`
- `approved_by`
- `approved_at`

### Review Queue

- `flow_name`
- `blocking_reason`
- `recommended_action`
- `review_priority`
- `resolution_notes`

### Run Log

- `flow_name`
- `source_window_start`
- `source_window_end`
- `duplicates_detected`
- `validation_errors`

## 9. Flow Priority

### Priority 1: Expense Intake And Categorization

Why first: expense chaos compounds fastest and creates the training data for categories, vendors, properties, and review thresholds.

Smallest validation:

- Process 10 representative receipts/statements.
- Classify document type, vendor, amount, date, category, property/entity, and confidence.
- Route low-confidence items to review.

### Priority 2: Invoice Collection Queue

Why second: invoices require status and follow-up logic, but the reminder action should wait until review and approval patterns are proven.

Smallest validation:

- Process 10 invoices.
- Classify open/paid/overdue/review required.
- Generate reminder drafts without sending.

### Priority 3: Weekly Financial Snapshot

Why third: reporting depends on clean transaction and invoice inputs. Build it after intake and invoice classification create usable data.

Smallest validation:

- Produce one weekly summary from Google Sheets data.
- Include income, expenses, net, overdue invoices, uncategorized expenses, and exceptions.

## 10. Success Metrics

MVP success is not "fully automated books." MVP success is measurable reduction in manual review time.

| Metric | Target |
| --- | --- |
| Document intake success | 90% of sample docs create valid output JSON. |
| Low-risk classification accuracy | 80% of simple receipts/invoices classified correctly before human correction. |
| Review routing | 100% of low-confidence or missing-data items enter review queue. |
| Duplicate prevention | 0 duplicate draft entries from repeated source records in test set. |
| Weekly review prep time | Reduce manual weekly finance prep by at least 50% after flows are live. |

## 11. Key Product Decisions

1. Use Google Drive and Google Sheets first.
   - Why: lowest setup cost, visible to owner/operator, easy for bookkeeper/CPA review.

2. Keep extraction/classification inside n8n using OpenRouter.
   - Why: one orchestration surface, easier model swaps, and fewer local runtime dependencies.

3. Start with draft/review workflows, not autoposting.
   - Why: financial automation needs trust before autonomy.

4. Put idempotency and audit trail in v1.
   - Why: duplicates and unexplained changes are the fastest way to lose trust.

## 12. Open Questions

These need answers before implementation stories are finalized:

1. Which accounting system, if any, should this eventually post to: QuickBooks, Xero, Wave, Google Sheets only, or another system?
2. What are the current source systems for income and invoice data?
3. What properties/entities must be tracked separately on day one?
4. What expense categories should be used: existing chart of accounts, CPA-provided categories, or a simple starting taxonomy?
5. What dollar amount requires a receipt before an expense can be approved?
6. Who approves invoice reminders before they are sent?
7. What is the weekly report audience: owner only, bookkeeper, CPA, investors, or partners?

## 13. Implementation Notes

Initial implementation should produce docs and dry-run artifacts before live workflows:

1. `docs/flow-expense-intake-categorization.md`
2. `docs/flow-invoice-collection-queue.md`
3. `docs/flow-weekly-financial-snapshot.md`
4. `docs/financial-event-schema.md`
5. `docs/financial-automation-readiness-checklist.md`

Only after those are reviewed should implementation move into n8n workflow JSON, schemas, and scripts.
