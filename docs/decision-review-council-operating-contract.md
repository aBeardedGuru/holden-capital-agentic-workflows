# Decision Review Council Operating Contract

## Purpose

Define the advisory contract for the `The Force Council` n8n workflow that reviews deals and decisions through four role-specific lenses:

- `discipline`
- `wealth`
- `strategy`
- `wisdom`

This workflow is advisory only. It does not approve transactions, move capital, post to external systems, or make decisions on the operator's behalf.

## Runtime Scope

Supported review types:

- `deal_review`
- `business_decision`
- `personal_decision`

Supported input modes:

- freeform chat
- structured request JSON normalized from chat

The workflow should accept imperfect user input, normalize it into a stable request contract, and only perform a full review when enough context exists to support a defensible recommendation.

## Source Of Reasoning

The council reasoning lenses are derived from the external `holden-capital-agents` skill repo, specifically:

- `council-discipline`
- `council-wealth`
- `council-strategy`
- `council-wisdom`

The external repo is design input only. Runtime behavior for this workflow must be defined by repo-local prompts, schemas, samples, and workflow JSON.

Important external metadata drift:

- the external `SKILL.md` and `README.md` still reference `knowledge-graph.json` and `knowledge-graph.md`
- the actual maintained council assets are the role `principles`, `patterns`, `templates`, and `runbooks`

This workflow must use the actual maintained assets, not the stale metadata references.

## Request Contract

The normalized request must match:

- [automation/schemas/council-review-request.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/council-review-request.schema.json)

Required fields:

- `schema_version`
- `request_id`
- `decision_type`
- `question`
- `context`
- `options_considered`
- `preferred_option`
- `time_horizon`
- `capital_at_risk`
- `resource_commitment`
- `upside_case`
- `base_case`
- `downside_case`
- `known_risks`
- `unknowns`
- `constraints`
- `values_or_principles`
- `requested_at`

The workflow may infer these fields from freeform chat, but it must preserve uncertainty explicitly rather than inventing facts.

## Review Flow

```text
Chat input
  -> normalize into request packet
  -> council decides if the request is reviewable
  -> if not reviewable, return clarification questions
  -> if reviewable, call all four role agents
  -> synthesize agreements, disagreements, risks, and next steps
  -> return advisory response
  -> prepare audit payload for configured logging surface
```

## Clarification Rules

Return `needs_clarification` instead of a full review when any of these are true:

- the operator’s actual question is unclear
- no concrete option or proposed action can be identified
- deal economics are too incomplete for a deal review
- downside, constraints, or time horizon are missing and materially change the recommendation
- the prompt appears to ask for certainty that the council cannot responsibly provide

Clarification output must include:

- the missing facts
- concise follow-up questions
- a provisional note on what cannot yet be evaluated

## Role Responsibilities

### Discipline

Focus on:

- execution realism
- habit or process implications
- focus cost
- behavioral friction
- sustainability and burnout risk

### Wealth

Focus on:

- capital allocation quality
- valuation and payoff asymmetry
- downside severity
- risk concentration
- opportunity cost
- whether uncertainty is tolerable

### Strategy

Focus on:

- strategic fit
- trade-offs
- coherence with current direction
- capability mismatch
- second-order business consequences
- what not to do

### Wisdom

Focus on:

- values alignment
- doubt signals
- long-term human consequences
- commitment quality
- whether fear, hope, or ego is distorting the decision

## Role Output Contract

Each role must return JSON matching:

- [automation/schemas/council-role-review.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/council-role-review.schema.json)

Each role must:

- state its verdict
- state confidence
- surface top risks
- identify key assumptions
- identify missing information
- challenge weak reasoning from the operator when needed

## Final Synthesis Contract

The final council output must match:

- [automation/schemas/council-review-result.schema.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/schemas/council-review-result.schema.json)

Allowed statuses:

- `needs_clarification`
- `review_complete`
- `partial_review`
- `failed`

The synthesis must preserve disagreements explicitly. It must not collapse materially different role views into false consensus.

## Chat Response Contract

The workflow should format the final user-visible response into these sections:

- recommendation
- why
- where the agents agree
- where they disagree
- biggest risks
- missing information
- next steps

If status is `needs_clarification`, replace the recommendation section with:

- what is missing
- the exact follow-up questions needed

## Logging Contract

Default logging surface: Google Sheets.

Recommended tabs:

- `Council Reviews`
- `Council Agent Views`

The tracked workflow blueprint may include placeholder-safe config for logging. The live workflow must not hardcode unknown sheet IDs, credential IDs, or secrets.

If logging is not configured in a live environment, the review path must still function for chat.

The separate long-lived knowledge hub should use:

- [knowledge-hub/](/home/dank/Projects/holden-capital-agentic-workflows/knowledge-hub) for text retrieval
- [docs/council-knowledge-sheets-schema.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/council-knowledge-sheets-schema.md) for structured retrieval

## Safety Rules

- No execution of investment decisions.
- No automated buying, selling, or capital movement.
- No silent external notifications.
- No fake certainty.
- No hidden assumptions presented as facts.
- No secrets, tokens, or credentials in prompts, schemas, samples, or tracked workflow JSON.

## Validation Artifacts

Use these fixtures when validating the council contract:

- [automation/samples/council-review-request.deal.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/council-review-request.deal.sample.json)
- [automation/samples/council-review-request.business.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/council-review-request.business.sample.json)
- [automation/samples/council-review-request.personal.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/council-review-request.personal.sample.json)
- [automation/samples/council-review-request.insufficient.sample.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/samples/council-review-request.insufficient.sample.json)
- [automation/workflows/the-force-council.blueprint.json](/home/dank/Projects/holden-capital-agentic-workflows/automation/workflows/the-force-council.blueprint.json)
