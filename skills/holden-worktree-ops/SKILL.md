---
name: holden-worktree-ops
description: Use when starting, coordinating, or cleaning up parallel branch work in a Holden Capital repo on the same machine. Create one git worktree per active branch and follow trunk-based workflow rules.
---

# Holden Worktree Ops

Use this skill when multiple agents or parallel tasks need isolated local checkouts in the same repository.

## Load First

Read:

- `governance/git-ops-standards.md`
- `governance/github-standards.md`

## Default Approach

Use one worktree per active branch.

Keep the main checkout as the coordination root, then add sibling worktrees for active tasks.

## Typical Flow

1. fetch `origin/main`
2. create a new short-lived branch
3. create a worktree for that branch
4. do the work in that worktree only
5. merge through PR to `main`
6. remove the worktree and delete the local branch

## Example Commands

```bash
git fetch origin
git worktree add ../holden-capital-agentic-workflows-wt-story-1-2 -b agent/story-1.2-ledger-contract origin/main
git worktree list
git worktree remove ../holden-capital-agentic-workflows-wt-story-1-2
git branch -d agent/story-1.2-ledger-contract
git worktree prune
```

## Working Rules

- do not share one dirty checkout across active agents
- do not reuse a task worktree for unrelated work
- keep branch names aligned with repo branch standards
- prefer small PRs into `main`

## Avoid

- long-lived epic worktrees as the default pattern
- parallel agents on the same checkout
- forgetting to prune or remove stale worktrees
