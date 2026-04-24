# Holden Capital GitHub Standards

This document defines the default GitHub execution model for Holden Capital repositories.

Use it alongside `governance/enterprise-development-standards.md`.

## Purpose

These standards make GitHub the reliable execution surface for agent work.

They exist so issues, branches, and pull requests are:

- implementation-ready
- reviewable
- scoped
- auditable

## GitHub Issues Standard

GitHub issues are the primary work surface.

### Epic Standard

Every epic should contain:

- goal
- strategic context
- scope
- story list
- implementation order
- acceptance criteria
- constraints
- dependencies
- risks
- validation approach

Epic issues should be detailed enough that they remain useful even if repo planning artifacts drift or move.

### Story Standard

Every story should contain:

- user story
- parent epic
- scoped change list
- constraints
- affected nodes or files
- acceptance criteria
- validation checklist
- implementation notes

Story issues must be detailed enough that an implementation agent can start from the issue itself.

## Branching Standard

Use this branch model by default:

- `agent/story-{id}-{slug}`
- `fix/{slug}`
- `docs/{slug}`
- `chore/{slug}`
- `spike/{slug}` for short-lived exploration that will not ship unreviewed

Rules:

- keep one implementation concern per branch
- do not commit directly to `main`
- keep branches short-lived
- prefer story-sized or smaller PRs
- use PRs to merge into `main`
- do not use long-lived epic branches as the default operating model

## Promotion Standard

Default promotion flow:

`branch -> main`

Most work should land as:

- `agent/story-* -> main`
- `fix/* -> main`
- `docs/* -> main`
- `chore/* -> main`

Epics remain planning and coordination containers in GitHub, not mandatory branch layers.

For larger efforts:

- break the epic into small mergeable stories
- merge each validated story to `main`
- use feature flags, draft states, or disabled workflows when partial work must stay non-operational

These still require PR review.

## Pull Request Standard

Every PR must state:

- what changed
- why it changed
- which issue it serves
- which contracts changed
- how it was validated
- what remains risky or unresolved

PRs must not mix unrelated planning, workflow, and governance changes.

## Pull Request Review Standard

Reviewers should check:

- issue scope was actually followed
- acceptance criteria are covered
- validation is explicit and repeatable
- risk is disclosed honestly
- no secrets or runtime data were committed
- related contracts and docs stayed in sync

## Template Enforcement Standard

Repo `.github` templates should reinforce this model:

- epic issue templates must ask for sequence, risk, and validation
- story issue templates must ask for constraints and repeatable validation
- PR templates must ask for scope, validation, and unresolved risk

## Adoption In This Repo

In `holden-capital-agentic-workflows`, these GitHub standards are applied through:

- [.github/ISSUE_TEMPLATE/epic-issue.md](/home/dank/Projects/holden-capital-agentic-workflows/.github/ISSUE_TEMPLATE/epic-issue.md)
- [.github/ISSUE_TEMPLATE/story-issue.md](/home/dank/Projects/holden-capital-agentic-workflows/.github/ISSUE_TEMPLATE/story-issue.md)
- [.github/pull_request_template.md](/home/dank/Projects/holden-capital-agentic-workflows/.github/pull_request_template.md)
