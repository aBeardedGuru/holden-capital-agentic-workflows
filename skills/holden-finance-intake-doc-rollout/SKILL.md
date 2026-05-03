---
name: holden-finance-intake-doc-rollout
description: Use when adding or changing supported finance document types in the intake workflow (for example bank statements) and you need repeatable classifier, routing, and sheet mapping updates.
---

# Holden Finance Intake Doc Rollout

Use this skill when you need a repeatable way to add or change finance document handling in the intake workflow.

## Load First

Read:

- `governance/enterprise-development-standards.md`
- `docs/finance-document-intake.md`
- `docs/finance-ledger-operating-contract.md`
- `skills/holden-finance-contract-sync/SKILL.md`

## Scope

This skill is for changes such as:

- adding a new document type to classifier output
- changing how a document type routes to processed/review/error folders
- changing which sheet/tab receives a row for a given document type
- splitting business event summary vs extraction/validation notes

## Default Workflow

1. define the document behavior contract first
2. update classifier output keys and allowed values
3. update parser/normalizer validation and fallback behavior
4. update sheet mappings and folder routing logic
5. update docs to match runtime behavior
6. validate JSON and run one multi-file manual execution

## Required Decision Table

For each document type, define:

- document type label
- processed folder target
- review routing condition
- error routing condition
- target sheet/tab(s)
- key fields required before append

Example:

- `invoice`: append expense rows, route to processed invoices folder when valid
- `bank_statement`: append balance sheet rows, route to statements folder when valid
- `other`: append financial log only, route to other folder unless review/error

## Implementation Checklist

Update in this order:

1. workflow classifier prompt (`AI Intake Classifier`) output schema
2. parser validation (`Parse And Normalize`) required keys and routing rules
3. append nodes mapping (`Append Financial Log`, and any sheet-specific append nodes)
4. final route builder (`Build Final Route`)
5. workflow artifact in `automation/workflows/`
6. docs in `docs/` describing columns and routing behavior

## Minimum Validation

```bash
python3 -m json.tool automation/workflows/<workflow-file>.json >/dev/null
python3 -m json.tool automation/schemas/<schema-file>.json >/dev/null
```

Manual n8n checks:

1. place at least two files in inbox (mixed document types)
2. run one manual execution
3. confirm all files were processed in one run
4. confirm each document type wrote to correct sheet columns
5. confirm folder moves match the decision table

## Working Rules

- keep `event_summary` as business narrative from document text
- keep `notes` for extraction/validation/operational context
- do not use single-item references (`$item(0)`, `.first()`) on multi-item paths
- if a code node is `runOnceForEachItem`, return one object (`{ json: ... }`), not an array
- keep secrets and live IDs out of tracked workflow JSON

