# AGENTS.md - automation Node Access Rules

This node contains the actual finance automation building blocks.

## Scope

- `prompts/` for extraction and classification prompts
- `schemas/` for machine contracts
- `scripts/` for local worker execution
- `workflows/` for n8n blueprint JSON
- `samples/` for safe fixtures

## Why This Node Exists

Future n8n work should feel obvious:

1. define or update the contract
2. update the prompt if needed
3. update the local script if needed
4. update the n8n workflow blueprint
5. validate with samples

## Rules

- Treat this node as one system, not five separate mini-projects.
- If a schema changes, check prompts, scripts, workflows, and samples in the same change.
- Do not commit secrets, real IDs, or runtime artifacts.
- Keep workflow files importable and safe by default.
