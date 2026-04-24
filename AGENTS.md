# AGENTS.md - Holden Capital Agentic Workflows Access Control

Defines which agents can work in this repo and how they should respect directory boundaries.

## Repository Purpose

This repo is the AI-first planning, documentation, schema, prompt, script, and workflow workspace for Holden Capital finance automation.

It is not the production application monorepo. It is the place where agents:

- define finance workflow contracts
- document epics, stories, and operating rules
- maintain prompts and schemas
- build workflow blueprints and local worker tooling

## Access Matrix

| Agent | Role | Permission | Primary Use |
| --- | --- | --- | --- |
| Primary OpenAI agent | Repo steward | ADMIN | Defines structure, approves standards, creates epics/stories/issues |
| OpenAI maintainer agent | Workflow maintainer | MAINTAINER | Implements docs, schemas, prompts, scripts, workflows, PRs |
| OpenAI developer agent | Feature developer | DEVELOPER | Implements assigned story-scoped changes |
| OpenAI reviewer agent | Reviewer | REVIEWER | Reviews docs, schemas, scripts, workflows, tests |

## Permission Model

### ADMIN
- Read and write all tracked files
- Create branches, issues, and PRs
- Modify AGENTS.md and INSTRUCTIONS.md
- Define repo structure and conventions

### MAINTAINER
- Read all tracked files
- Write feature files in assigned scope
- Create branches and PRs
- Update docs, schemas, prompts, scripts, and workflow blueprints
- Cannot change repo governance casually

### DEVELOPER
- Read all tracked files
- Write only within assigned story scope
- May update docs/tests required by the same story
- Cannot modify governance files without explicit direction

### REVIEWER
- Read all tracked files
- Run validation and review changes
- Cannot write code or docs as part of review-only work

## Node Ownership

| Path | Primary Concern | Typical Agent Mode |
| --- | --- | --- |
| `/docs` | Business, workflow, and planning documentation | PM, architect, tech writer |
| `/prompts` | Prompt contracts for Codex extraction/classification | Architect, dev |
| `/samples` | Test fixtures and sample payloads | Dev, reviewer |
| `/schemas` | JSON contracts between n8n and local tooling | Architect, dev |
| `/scripts` | Local worker and support scripts | Dev |
| `/workflows` | n8n blueprint JSON and workflow contracts | Architect, dev |
| `/.github` | Issue/PR process and repo automation metadata | Admin, maintainer |
| `/_bmad-output` | Planning artifacts and story decomposition | PM, architect |
| `/tests` | Validation harness and regression checks | Dev, reviewer |

## Access Rules

### Rule 1: Contract-First Changes
If a change affects `schemas/`, `prompts/`, `scripts/`, or `workflows/`, the agent must update the affected contract docs in `docs/` or `_bmad-output/` in the same change.

### Rule 2: No Silent Workflow Drift
If a workflow blueprint changes, the agent must verify whether prompts, schemas, samples, and docs also need updates.

### Rule 3: Story Scope Matters
DEVELOPER agents should work from a specific story issue or story file. Do not make cross-cutting changes without an explicit epic-level reason.

### Rule 4: Governance Is Restricted
Only ADMIN should make broad structural changes to:

- `AGENTS.md`
- `INSTRUCTIONS.md`
- `PROJECT_CONTEXT.md`
- `.github/ISSUE_TEMPLATE/*`
- `.github/pull_request_template.md`

### Rule 5: Runtime Data Stays Local
Agents must not commit runtime state, credentials, or generated operational data. `runtime/` is local-only.

## Git and GitHub Working Model

This repo follows the same useful pattern observed in `holden-capital-mono`:

- Epics live as GitHub issues
- Stories should become GitHub issues under those epics
- Story branches are the normal implementation unit
- PRs should describe story scope, contracts changed, and validation performed

Recommended branch names:

- `feature/epic-{id}-{slug}`
- `agent/story-{id}-{slug}`
- `fix/{slug}`
- `docs/{slug}`

## Before Starting Work

1. Read this file.
2. Read [INSTRUCTIONS.md](/home/dank/Projects/holden-capital-agentic-workflows/INSTRUCTIONS.md).
3. Read the node-local `AGENTS.md` and `INSTRUCTIONS.md` for the directories you will touch.
4. Confirm whether you are working from an epic/story issue, a planning artifact, or an ad hoc maintenance task.
