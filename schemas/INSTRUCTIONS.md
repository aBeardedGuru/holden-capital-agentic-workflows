# INSTRUCTIONS.md - schemas Node Workflow

## Change Process

1. Identify the producer and consumer of the schema.
2. Edit the schema intentionally.
3. Update sample payloads.
4. Update prompts and scripts that consume or produce the contract.
5. Update docs describing the contract.

## Schema Principles

- explicit required fields
- minimal ambiguity
- review-first statuses
- privacy-safe financial fields

## Current Contracts

- `finance-job.schema.json`: n8n to local worker
- `finance-extraction.schema.json`: local worker/Codex to n8n review flow
