# Epic 5: Unified Operator Front And Cross-Repo Bridge

Enable the operator to run one daily finance-and-portfolio review loop from a single command surface with explicit contracts between planning artifacts and monorepo runtime surfaces.

## Story 5.1: Define Cross-Repo Boundary And Promotion Contract

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

## Story 5.2: Define Unified Operator UX Contract

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

## Story 5.3: Publish Bridge Event And Status Schema

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

## Story 5.4: Add Daily Close Workflow Runbook And Acceptance Checks

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
