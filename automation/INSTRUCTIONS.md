# INSTRUCTIONS.md - automation Node Workflow

## Working Order

When building or changing a finance automation flow, work in this order:

1. `schemas/`
2. `prompts/`
3. `scripts/`
4. `workflows/`
5. `samples/`
6. `docs/`

That order keeps the contract clear before implementation details move.

## Expected Flow Pattern

Use this mental model:

`Trigger -> Validate -> Extract/Classify -> Review/Route -> Log`

## Current Automation Surfaces

- `prompts/extract-finance-document.md`
- `schemas/finance-job.schema.json`
- `schemas/finance-extraction.schema.json`
- `workflows/google-drive-download-for-processing.json`

## Simplicity Rule

If a change makes an agent read more than one level deep in multiple places to understand one flow, the structure is too complex and should be simplified again.
