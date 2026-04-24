# Holden Capital Git Ops Standards

This document defines the default git operating model for Holden Capital repositories.

Use it with:

- `governance/enterprise-development-standards.md`
- `governance/github-standards.md`

## Purpose

These standards exist to keep local git work:

- safe for parallel agent execution
- aligned with trunk-based delivery
- low-friction on a shared machine
- resistant to branch and workspace collisions

## Default Local Development Model

Use `git worktree` as the default approach when multiple agents or parallel tasks need to operate in the same repository on the same machine.

Why:

- each branch gets an isolated working directory
- agents do not stomp on each other’s checkout state
- branch switching in one task does not disrupt another task
- it is lighter and cleaner than cloning the repo repeatedly

## Recommended Worktree Layout

Keep the main repository checkout as the coordination root, and create sibling worktrees for active tasks.

Example:

```text
/Projects/holden-capital-agentic-workflows              # coordination root
/Projects/holden-capital-agentic-workflows-wt-story-1-2
/Projects/holden-capital-agentic-workflows-wt-fix-ledger-export
/Projects/holden-capital-agentic-workflows-wt-docs-governance
```

## Worktree Naming Standard

Use names that clearly map to the branch:

- `*-wt-story-{id}-{slug}`
- `*-wt-fix-{slug}`
- `*-wt-docs-{slug}`
- `*-wt-chore-{slug}`

The branch name and worktree name should be easy to correlate.

## Recommended Commands

Create a worktree for a story branch:

```bash
git fetch origin
git worktree add ../holden-capital-agentic-workflows-wt-story-1-2 -b agent/story-1.2-ledger-contract origin/main
```

Create a worktree for a fix branch:

```bash
git fetch origin
git worktree add ../holden-capital-agentic-workflows-wt-fix-schema fix/schema-cleanup origin/main
```

List active worktrees:

```bash
git worktree list
```

Remove a finished worktree:

```bash
git worktree remove ../holden-capital-agentic-workflows-wt-story-1-2
git branch -d agent/story-1.2-ledger-contract
```

Prune stale metadata:

```bash
git worktree prune
```

## Parallel Development Rules

When multiple agents are active at once:

- assign one branch and one worktree per agent task
- do not share a worktree across active agents
- do not reuse a dirty worktree for a different task
- sync from `origin/main` before starting a new branch
- merge small PRs frequently to reduce drift

## Trunk-Based Guidance

Worktrees support trunk-based development best when:

- each worktree is tied to one small branch
- each branch is intended for a small PR into `main`
- long-lived branch stacks are avoided

Epics should coordinate issue sequencing, not require one persistent worktree for the entire epic.

## Cleanup Standard

After a branch is merged or abandoned:

- remove the associated worktree
- delete the local branch if it is no longer needed
- prune stale worktree references

Do not let old worktrees accumulate indefinitely.

## When Not To Use A Worktree

A separate worktree is usually unnecessary when:

- only one agent is active
- the change is trivial and short-lived
- the task is read-only review or documentation lookup

Even then, worktrees are still acceptable if they reduce confusion.

## Safety Notes

- never run destructive cleanup commands against the wrong worktree path
- confirm the branch and path before removing a worktree
- avoid putting runtime or secret files into shared long-lived worktree folders

## Adoption In This Repo

In `holden-capital-agentic-workflows`, worktrees are the recommended git-ops model for parallel agent development on the same machine.
