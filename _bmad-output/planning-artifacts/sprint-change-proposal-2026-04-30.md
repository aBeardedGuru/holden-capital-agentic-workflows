---
workflow: bmad-correct-course
date: 2026-04-30
project: holden-capital-agentic-workflows
owner: John (BMAD PM)
mode: batch
status: approved
scopeClassification: major
---

# Sprint Change Proposal

## 1. Issue Summary

### Trigger

- Triggering issue: architecture/design review request for `holden-capital-mono` due repo divergence and lack of one working application for STR business operations.
- Trigger category: strategic pivot and execution fragmentation.

### Core Problem Statement

Holden artifacts are producing value in separate lanes (property intelligence, finance workflow planning, infra, communications), but there is no enforced product spine that delivers one daily operator workflow end-to-end.

### Evidence

- Finance automation PRD/epics are housed in `holden-capital-agentic-workflows/planning/`.
- Most runnable app code/UI is in `holden-capital-mono/real-estate-app`.
- Monorepo real-estate app planning is still anchored to parsing and property intelligence workstreams.
- Dedicated finance UX contract is absent.

## 2. Impact Analysis

### Epic Impact

- Current finance epics (1-4) remain valid but incomplete as a product without runtime/UI integration ownership.
- Real-estate-app epics include many completed units but no single explicit epic guarantees "STR operations command center" closure.

### Story Impact

- Existing story-level work can continue for maintenance, but new feature stories should be gated until unification bridge stories exist.
- A new unification story set is required to map finance contracts into monorepo surfaces.

### Artifact Conflicts

- PRD conflict: local finance PRD assumes review-first flow surfaces, monorepo app artifacts emphasize parsing/property tooling.
- Architecture conflict: local architecture defines n8n + Sheets + Drive workflow system; monorepo architecture emphasizes parsing microservice and property analysis.
- UX conflict: no canonical operator UX joining finance queue + portfolio decisions.

### Technical Impact

- Requires cross-repo API contract definitions.
- Requires shared event schema/versioning for finance and property updates.
- Requires one launchable “operator day flow” with measurable outcome.

## 3. Path Forward Evaluation

### Option 1: Direct Adjustment

- Viable: Yes
- Effort: Medium
- Risk: Medium
- Notes: Add bridge epic + resequence backlog; keep core architecture.

### Option 2: Potential Rollback

- Viable: No
- Effort: High
- Risk: High
- Notes: Rolling back completed epics would destroy momentum without solving integration ownership.

### Option 3: PRD MVP Review

- Viable: Yes
- Effort: Medium
- Risk: Low
- Notes: Narrow MVP to one “daily operator close loop” and defer peripheral enhancements.

### Recommended Path

**Selected approach: Hybrid (Option 1 + Option 3)**

Rationale:
- Preserve existing progress.
- Introduce a unification epic immediately.
- Tighten MVP around one executable operator loop before expanding features.

## 4. Detailed Change Proposals

### A. PRD Changes

#### Proposal A1

Artifact: `planning/prd-financial-operations-automation.md`
Section: MVP Scope

OLD:
- MVP defines three dry-run financial flows.

NEW:
- MVP defines three dry-run financial flows plus one explicit "Unified Operator Daily Close" path executed from a single command surface.

Rationale:
- Converts workflow outputs into a product experience.

#### Proposal A2

Artifact: `planning/prd-financial-operations-automation.md`
Section: Success Metrics

OLD:
- Time-reduction metrics for weekly/month-end prep.

NEW:
- Add system cohesion KPI: "Operator can execute intake-review-summary loop in one session without switching repositories or manual data stitching."

Rationale:
- Measures unification directly.

### B. Epic Changes

#### Proposal B1

Artifact: `planning/epics/epic-list.md`

OLD:
- Four finance epics.

NEW:
- Add Epic 5: Unified Operator Front (Bridge Epic).

Proposed Epic 5 scope:
1. Define cross-repo event and API contracts.
2. Define finance review surface inside monorepo app.
3. Add workflow status/exception visibility into command center.
4. Add end-to-end daily close runbook and acceptance tests.

Rationale:
- Assigns ownership for the currently missing seam.

#### Proposal B2

Artifact: `planning/epics/index.md`

OLD:
- Index terminates at Epic 4.

NEW:
- Include Epic 5 with story links and FR coverage mapping.

Rationale:
- Keeps planning discoverable and auditable.

### C. Architecture Changes

#### Proposal C1

Artifact: `_bmad-output/planning-artifacts/architecture.md`

OLD:
- Contract chain defined primarily inside this repo.

NEW:
- Add cross-repo boundary section:
  - "design authority" in this repo
  - "runtime authority" in monorepo
  - promotion gates for docs -> workflow JSON -> app integration.

Rationale:
- Eliminates ambiguity about where design ends and implementation begins.

### D. UX Changes

#### Proposal D1

Artifact to create: `docs/unified-operator-ux-contract.md`

OLD:
- No dedicated finance UX doc.

NEW:
- Define one operator workflow:
  - triage inbox documents
  - resolve review queue
  - view daily/weekly summary and exceptions
  - trigger follow-up drafts (approval-gated)

Rationale:
- Prevents backend-first drift without operator usability.

## 5. Implementation Handoff

### Scope Classification

**Major**: Fundamental replan and cross-repo coordination required.

### Handoff Recipients and Responsibilities

1. PM (John / bmad-agent-pm)
- Update PRD and epic definitions for unification.
- Create/refresh issue tree for bridge epic.

2. Architect (Winston / bmad-agent-architect)
- Define cross-repo contracts and release gates.
- Validate architecture boundary updates.

3. Dev (Amelia / bmad-agent-dev)
- Implement bridge stories in monorepo and workflow repo.
- Add integration validation artifacts.

4. Tech Writer (Paige / bmad-agent-tech-writer)
- Produce unified operator UX contract and runbook.

### Success Criteria

1. One documented and testable daily operator close path exists.
2. Bridge epic stories are created and sequenced with owners.
3. Cross-repo contracts are versioned and referenced by both repos.
4. First integrated flow runs without manual repo-to-repo stitching.

## 6. Checklist Execution Log

- 1.1 Trigger identified: [x] Done
- 1.2 Core problem defined: [x] Done
- 1.3 Evidence gathered: [x] Done
- 2.1-2.5 Epic impact assessed: [x] Done
- 3.1-3.4 Artifact conflicts assessed: [x] Done
- 4.1-4.4 Options assessed and selected: [x] Done
- 5.1-5.5 Proposal components complete: [x] Done
- 6.1-6.2 Final review complete: [x] Done
- 6.3 Explicit user approval: [x] Done
- 6.4 `sprint-status.yaml` update: [N/A] (file not present in this repo)
- 6.5 Handoff confirmation: [x] Done

## 7. Recommended Immediate Sequence (Next 7 Days)

1. Approve this proposal.
2. Add Epic 5 (Unified Operator Front) in `planning/epics/`.
3. Open one epic issue and first two story issues (bridge contract + UX contract).
4. Freeze new non-bridge feature work until story 5.1 and 5.2 are underway.
5. Review first end-to-end dry run in checkpoint.
