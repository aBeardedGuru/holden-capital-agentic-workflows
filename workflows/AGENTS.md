# AGENTS.md - workflows Node Access Rules

This node contains n8n blueprint exports and workflow definitions.

## Rules

- Workflow files must remain safe to commit.
- No live credentials, tokens, or real folder IDs in committed blueprints.
- Workflow changes must stay aligned with `schemas/`, `scripts/`, and `docs/`.
- Workflow JSON should be importable and understandable by a maintainer without hidden context.
