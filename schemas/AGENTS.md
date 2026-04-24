# AGENTS.md - schemas Node Access Rules

This node defines machine-readable contracts between n8n, local scripts, prompts, and downstream review surfaces.

## Rules

- Treat schema changes as contract changes.
- Do not widen or narrow fields casually.
- Preserve backward compatibility when possible, or version the schema intentionally.
- Schema edits usually require matching changes in `prompts/`, `samples/`, `scripts/`, and `docs/`.
