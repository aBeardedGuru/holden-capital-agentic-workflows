---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - planning/prd-financial-operations-automation.md
  - planning/epics/index.md
  - planning/epics/overview.md
  - planning/epics/epic-list.md
  - planning/epics/requirements-inventory.md
  - planning/epics/epic-1-finance-intake-and-review-foundation.md
  - planning/epics/epic-2-expense-intake-and-categorization.md
  - planning/epics/epic-3-invoice-collection-queue.md
  - planning/epics/epic-4-weekly-financial-snapshot.md
  - PROJECT_CONTEXT.md
workflowType: 'architecture'
project_name: 'holden-capital-agentic-workflows'
user_name: 'dank'
date: '2026-04-26'
lastStep: 8
status: 'complete'
completedAt: '2026-04-26'
---

# Architecture Decision Document

This document defines the technical architecture for the finance automation scope in this repo, with OpenRouter-backed model inference inside n8n as the runtime baseline.

## Project Context Analysis

### Requirements Overview

Functional scope is concentrated in four workflow groups:
- Intake and review foundation (Drive ingest, extraction/classification, Sheets writes, routing, audit)
- Expense intake and categorization
- Invoice collection queue (status + reminder drafts, no send)
- Weekly financial snapshot generation

Non-functional constraints driving architecture:
- No live accounting posting or external reminders without explicit approval
- No secrets or credentials in repo artifacts
- Full traceability from source file/record to output + review decision
- Duplicate detection and idempotency at flow boundaries
- Deterministic structured output from model inference

Scale profile:
- Complexity level: medium
- Primary domain: workflow automation + contract-driven data processing
- Core data surfaces: Google Drive, Google Sheets, runtime packet/output storage

### Technical Constraints and Dependencies

- Orchestration platform: n8n
- Model runtime: OpenRouter models via n8n OpenRouter chat model node
- Contract validation: JSON Schema-based contracts (`automation/schemas`)
- Review and ledger surface: Google Sheets tabs (`Transactions`, `Documents`, `Review Queue`, `Run Log`)
- Source intake and file lifecycle: Google Drive folder contract

### Cross-Cutting Concerns

- Contract-first compatibility across `planning -> docs -> automation`
- Approval gates before any external side effect
- Idempotency and duplicate handling across all flows
- Confidence threshold routing to review queue
- Structured run logging and machine-readable failure reasons

## Architecture Starter Recommendation

Recommended architecture style:
- Event-driven workflow orchestration (n8n)
- Contract-first extraction and transformation boundaries
- Human-in-the-loop review-first decision pipeline

Why this starter:
- Matches existing repo artifacts and governance standards
- Minimizes operational sprawl (single orchestration surface)
- Supports model/provider swaps while preserving output contracts

## Architecture Decisions

### ADR-01: Orchestration and Execution Surface
Decision:
- Use n8n as the single orchestration surface for intake, classification, routing, and logging.

Rationale:
- Existing flow artifacts and operational model are already n8n-centered.
- Keeps side effects (Drive/Sheets) in one control plane.

Implications:
- Every production-facing automation change requires workflow JSON + contract sync.

### ADR-02: Model Runtime Boundary
Decision:
- Use OpenRouter-backed models from n8n for classification and extraction.

Rationale:
- Centralized runtime configuration and model switching.
- Eliminates local worker dependency for core flow execution.

Implications:
- Model prompts and parser logic must enforce deterministic JSON output.
- Credential management is delegated to n8n credential store.

### ADR-03: Canonical Contract Chain
Decision:
- Treat `planning -> docs -> automation` as mandatory sync chain.
- Inside automation use: `schemas -> prompts -> workflows -> samples`.

Rationale:
- Prevents behavioral drift and hidden assumptions.

Implications:
- Any schema change requires downstream prompt/workflow/sample verification.

### ADR-04: Data and Review Surfaces
Decision:
- Google Sheets is the first system of record and review queue for MVP.
- Google Drive is the canonical source-file lifecycle surface.

Rationale:
- Fast operator visibility and low-friction review loop.

Implications:
- Sheet/tab contracts must stay stable to avoid workflow breakage.

### ADR-05: Safety Envelope
Decision:
- Enforce dry-run and draft modes for all financially sensitive actions.
- Keep external reminders and accounting posts behind explicit approval.

Rationale:
- Aligns with PRD and enterprise finance safety standards.

Implications:
- Workflow nodes that could trigger external side effects remain disabled or gated in MVP.

### ADR-06: Traceability and Idempotency
Decision:
- Require idempotency keys and duplicate decision logging in all flows.
- Capture audit metadata in `Documents` and `Run Log` for every run.

Rationale:
- Financial workflow trust depends on explainability and replay safety.

Implications:
- New flows must implement consistent key generation and duplicate handling policy.

## Technology Stack and Interfaces

### Core Stack
- n8n for orchestration
- OpenRouter model node for extraction/classification
- Google Drive nodes for intake and state transitions
- Google Sheets nodes for ledger/review/run logging
- JSON Schema contracts under `automation/schemas`
- Markdown docs/planning for architecture and operating contracts

### Interface Contracts
- Input: Drive file metadata + bounded content payload + workflow context
- Output: `finance-extraction.schema.json`-compatible JSON
- Routing: confidence and validation checks determine processed/review/error outcome
- Logging: all runs append `Run Log`; all uncertain/failed items append `Review Queue`

## Implementation Patterns and Consistency Rules

### Naming Patterns
- Flow names: `snake_case` (example: `finance_document_intake`)
- IDs/keys in JSON: `snake_case`
- Sheet status enums: fixed lowercase enum sets (`pending`, `approved`, `corrected`, `rejected`, `needs_more_info`)

### Validation Patterns
- Validate required config IDs before side effects.
- Validate model output against schema before writing ledger rows.
- On schema/parse failure, write failure metadata and route to error/review.

### Confidence and Review Routing
- Define one threshold field (`confidenceReviewThreshold`) per flow config node.
- Any missing required field or low confidence routes to `Review Queue`.

### Error Handling
- Fail closed for external actions.
- Emit machine-readable reason codes in run metadata.
- Preserve source file; do not delete source documents.

### Prompt/Model Patterns
- Explicitly constrain model output to strict JSON shape.
- Keep prompts deterministic and contract-specific.
- Record model choice/version in run metadata where possible.

## Project Structure and Boundaries

### Architecture Mapping by Epic
- Epic 1 (intake/review foundation):
  - `docs/finance-document-intake.md`
  - `docs/finance-ledger-operating-contract.md`
  - `automation/schemas/finance-job.schema.json`
  - `automation/schemas/finance-extraction.schema.json`
  - `automation/workflows/google-drive-download-for-processing.json`
- Epic 2 (expense categorization):
  - new expense contract docs + workflow extensions under `automation/workflows` and `docs/`
- Epic 3 (invoice queue):
  - invoice status/reminder draft contracts + workflow module(s)
- Epic 4 (weekly snapshot):
  - snapshot input/output contracts + summary workflow module(s)

### Repo Boundary Rules
- `planning/` defines scope and acceptance targets.
- `docs/` defines operating contracts.
- `automation/` contains executable contracts and workflow artifacts.
- `runtime/` contains local operational data only and is never committed.

### Recommended Additional Architecture Artifacts
- `docs/flow-expense-intake-categorization.md`
- `docs/flow-invoice-collection-queue.md`
- `docs/flow-weekly-financial-snapshot.md`
- `docs/financial-event-schema.md`
- `docs/financial-automation-readiness-checklist.md`

## Validation Results

### Coherence Validation
- Planning and epic structure align with review-first and no-autopost constraints.
- OpenRouter-in-n8n direction is now aligned in PRD + requirements inventory + Epic 1 runtime story.

### Requirements Coverage
- FR1-FR21 have epic coverage mapping in `planning/epics/requirements-inventory.md`.
- NFR safety/privacy/traceability constraints are reflected in architecture decisions.

### Implementation Readiness
- Foundation contracts for intake exist and are executable.
- Remaining work is flow-specific contract expansion for Epics 2-4.

### Gaps to Resolve Next
- Finalize normalized input contracts for invoice and weekly snapshot flows.
- Define model fallback policy (provider/model routing and retry strategy).
- Standardize failure reason code taxonomy across all flows.

## Handoff Guidance

This architecture is ready to guide story-level implementation.

Recommended next sequence:
1. Publish/approve this architecture artifact.
2. Create story issues for Epic 2 contract files and workflow slices.
3. Add schema-level validation checkpoints inside each new workflow segment.
4. Run checkpoint review before enabling any new side-effecting workflow nodes.

Invoke `bmad-help` at any point to select the next BMAD workflow.
