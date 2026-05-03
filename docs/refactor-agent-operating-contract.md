# Refactor Agent Operating Contract

## Purpose

Define a simple one-agent n8n workflow that reviews a repository, identifies safe refactor opportunities, and returns a structured refactor report for a monorepo or single-repo codebase.

This workflow is advisory-first by default. It should inspect and recommend before it attempts larger structural change.

## Current Target

The initial live target is the chat workflow:

- `Refactor Agent`
- n8n workflow ID: `BIIm0hKHWavBIY3z`

The tracked blueprint in this repo is the safe, importable version of that workflow.

## Inputs

- A chat request that names the target repository using either:
  - a GitHub repository URL, or
  - an `owner/repo` string
- Optional focus instructions such as:
  - package or folder to prioritize
  - whether to stay advisory-only or make low-risk changes
  - risk tolerance for cross-package refactors
- Prompt contract:
  - `automation/prompts/refactor-agent-monorepo.md`

## Outputs

- One structured refactor report in markdown with these sections:
  - `Repository map`
  - `Conventions detected`
  - `Findings`
  - `Refactor plan`
  - `Proposed changes`
  - `Test plan`
  - `Risks and rollback`

## Workflow Shape

1. Trigger:
- Chat trigger.

2. Request normalization:
- Convert the inbound chat payload into a stable text request for the agent.
- Parse the repository target and requested action from the same input.

3. Repository validation:
- Extract a single GitHub repository target from the request.
- If no repository target is present, return a clarification response instead of calling tools.

4. Repository preflight:
- Look up the repository before the agent runs.
- If the repository is unavailable or inaccessible, return a concise note instead of invoking the agent.

5. Repository inspection:
- Use the preflight metadata, repository file listing, and connected GitHub pull request context to gather repository context.
- Start by reading the top-level tree, then manifests, then entrypoints and relevant source files.
- Use file contents when a path is known and avoid broad claims without evidence.

6. Refactor analysis:
- Apply the refactor prompt.
- Prefer evidence-backed, low-risk findings.
- Do not claim file-level certainty when tooling does not expose file contents.

7. Response:
- Return one structured report to the chat caller.

## Node Inventory

- `When chat message received`
  - chat trigger entrypoint
- `Prepare Request`
  - normalizes chat payload into one stable refactor request string
- `Validate Repository Target`
  - extracts and validates a GitHub repository target from the request
- `Repository Target Gate`
  - routes missing repository targets to a clarification response
- `Get a repository in GitHub`
  - preflights repository availability and returns lightweight metadata
- `List repository files in GitHub`
  - discovers top-level and targeted repository files
- `Get repository file in GitHub`
  - reads a known repository file path
- `Repository Availability Gate`
  - routes inaccessible repositories to a concise note and sends successful lookups forward
- `Prepare Agent Payload`
  - normalizes repository lookup metadata and preserves validated request context for downstream nodes
- `Refactor Agent`
  - single AI agent node that applies the refactor prompt and returns the structured report
- `Reply With Clarification`
  - returns a short response when the repository target is missing
- `Reply With Repository Unavailable`
  - returns a short response when the repository cannot be accessed
- `OpenRouter Chat Model`
  - language model backing the agent
- `Get pull requests of a repository in GitHub`
  - pull request metadata tool for recent change and drift context

## Connection Shape

- `When chat message received -> Prepare Request -> Validate Repository Target -> Repository Target Gate`
- `Repository Target Gate -> Reply With Clarification` when the request is missing a repo
- `Repository Target Gate -> Get a repository in GitHub` when the request contains a valid repo target
- `Get a repository in GitHub -> Prepare Agent Payload`
- `Prepare Agent Payload -> Repository Availability Gate`
- `Repository Availability Gate -> Reply With Repository Unavailable` when the repo lookup fails
- `Repository Availability Gate -> Refactor Agent` when the repo lookup succeeds
- `OpenRouter Chat Model -> Refactor Agent` as `ai_languageModel`
- `List repository files in GitHub -> Refactor Agent` as `ai_tool`
- `Get repository file in GitHub -> Refactor Agent` as `ai_tool`
- `Get pull requests of a repository in GitHub -> Refactor Agent` as `ai_tool`

## Required Guardrails

- Preserve public behavior by default.
- Prefer recommendations over speculative rewrites.
- Do not claim hidden code facts that were not actually inspected.
- Do not call GitHub tools unless the repository target was validated upstream.
- Use `requestedAction` to bias output toward refactor guidance when the user explicitly asks for refactoring.
- Prefer the upstream repository lookup metadata over re-querying the repository in the agent path.
- Treat GitHub lookup failures as advisory evidence that the repo is unavailable or inaccessible, not as a crash condition.
- Keep the workflow importable and placeholder-safe.
- Do not store live credential IDs, webhook IDs, or secrets in tracked JSON.

## Known Limitation In This Simple Version

This first version mirrors the current live workflow shape and keeps the toolset small. It is useful for repo-level triage and phased refactor planning, but it is not a full code-indexed refactor worker yet.

If deeper file inspection is needed, add the required repository file or search tools before treating the agent as a source of line-level certainty.

## Validation

- `python3 -m json.tool automation/workflows/refactor-agent.blueprint.json >/dev/null`
- Review prompt text for output shape and guardrail alignment.
- Import the blueprint into n8n and verify the connected credentials manually.

## Governance Alignment

- Contract-first: prompt and operating contract define the agent before wider rollout.
- Reviewable: the blueprint is small and easy to audit.
- Safe-by-default: this version returns structured guidance instead of autonomous broad rewrites.
