# Epic 4: Periodic Financial Summarization

Enable the operator to produce periodic (weekly and monthly) financial summaries that cover income, expenses, invoice status, property breakdowns, and review actions.

## Story 4.1: Define Periodic Summary Input Contract

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

## Story 4.2: Generate Weekly Financial Summary Draft

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

## Story 4.3: Add Property-Level Breakdown To Weekly Snapshot

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

## Story 4.4: Surface Variances And Recommended Review Actions

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

## Story 4.5: Log Periodic Summary Sources And Generation Metadata

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

## Story 4.6: Generate Monthly Financial Summary Draft

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
