# Epic 3: Invoice Collection Queue

Enable the operator to classify invoices, identify overdue or mismatched items, and prepare approved follow-up actions without sending unapproved reminders.

## Story 3.1: Define Invoice Source Record Contract

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

## Story 3.2: Classify Invoice Payment Status

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

## Story 3.3: Detect Invoice Payment Reconciliation Exceptions

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

## Story 3.4: Prepare Overdue Invoice Reminder Drafts

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

## Story 3.5: Prevent Duplicate Invoice Follow-Up Drafts

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
