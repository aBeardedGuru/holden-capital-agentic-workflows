# Council Knowledge Sheets Schema

## Purpose

Define the structured table layer that complements the text corpus in `knowledge-hub/`.

Use one workbook or table base named `Council Knowledge`.

Recommended tabs:

- `Decision Journal`
- `Deal Scorecards`
- `Red Flags`
- `Operator Principles`

## Decision Journal

Purpose:

- store prior important decisions
- capture what was known at decision time
- record outcomes and lessons

Required columns:

- `entry_id`
- `decision_date`
- `decision_type`
- `title`
- `summary`
- `preferred_option`
- `other_options`
- `capital_at_risk`
- `time_horizon`
- `known_risks`
- `unknowns`
- `actual_outcome`
- `lesson`
- `tags`
- `approved_for_retrieval`

## Deal Scorecards

Purpose:

- store reusable underwriting or deal-comparison facts
- give the wealth agent an exact factual layer to query

Required columns:

- `deal_id`
- `recorded_at`
- `asset_name`
- `asset_type`
- `market`
- `purchase_price`
- `capital_required`
- `base_case_return`
- `upside_case_return`
- `downside_case_return`
- `max_loss_estimate`
- `key_risks`
- `kill_criteria`
- `status`
- `lesson`
- `approved_for_retrieval`

## Red Flags

Purpose:

- store recurring warning patterns the council should retrieve quickly

Required columns:

- `flag_id`
- `role`
- `title`
- `description`
- `decision_type`
- `severity`
- `trigger_condition`
- `recommended_response`
- `example_reference`
- `approved_for_retrieval`

## Operator Principles

Purpose:

- store operator-specific decision rules and non-negotiables

Required columns:

- `principle_id`
- `role`
- `title`
- `statement`
- `why_it_exists`
- `applies_to`
- `priority`
- `approved_for_retrieval`

## Retrieval Guidance

Use the structured sheets for:

- exact prior-case lookup
- red-flag matching
- operator-specific principles
- numeric underwriting references

Do not use the sheets as the only knowledge source. They complement the vector-retrieved text corpus.
