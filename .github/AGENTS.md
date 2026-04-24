# AGENTS.md - .github Node Access Rules

This directory controls how agents interact with GitHub issues, pull requests, and repo workflow metadata.

## Scope

Files here shape how work enters and leaves the repo:

- issue templates
- PR template
- workflow metadata when present

## Rules

- Keep issue templates aligned with the repo's epic/story process.
- Keep PR templates aligned with contract-first finance workflow changes.
- Do not add automation that assumes secrets or hosted infrastructure without explicit approval.
- Prefer lightweight process over heavy ceremony.

## When Editing This Node

Agents must check whether changes here affect:

- root `INSTRUCTIONS.md`
- GitHub issue usage
- epic/story operating flow
