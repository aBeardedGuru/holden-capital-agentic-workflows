# INSTRUCTIONS.md - skills Node Workflow

## Purpose

Use this node for repo-local Codex skills that agents can load quickly for repeated Holden Capital workflows.

## Current Skills

- `holden-github-cli-ops`
  - for GitHub issue, PR, label, and comment work via `gh`
- `holden-worktree-ops`
  - for creating and cleaning up git worktrees for parallel local development
- `holden-finance-contract-sync`
  - for finance automation changes that must keep `planning -> docs -> automation` in sync

## Writing Standard

- keep metadata specific so the skill triggers cleanly
- keep the body procedural and short
- link to governance docs for durable policy
- move detailed examples or domain data into references only when needed

## Keep In Sync With

- `governance/enterprise-development-standards.md`
- `governance/github-standards.md`
- `governance/git-ops-standards.md`
- `governance/agent-tooling-standards.md`
- root `AGENTS.md`
- root `INSTRUCTIONS.md`
