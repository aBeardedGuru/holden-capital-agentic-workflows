# Holden Capital Enterprise Development Standards

This document adapts the durable governance and delivery standards from `holden-capital-mono` for Holden Capital repositories.

It is the enterprise default for AI-assisted development unless a repo-specific rule explicitly tightens it.

## Purpose

These standards exist to keep Holden Capital delivery:

- issue-driven
- contract-first
- reviewable
- auditable
- safe for production-facing automation
- trunk-based by default

## Operating Model

Holden Capital development uses:

- `ho-pe` as the primary repo steward and orchestration agent
- BMAD agents as specialist roles
- OpenAI models as the runtime layer
- GitHub issues and pull requests as the execution surface
- git worktrees as the recommended local parallel-development model
- CLI-first tooling, with `gh` preferred over MCP for GitHub work

The role taxonomy is BMAD plus `ho-pe`, not model-family specific.

## Planning Is The Source Of Truth

Before implementation starts, the working agent must read the relevant planning and operating context:

1. epic or story issue
2. repo `AGENTS.md`
3. repo `INSTRUCTIONS.md`
4. relevant node-level instructions
5. relevant operating docs and schemas

If implementation behavior conflicts with the issue or docs, the agent must resolve the contract first instead of coding through ambiguity.

## Standard Role Model

| Role | Purpose | Expected Authority |
| --- | --- | --- |
| `ho-pe` | Repo steward, orchestrator, standards owner | ADMIN |
| BMAD PM / Architect | Planning, decomposition, architecture, contract design | MAINTAINER |
| BMAD Dev | Story implementation | DEVELOPER |
| BMAD QA / Reviewer / Tech Writer | Validation, review, clarity, readiness checks | REVIEWER |

## Permission Standards

### ADMIN

- May modify governance files and repo structure
- May create epics, stories, branches, PRs, and standards
- May approve cross-node or cross-project direction
- Must not bypass review for consequential changes

### MAINTAINER

- May implement planning and technical changes in scope
- May create branches and PRs
- May lead story execution and contract updates
- Must not casually rewrite repo governance

### DEVELOPER

- Must work from a defined story or equivalent task
- Must keep changes within story scope plus directly required docs/contracts
- Must not rewrite governance or widen scope without explicit approval

### REVIEWER

- Must validate behavior, coverage, and standards compliance
- Must not treat review as implementation unless explicitly reassigned

## GitHub Execution Standard

Follow `governance/github-standards.md` for issue structure, branch naming, promotion flow, and PR expectations.

## Git Operations Standard

Follow `governance/git-ops-standards.md` for local branch handling, worktree usage, and parallel agent coordination on shared machines.

## Agent Tooling Standard

Follow `governance/agent-tooling-standards.md` for CLI, API, and integration tool preference.

## Contract-First Delivery Standard

When changing workflow automation, agents must keep these surfaces in sync:

`planning -> docs -> automation`

Inside automation:

`schemas -> prompts -> scripts -> workflows -> samples`

If one layer changes, the agent must verify adjacent layers in the same change.

## Universal Quality Gates

These gates apply to all Holden Capital repos, adapted to the repo’s actual artifact types.

### Required For All Changes

- acceptance criteria addressed
- docs and contracts updated when behavior changes
- no secrets committed
- runtime or generated operational state not committed
- changed files validate in their native format
- review notes are explicit when risk remains

### Required For Automation Or Code Changes

- relevant JSON validates
- scripts pass syntax checks
- tests run where tests exist
- changed behavior has executable or repeatable validation
- production-affecting actions remain behind approval gates unless the issue explicitly changes that rule

### Coverage Standard

For code-bearing modules with an existing test harness, target `>=90%` coverage unless a stricter repo-local rule applies.

Docs-only, schema-only, and blueprint-only changes do not require artificial coverage padding, but they do require direct validation.

## Safety Standards For Financial Automation

- no silent posting to accounting systems
- no unapproved external reminders
- no secrets in repo, workflow JSON, or job payloads
- preserve traceability from source document to final decision
- runtime data stays local and ignored
- review queue is preferred over low-confidence automation

## Escalation Standard

Escalate before proceeding if:

- the issue is underspecified
- the contract and implementation disagree
- the change crosses node boundaries without clear approval
- the work would alter governance, approval gates, or financial safety guarantees

## Adoption In This Repo

In `holden-capital-agentic-workflows`, these enterprise standards are applied through:

- [AGENTS.md](/home/dank/Projects/holden-capital-agentic-workflows/AGENTS.md)
- [INSTRUCTIONS.md](/home/dank/Projects/holden-capital-agentic-workflows/INSTRUCTIONS.md)
- [PROJECT_CONTEXT.md](/home/dank/Projects/holden-capital-agentic-workflows/PROJECT_CONTEXT.md)
- [github-standards.md](/home/dank/Projects/holden-capital-agentic-workflows/governance/github-standards.md)
- [git-ops-standards.md](/home/dank/Projects/holden-capital-agentic-workflows/governance/git-ops-standards.md)
- [agent-tooling-standards.md](/home/dank/Projects/holden-capital-agentic-workflows/governance/agent-tooling-standards.md)
- `.github` issue and PR templates
