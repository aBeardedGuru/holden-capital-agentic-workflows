# INSTRUCTIONS.md - prompts Node Workflow

## Before Editing A Prompt

Read:

1. the target schema in `schemas/`
2. the relevant sample in `samples/`
3. the consuming script in `scripts/`

## Prompt Design Rules

- ask for structured output only
- keep document classification categories aligned with schema enums
- require confidence and review reason when applicable
- preserve the review-first model

## Validation Mindset

If prompt behavior changes, confirm that the expected output still fits the extraction schema and worker flow.
