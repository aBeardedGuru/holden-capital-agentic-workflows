# PROJECT_CONTEXT.md - Finance Automation Workspace

## Purpose

This repo is the AI-optimized workspace for Holden Capital finance automation planning and implementation support.

It exists to make agent work reliable across:

- finance document intake
- document classification and extraction
- expense categorization
- invoice collection queueing
- weekly financial reporting
- issue-driven planning and execution
- simple n8n workflow development

## Primary Stack

- Markdown for docs, planning, and agent instructions
- JSON Schema for contracts
- JSON for n8n blueprints and sample payloads
- Bash for local worker automation
- GitHub Issues and PRs for execution workflow
- OpenAI models for agent runtime
- BMAD agents plus `ho-pe` for operating roles

## Core Flow

Google Drive -> n8n -> local job packet -> Codex CLI -> JSON output -> Google Sheets -> review queue / processed state

## Design Bias

- contract-first
- docs-first
- review-first financial automation
- local AI execution where possible
- no secrets in repo

## Canonical Planning Surfaces

- `docs/`
- `planning/`
- GitHub epic and story issues

## Canonical Implementation Surfaces

- `automation/`
