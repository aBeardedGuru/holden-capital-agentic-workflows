# INSTRUCTIONS.md - workflows Node Workflow

## Workflow Design Standard

Prefer the same useful pattern seen in the mono repo's communications project:

`Trigger -> Validate -> Transform -> Integrate -> Review/Error -> Log`

## Current Blueprint Expectations

- default to inactive when configuration is incomplete
- use placeholder IDs and paths
- include implementation notes when the blueprint is partial
- keep review and audit steps visible

## When Editing

- confirm the blueprint still matches the local worker command and runtime directories
- confirm schema names and output expectations still match
- update docs if manual setup steps change
