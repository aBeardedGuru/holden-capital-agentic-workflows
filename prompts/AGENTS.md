# AGENTS.md - prompts Node Access Rules

This node contains prompt files that drive Codex extraction and classification behavior.

## Scope

- extraction prompts
- classification prompts
- structured output guidance

## Rules

- Prompts are contracts, not freeform experiments.
- Changes here usually require checking `schemas/` and `samples/`.
- Keep prompts explicit about output format, review behavior, and safety limits.
- Do not encode secrets, API tokens, or machine-specific assumptions.
