---
name: holden-github-cli-ops
description: Use when work involves GitHub issues, pull requests, labels, comments, or repo metadata for Holden Capital repos. Prefer the GitHub CLI (`gh`) over MCP or browser workflows, and follow Holden GitHub and tooling standards.
---

# Holden GitHub CLI Ops

Use this skill for GitHub execution work in Holden Capital repositories.

## Load First

Read:

- `governance/github-standards.md`
- `governance/agent-tooling-standards.md`

## Default Approach

Use `gh` as the primary tool for:

- creating and editing issues
- creating and editing pull requests
- adding comments
- managing labels and milestones
- checking workflow runs when needed

Prefer structured output when possible, for example:

```bash
gh issue view 12 --json title,body,labels,assignees
gh pr view 34 --json title,body,files,statusCheckRollup
```

## Working Rules

- keep issue bodies self-sufficient
- do not rely on stale repo docs when updating issue content
- align issue and PR language with `governance/github-standards.md`
- prefer editing existing issues over scattering context across comments when the body is wrong

## Typical Commands

```bash
gh issue create
gh issue edit
gh issue comment
gh pr create
gh pr edit
gh pr comment
gh label list
gh label create
```

## Avoid

- defaulting to MCP when `gh` can do the job
- leaving issue bodies thin and pushing the real spec into comments
- mixing unrelated GitHub admin work into an implementation PR
