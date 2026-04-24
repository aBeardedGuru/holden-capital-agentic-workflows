# AGENTS.md - Holden Capital Agentic Workflows Access Control

Defines which agents can work in this repo and how they should respect directory boundaries.

## Repository Purpose

This repo is the AI-first planning, documentation, and automation workspace for Holden Capital finance automation.

It is not the production application monorepo. It is the place where agents:

- define finance workflow contracts
- document epics, stories, and operating rules
- build and validate n8n workflow support artifacts

This repo adopts the Holden Capital enterprise governance baseline defined in [governance/enterprise-development-standards.md](/home/dank/Projects/holden-capital-agentic-workflows/governance/enterprise-development-standards.md).

## Operating Model

This repo uses:

- `ho-pe` as the custom primary orchestrator and repo steward
- BMAD agents as the specialist working roles
- OpenAI models as the runtime/model layer

The role taxonomy should follow BMAD and your custom `ho-pe` agent, not Claude model names.

## Access Matrix

| Agent | Role | Permission | Primary Use |
| --- | --- | --- | --- |
| ho-pe | Repo steward / orchestrator | ADMIN | Defines structure, approves standards, creates epics/stories/issues, coordinates BMAD agents |
| BMAD PM | Product planning specialist | MAINTAINER | PRDs, requirements, epics, issue shaping |
| BMAD Architect | System design specialist | MAINTAINER | Architecture, contracts, workflow design, repo structure |
| BMAD Dev | Implementation specialist | DEVELOPER | Docs, schemas, prompts, scripts, workflows, story-scoped changes |
| BMAD Tech Writer / QA / Reviewer | Validation specialist | REVIEWER | Reviews docs, contracts, workflow behavior, and readiness |

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
| `/planning` | PRD, epics, and future story planning | PM, architect |
| `/automation` | Prompts, schemas, scripts, workflows, and samples | Architect, dev |
| `/governance` | Enterprise standards and repo governance baselines | ho-pe, architect |
| `/.github` | Issue/PR process and repo automation metadata | Admin, maintainer |

## Access Rules

### Rule 1: Contract-First Changes
If a change affects `automation/`, the agent must update the affected contract docs in `docs/` or `planning/` in the same change.

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

### Rule 6: Enterprise Standards Apply By Default
If repo-local guidance is silent, agents should follow the Holden Capital enterprise standards from `governance/enterprise-development-standards.md`.

### Rule 7: Prefer Worktrees For Parallel Agent Work
If multiple agents are active on the same machine in this repo, prefer separate git worktrees instead of sharing one checkout.

## Git and GitHub Working Model

This repo follows the Holden Capital enterprise GitHub model adapted from `holden-capital-mono`:

- Epics live as GitHub issues
- Stories should become GitHub issues under those epics
- Story or small task branches are the normal implementation unit
- PRs normally land directly on `main`
- PRs should describe scope, contracts changed, and validation performed

The detailed GitHub execution rules live in [governance/github-standards.md](/home/dank/Projects/holden-capital-agentic-workflows/governance/github-standards.md).
The detailed git operating rules live in [governance/git-ops-standards.md](/home/dank/Projects/holden-capital-agentic-workflows/governance/git-ops-standards.md).

Recommended branch names:

- `agent/story-{id}-{slug}`
- `fix/{slug}`
- `docs/{slug}`
- `chore/{slug}`

If a BMAD agent is acting on a story, the branch should usually use `agent/story-{id}-{slug}`. The runtime model is OpenAI; the working role is BMAD.

## Before Starting Work

1. Read this file.
2. Read [INSTRUCTIONS.md](/home/dank/Projects/holden-capital-agentic-workflows/INSTRUCTIONS.md).
3. Read the node-local `AGENTS.md` and `INSTRUCTIONS.md` for `governance/`, `docs/`, `planning/`, or `automation/` as needed.
4. Confirm whether you are working from an epic/story issue, a planning artifact, or an ad hoc maintenance task.
