# INSTRUCTIONS.md - scripts Node Workflow

## Before Editing A Script

Read:

1. related schema files
2. related prompts
3. related workflow blueprint notes
4. the relevant doc in `docs/`

## Script Standards

- fail loudly on contract violations
- keep paths explicit
- prefer deterministic file movement between runtime directories
- never commit runtime outputs as fixtures

## Current Primary Script

- `codex-finance-worker.sh`: reads inbox job JSON, invokes Codex locally, validates output, and moves job files through runtime states
