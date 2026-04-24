# Holden Capital Agent Tooling Standards

This document defines the preferred tooling order for agents working in Holden Capital repositories.

## Purpose

These standards keep agent execution:

- deterministic
- scriptable
- reviewable
- easy to repeat on local machines and CI

## Default Tool Preference Order

Use tools in this order unless the task clearly requires a different path:

1. local CLI tools
2. provider CLIs
3. direct APIs
4. browser or MCP-style integrations only as fallback

## GitHub Standard

For GitHub operations, prefer `gh` over MCP integrations.

Use `gh` for:

- issue creation and editing
- pull request creation and editing
- comments and status checks
- labels, milestones, and repo metadata
- workflow run inspection when relevant

Reasons:

- reproducible command history
- structured JSON output when needed
- easy automation in scripts and skills
- lower ambiguity than UI-driven tooling

## General CLI Standard

Prefer established CLI tools over ad hoc manual workflows.

Examples:

- `git` for source control
- `gh` for GitHub
- `rg` for search
- `jq` for JSON transforms
- `python3 -m json.tool` for JSON validation
- provider CLIs when they are stable and already part of the workflow

When CLI output can be structured, prefer structured output modes such as JSON.

## API Standard

Use direct APIs when:

- no reliable CLI exists
- the CLI does not expose the required capability
- the task needs scripted bulk behavior better handled in code

When using APIs:

- prefer official APIs
- keep secrets out of repo files
- use the smallest required permission scope
- document any non-obvious API assumptions in the related change

## MCP And Browser Integration Standard

Do not default to MCP or browser-driven integrations when a CLI or direct API path is available.

Use them only when:

- the task genuinely depends on interactive UI state
- there is no equivalent CLI or API path
- the user explicitly asks for that route

## Adoption In This Repo

In `holden-capital-agentic-workflows`, agents should generally prefer:

- `git` and `git worktree`
- `gh`
- local shell tools
- direct provider APIs only when CLI paths are insufficient
