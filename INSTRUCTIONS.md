# INSTRUCTIONS.md - Holden Capital Agentic Workflows Operating Guide

This file tells agents how to work in this repo efficiently and consistently.

## Quick Start

### Step 1: Load Context

Read these in order:

1. `AGENTS.md`
2. `PROJECT_CONTEXT.md`
3. Node-local `AGENTS.md` and `INSTRUCTIONS.md` for touched directories
4. Relevant docs in `docs/`
5. Relevant planning artifacts in `_bmad-output/planning-artifacts/`

### Step 2: Identify Work Type

Work in this repo usually falls into one of these buckets:

- planning and decomposition
- prompt/schema contract work
- local worker script work
- n8n blueprint work
- issue/PR process maintenance
- documentation refinement

### Step 3: Follow The Contract Chain

For finance automation, these layers depend on each other:

`docs -> prompts -> schemas -> scripts -> workflows -> samples/tests`

If you change something lower in the chain, check whether higher-level docs or sibling contracts must also change.

## Repo Workflow

### Issues

Use GitHub issues as the execution surface:

- Epic issues contain the full epic details
- Story issues should contain implementable scope and acceptance criteria
- Ad hoc maintenance issues should still define expected outcome and validation

### Branching

Use the mono repo pattern where it helps:

- `feature/epic-{id}-{slug}` for multi-story work
- `agent/story-{id}-{slug}` for story implementation
- `docs/{slug}` for documentation-only work
- `fix/{slug}` for bug fixes

### Pull Requests

PRs should include:

- what changed
- why it changed
- which issue/story it serves
- which contracts changed
- how it was validated

Do not open vague PRs that mix unrelated planning, workflow, and script changes.

## Quality Gates

Before marking work complete:

- docs still match actual repo behavior
- schema examples still validate conceptually
- prompts still reflect schema/output expectations
- scripts still point at the right paths and contracts
- workflow blueprints do not embed secrets
- runtime files are not committed

## Finance Automation Principles

1. Review-first before automation-first.
2. No silent posting into accounting systems.
3. No unapproved external reminders.
4. Preserve auditability from source document to final decision.
5. Prefer explicit contracts over agent memory.

## Directory Guide

- `docs/`: business and implementation documentation
- `prompts/`: extraction/classification prompts for Codex
- `samples/`: sample fixtures and example records
- `schemas/`: machine-readable contract definitions
- `scripts/`: local worker and helper scripts
- `workflows/`: n8n blueprint exports and workflow definitions
- `.github/`: issue and PR process templates
- `_bmad-output/`: planning artifacts and breakdowns
- `tests/`: validation and regression scaffolding

## When In Doubt

- update the docs first if the problem is conceptual
- update the schema first if the problem is contractual
- update the script or workflow only after the contract is clear
- prefer story-sized changes over repo-wide rewrites
