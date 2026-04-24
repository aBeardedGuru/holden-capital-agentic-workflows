---
name: holden-finance-contract-sync
description: Use when changing finance automation behavior in this repo, especially prompts, schemas, scripts, workflow blueprints, or related docs. Keep the contract chain in sync across planning, docs, and automation, and validate changed artifacts.
---

# Holden Finance Contract Sync

Use this skill when a change touches finance automation behavior in `holden-capital-agentic-workflows`.

## Load First

Read:

- `governance/enterprise-development-standards.md`
- `docs/finance-document-intake.md` when relevant
- `planning/` artifacts related to the flow

## Contract Chain

For this repo, keep:

`planning -> docs -> automation`

Inside `automation/`, check:

`schemas -> prompts -> scripts -> workflows -> samples`

## Default Workflow

1. identify the behavioral change
2. find the affected contract layer first
3. update adjacent docs or artifacts in the same change
4. validate scripts and JSON artifacts
5. call out remaining risk explicitly

## Minimum Validation

Use the smallest relevant validation set:

```bash
bash -n automation/scripts/<script>.sh
python3 -m json.tool automation/workflows/<file>.json >/dev/null
python3 -m json.tool automation/schemas/<file>.json >/dev/null
python3 -m json.tool automation/samples/<file>.json >/dev/null
```

## Working Rules

- do not change workflow behavior without updating the related docs
- do not leave schema and prompt drift unresolved
- keep safety rules intact unless the issue explicitly changes them
- prefer review-state or disabled workflows over partially live automation

## Avoid

- updating only one layer of the contract chain
- treating planning docs as optional when behavior changes are user-visible
- leaving validation implicit
