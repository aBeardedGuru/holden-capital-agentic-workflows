# INSTRUCTIONS.md - Holden Capital Agentic Workflows Operating Guide

This file tells agents how to work in this repo efficiently and consistently.

## Quick Start

### Step 1: Load Context

Read these in order:

1. `AGENTS.md`
2. `governance/enterprise-development-standards.md`
3. `governance/github-standards.md` for issue, branch, or PR work
4. `governance/git-ops-standards.md` for local branch and worktree setup
5. `governance/agent-tooling-standards.md` for CLI/API tool choice
6. `PROJECT_CONTEXT.md`
7. Node-local `AGENTS.md` and `INSTRUCTIONS.md` for `governance/`, `skills/`, `docs/`, `planning/`, or `automation/`
8. Relevant docs in `docs/`
9. Relevant planning artifacts in `planning/`

### Step 2: Identify Work Type

Work in this repo usually falls into one of these buckets:

- planning and decomposition
- skill-driven repeated workflow execution
- prompt/schema contract work
- local worker script work
- n8n blueprint work
- issue/PR process maintenance
- documentation refinement

Typical role selection:

- BMAD PM for PRDs, epics, stories, and issue planning
- BMAD Architect for workflow contracts, schemas, structure, and cross-node design
- BMAD Dev for implementation work in prompts, scripts, schemas, and workflows
- BMAD Tech Writer for documentation cleanup and agent-facing clarity
- ho-pe for repo stewardship, orchestration, and cross-cutting changes

### Step 3: Follow The Contract Chain

For finance automation, these layers depend on each other:

`planning -> docs -> automation`

Inside `automation/`, the dependency chain is:

`schemas -> prompts -> scripts -> workflows -> samples`

If you change something lower in the chain, check whether higher-level docs or sibling contracts must also change.

## Repo Workflow

### Issues

Use GitHub issues as the execution surface:

- Epic issues contain the full epic details
- Story issues should contain implementable scope and acceptance criteria
- Ad hoc maintenance issues should still define expected outcome and validation

### Branching

Use the Holden Capital trunk-based branch pattern:

- `agent/story-{id}-{slug}` for story implementation
- `docs/{slug}` for documentation-only work
- `fix/{slug}` for bug fixes
- `chore/{slug}` for maintenance work

The branch naming is model-agnostic. OpenAI is the runtime. BMAD or `ho-pe` is the working role.

### Local Git Ops

When parallel agent work is happening on the same machine, prefer one git worktree per active branch.

Do not have multiple active agents share one dirty checkout.

### Tool Choice

Prefer:

- `gh` over MCP for GitHub work
- local CLI tools over browser-driven workflows
- direct APIs only when CLI paths are insufficient

### Pull Requests

PRs should include:

- what changed
- why it changed
- which issue/story it serves
- which contracts changed
- how it was validated

Do not open vague PRs that mix unrelated planning, workflow, and script changes.

### Promotion Model

Default promotion flow:

`branch -> main`

Most work should merge straight to `main` through small PRs. Epics should usually organize issues and sequencing, not act as long-lived branch layers.

## Quality Gates

Before marking work complete:

- issue acceptance criteria are actually covered
- docs still match actual repo behavior
- schema examples still validate conceptually
- prompts still reflect schema/output expectations
- scripts still point at the right paths and contracts
- workflow blueprints do not embed secrets
- runtime files are not committed
- risks and unresolved items are called out explicitly

## Finance Automation Principles

1. Review-first before automation-first.
2. No silent posting into accounting systems.
3. No unapproved external reminders.
4. Preserve auditability from source document to final decision.
5. Prefer explicit contracts over agent memory.

## Directory Guide

- `docs/`: business and implementation documentation
- `planning/`: PRD and epic breakdowns
- `automation/`: prompts, schemas, scripts, workflows, and samples
- `skills/`: repo-local Codex skills for repeated workflows
- `governance/`: enterprise and repo-level standards
- `.github/`: issue and PR process templates

## When In Doubt

- update the docs first if the problem is conceptual
- update planning if the problem is scope or sequencing
- update the automation contract first if the problem is technical
- prefer story-sized changes over repo-wide rewrites
- escalate before changing governance, approval gates, or financial safety rules
