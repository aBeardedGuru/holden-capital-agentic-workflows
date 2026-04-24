# Financial Operations Sample Flow Setup Guide

Date: 2026-04-23
Scope: Documentation-only setup for designing Holden Capital sample flows before implementation in `holden-capital-mono`.

## Working Model

Use this repo as the design bench for financial operations flows. Do not start by editing `holden-capital-mono`.

Recommended flow lifecycle:

1. Draft the flow spec in this repo.
2. Review the trigger, payload, approval behavior, accounting impact, and failure behavior.
3. Convert the approved spec into n8n JSON in the appropriate implementation folder in `holden-capital-mono`.
4. Test in n8n dry-run mode.
5. Add real integrations only after idempotency, audit logging, and reconciliation rules are clear.

## Financial Automation Focus

Prioritize flows that reduce manual bookkeeping work and improve financial visibility:

| Area | Business Outcome | First Automation Target |
| --- | --- | --- |
| Financial reporting | Faster owner/operator visibility into cash flow, income, expenses, and exceptions | Weekly financial snapshot assembled from source exports. |
| Invoice collection | Fewer missed vendor/customer invoices and cleaner payment follow-up | Invoice intake, status classification, and reminder queue. |
| Expense tracking | Better categorization, property attribution, and receipt capture | Receipt/expense intake with category suggestions and exception review. |

The first sample flows should be dry-run and review-oriented. A financial workflow should prepare a report, queue a reminder, or classify an expense before it posts anything into an accounting system.

## Sample Flow Spec Template

Copy this section into a new doc for each sample flow.

```markdown
# Flow: [Name]

## Purpose

[What business outcome this flow creates.]

## Trigger

- Type: webhook | schedule | manual | API event
- Event name:
- Source system:
- SLA:

## Required Payload

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| source_record.id | string | yes | Unique source record identifier. |
| source_record.system | string | yes | Origin system, such as bank export, Stripe, QuickBooks, email, or property system. |
| amount | number | yes | Positive or negative money value. |
| currency | string | yes | ISO currency code, normally `USD`. |
| occurred_at | string | yes | ISO timestamp or transaction date. |

## Optional Payload

| Field | Type | Used For |
| --- | --- | --- |
| property_id | string | Property-level reporting and allocation. |
| vendor.name | string | Invoice or expense classification. |
| receipt_url | string | Receipt review and audit trail. |
| accounting_category | string | Suggested chart-of-accounts mapping. |

## Output Draft

### Human Review Summary

- Status:
- Recommended action:
- Exceptions:
- Review link:

### System Action

- Destination:
- Dry-run payload:
- Required approval:

## Validation Rules

- Missing required fields:
- Invalid amount:
- Unknown property:
- Unknown vendor:
- Duplicate source record:
- Missing receipt or invoice attachment:

## Flow Steps

1. Receive trigger.
2. Validate payload.
3. Normalize data.
4. Classify record.
5. Detect exceptions and duplicates.
6. Prepare dry-run output for review.
7. Production accounting or reminder action, when enabled.
8. Record audit log.

## Error Handling

| Failure | Behavior |
| --- | --- |
| Missing required field | Reject with clear validation message. |
| Duplicate source record | Skip posting and log duplicate decision. |
| Low-confidence category | Queue for human review. |
| Transient provider failure | Retry with backoff. |
| Permanent provider failure | Alert operator and log failed action. |

## Idempotency

- Idempotency key:
- Duplicate behavior:
- Log lookup:
- Audit record:

## Acceptance Criteria

- Given a valid payload, when the flow runs, then it returns a dry-run financial action draft.
- Given a missing required field, when the flow runs, then it rejects the payload with the missing field name.
- Given a low-confidence classification, when the flow runs, then it queues the item for human review instead of posting.
- Given the same source record twice, when production actions are enabled, then the flow does not create duplicate accounting entries or reminders.
```

## Flow 1: Weekly Financial Snapshot Dry Run

### Purpose

Create a weekly financial operating snapshot without manually assembling income, expense, invoice, and exception data.

### Trigger

- Type: schedule
- Timing: weekly, Monday morning
- Source systems: accounting export, bank export, property revenue export, invoice tracker
- SLA target: draft report ready before weekly review

### Required Payload

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| reporting_period.start | string | yes | ISO date. |
| reporting_period.end | string | yes | ISO date. |
| income.total | number | yes | Gross income for period. |
| expenses.total | number | yes | Expense total for period. |
| invoices.open_count | number | yes | Open invoice count. |
| invoices.overdue_count | number | yes | Overdue invoice count. |
| exceptions.count | number | yes | Items requiring review. |

### Optional Payload

| Field | Type | Used For |
| --- | --- | --- |
| property_breakdown[] | array | Property-level income, expenses, and net operating view. |
| cash_balance.current | number | Cash position snapshot. |
| uncategorized_expenses.count | number | Bookkeeping cleanup priority. |
| large_variance_items[] | array | Explain material changes from prior period. |

### Dry-Run Output

The dry-run flow should return:

```json
{
  "status": "accepted",
  "reportingPeriod": "2026-04-13/2026-04-19",
  "summary": {
    "income": 12450.00,
    "expenses": 3865.25,
    "net": 8584.75,
    "openInvoices": 6,
    "overdueInvoices": 2,
    "exceptions": 4
  },
  "recommendedActions": [
    "Review 4 uncategorized expenses before posting the weekly snapshot.",
    "Send reminders for 2 overdue invoices.",
    "Investigate cleaning expense variance above threshold."
  ]
}
```

### Production Promotion

Before activation, add:

- Read-only connectors for accounting, bank, invoice, and property revenue data.
- Report delivery target, such as email, dashboard, or shared folder.
- Variance thresholds by property and category.
- Audit log with source file versions and generated report hash.
- Human approval before sending owner-facing financial reports.

## Flow 2: Invoice Collection Queue Dry Run

### Purpose

Collect invoice data, classify payment status, and prepare follow-up actions without sending live reminders first.

### Trigger

- Type: schedule or inbox trigger
- Timing: daily business morning, plus optional email attachment intake
- Source systems: invoice inbox, accounting system, vendor portal, payment processor
- SLA target: same-day classification for new or overdue invoices

### Required Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| invoice.id | string | yes | Invoice identifier from source or generated hash. |
| invoice.number | string | yes | Vendor/customer invoice number when available. |
| invoice.party.name | string | yes | Vendor, customer, tenant, or counterparty. |
| invoice.amount_due | number | yes | Outstanding amount. |
| invoice.currency | string | yes | Normally `USD`. |
| invoice.issue_date | string | yes | Invoice issue date. |
| invoice.due_date | string | yes | Due date for aging. |
| invoice.status | string | yes | `new`, `open`, `paid`, `partial`, `overdue`, or `disputed`. |

### Classification Rule

- If status is `paid`, mark complete and do not queue follow-up.
- If due date is past and amount due is greater than zero, queue overdue reminder draft.
- If invoice lacks vendor/customer mapping, queue for human review.
- If invoice amount differs from matching payment record, mark as reconciliation exception.

### Dry-Run Output

The dry-run flow should return:

```json
{
  "status": "accepted",
  "invoiceId": "inv_2044",
  "classification": "overdue",
  "daysOverdue": 12,
  "recommendedAction": "queue_payment_follow_up",
  "approvalRequired": true,
  "reminderDraft": {
    "to": "ap@example-vendor.com",
    "subject": "Payment follow-up for invoice INV-2044",
    "body": "Please confirm payment status for invoice INV-2044..."
  }
}
```

### Production Promotion

Before activation, add:

- Email or accounting connector for invoice intake.
- Attachment storage and OCR/extraction path, if invoices arrive as PDFs.
- Counterparty mapping table.
- Payment matching rule.
- Approval gate before external reminders are sent.
- Audit log for every reminder decision.

## Flow 3: Expense Intake And Categorization Dry Run

### Purpose

Capture expenses quickly, assign property and category suggestions, and route uncertain items for review before bookkeeping entry.

### Trigger

- Type: inbox trigger, mobile receipt upload, bank transaction import, or manual form
- Timing: continuous intake with daily review digest
- Source systems: bank export, receipt inbox, card feed, manual upload
- SLA target: expense classified or queued for review within one business day

### Required Data

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| expense.source_record_id | string | yes | Idempotency key component. |
| expense.amount | number | yes | Transaction amount. |
| expense.currency | string | yes | Normally `USD`. |
| expense.occurred_at | string | yes | Transaction or receipt date. |
| expense.merchant | string | yes | Merchant or vendor name. |
| expense.description | string | yes | Bank memo, receipt text, or manual note. |

### Optional Data

| Field | Type | Used For |
| --- | --- | --- |
| property_id | string | Direct property attribution. |
| receipt_url | string | Audit evidence. |
| payment_account | string | Reconciliation and account mapping. |
| tax_hint | string | CPA review and deductible category hint. |

### Classification Rule

- Match merchant and memo against known vendor/category rules.
- Infer property from property alias, card, vendor, or upload folder.
- Require human review when confidence is below threshold, receipt is missing above a dollar limit, or property attribution is ambiguous.
- Never post to accounting when category confidence is low.

### Dry-Run Output

```json
{
  "status": "review_required",
  "sourceRecordId": "bank_txn_88391",
  "suggestedCategory": "Repairs and Maintenance",
  "suggestedPropertyId": "sunchase-308",
  "confidence": 0.78,
  "exceptions": [
    "Receipt missing for expense above review threshold"
  ],
  "recommendedAction": "queue_bookkeeping_review"
}
```

### Production Promotion

Before activation, add:

- Known vendor/category mapping table.
- Receipt storage and naming convention.
- Review queue destination.
- Accounting-system draft entry creation.
- Duplicate detection keyed by source record, amount, date, and merchant.
- Monthly export for CPA or bookkeeper review.

## Minimum Review Checklist

Before implementing any financial sample flow in n8n:

- The trigger and payload are documented.
- Required fields are explicit.
- Missing-data behavior is explicit.
- The dry-run financial action is visible in the spec.
- Idempotency is defined.
- Human approval gates are defined for posting, reminders, and owner-facing reports.
- Logging and audit targets are known.
- Reconciliation behavior is explicit.
- Sensitive financial data is minimized in workflow logs.
- Secrets are not embedded in exported workflow JSON.

## Recommended Next Docs

Create these next, in order:

1. `docs/flow-weekly-financial-snapshot.md`
2. `docs/flow-invoice-collection-queue.md`
3. `docs/flow-expense-intake-categorization.md`
4. `docs/financial-event-schema.md`
5. `docs/financial-automation-readiness-checklist.md`
