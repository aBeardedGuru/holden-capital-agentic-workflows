# Epic 2: Expense Intake And Categorization

Enable the operator/bookkeeper to turn expense documents and source records into categorized, property-attributed draft entries while routing uncertain or missing-receipt items to review.

## Story 2.1: Define Expense Source Record Contract

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

## Story 2.2: Classify Expense Category And Property Drafts

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

## Story 2.3: Route Low-Confidence And Missing-Receipt Expenses To Review

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

## Story 2.4: Prevent Duplicate Expense Drafts

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

## Story 2.5: Produce Expense Categorization Dry-Run Output

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
