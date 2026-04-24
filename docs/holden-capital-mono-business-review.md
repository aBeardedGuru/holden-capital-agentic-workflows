# Holden Capital Mono Business Review

Date: 2026-04-23
Reviewer: Winston, system architect
Scope reviewed: `/home/dank/Projects/holden-capital-mono`

## Executive Summary

`holden-capital-mono` is best understood as an operating system for a real estate investment and property operations business. The repo combines four business capabilities:

1. Real estate intelligence through `real-estate-app/`
2. Guest and operator communication automation through `communications/`
3. Infrastructure and deployment automation through `infra/`
4. Agent skill and workflow governance through `agents/`

The strategic direction is coherent: use real estate data, repeatable automations, and local infrastructure discipline to reduce manual work and improve investment decisions. The main gap is not vision. The gap is the handoff layer between strategy and runnable sample workflows, especially for `communications/` and n8n.

## Business Purpose

The business purpose is to build an intelligent, automated platform for property acquisition, analysis, operations, and communications.

The clearest value chain is:

1. Gather property and market data.
2. Analyze investment quality and operating potential.
3. Track acquisition targets and property state.
4. Automate routine communications and operational workflows.
5. Run the platform on reliable, recoverable infrastructure.
6. Use agent workflows to keep delivery consistent.

This is a good architecture for a small but scaling real estate operation because it keeps the critical business loops close together: data, decisions, communications, deployment, and agent execution.

## Strategic Goals Observed

The repo documents four strategic pillars:

| Pillar | Goal | Current Interpretation |
| --- | --- | --- |
| Real Estate Intelligence | Turn property data into useful investment decisions | `real-estate-app/` is the core business product and analytical engine. |
| Operational Automation | Reduce manual operating burden | OpenClaw and agent workflows are intended to automate recurring technical and operational work. |
| Process Automation | Automate guest and business communications | `communications/` is the right place for n8n flows, templates, and workflow runbooks. |
| Infrastructure Excellence | Make the system deployable, recoverable, and observable | `infra/` and ForceGrid are the platform foundation. |

The goals are directionally strong. The repo would benefit from converting them into narrower "first usable flow" milestones so implementation agents do not overbuild.

## Repo Review

### What Is Strong

- The monorepo has clear domain boundaries: communications, real-estate app, infrastructure, and agent definitions.
- Governance docs exist for branching, code standards, security, releases, and architecture.
- The real-estate app has a mature shape: FastAPI backend, React frontend, PostgreSQL, Alembic, Docker, Storybook/Playwright work, Firecrawl docs, and BMAD planning artifacts.
- The communications project has useful guest-facing content already: booking, check-in, checkout, review, question, and stay templates.
- The n8n backup review correctly identifies persistence and recovery as critical before production use.
- The roadmap shows sensible sequencing: product foundations first, then workflow automation and infrastructure hardening.

### Main Gaps

- `communications/` says `workflows/` should exist, but no workflow catalog is currently present.
- The n8n deployment artifact is production-leaning and NAS-backed. That is right for operations, but not enough for quick local sample-flow iteration.
- Communications has templates, but no explicit mapping from template to trigger, payload, channel, SLA, error handling, and logging.
- Business goals are broad and ambitious. The next implementation unit should be deliberately small: a dry-run workflow that validates shape before sending real messages.
- There are two `holden-capital-mono` directories on disk:
  - `/home/dank/Projects/holden-capital-mono`
  - `/home/dank/Projects/qa-agent/holden-capital-mono`
  The direct project path appears to be the intended active repo.

## Architectural Read

The right architecture is boring and staged:

1. Start with dry-run n8n flows that validate payloads and render messages.
2. Add real-estate-app reads only after payload shape is stable.
3. Add SendGrid/Twilio only after validation, rendering, idempotency, and logging are agreed.
4. Add production backup and deployment once the first few flows are worth preserving.

This prevents the common automation failure mode: wiring live integrations before the business event model is stable.

## Recommended First Sample Flows

| Priority | Flow | Trigger | Output | Why This First |
| --- | --- | --- | --- | --- |
| 1 | Booking created confirmation | `booking.created` webhook | Dry-run email/SMS draft | Highest guest impact, simple event model, clear SLA. |
| 2 | Check-in reminder | Scheduled query or booking event | Dry-run SMS/email draft | Uses existing check-in templates and has clear timing rules. |
| 3 | Checkout reminder | Scheduled query | Dry-run message draft | Operationally useful and low integration complexity. |
| 4 | Payment issue notification | Payment webhook | Guest/operator message draft | More sensitive; do after base validation patterns exist. |
| 5 | Review request | Scheduled post-checkout event | Email/SMS draft | Useful but less urgent than stay-critical communication. |

## First Milestone

Create a docs-only sample-flow design pack before adding workflow JSON to the monorepo.

The first milestone should answer:

- What event starts the flow?
- What payload fields are required?
- What template is used?
- What does the rendered message look like?
- What is the SLA?
- What happens on missing data?
- What gets logged?
- What makes the flow safe to activate?

Once those answers are stable, the implementation step can add importable n8n JSON to `holden-capital-mono/communications/workflows/`.

## Risks To Watch

- Credentials and secrets: n8n workflows must not export live credentials to git.
- Duplicate sends: every guest-facing workflow needs idempotency before activation.
- Payload drift: real-estate-app event schemas should be versioned or documented.
- Over-coupling: n8n should call stable APIs, not depend on internal database structure.
- Recovery: production n8n should not go live without persistent storage and snapshots.

## Architect Recommendation

Treat `holden-capital-agentic-workflows` as the planning and workflow-design workspace. Treat `holden-capital-mono` as the product and implementation workspace.

That gives you a clean working rhythm:

1. Design sample flows as docs here.
2. Review business logic and failure paths here.
3. Promote approved flows into the monorepo as versioned n8n JSON.
4. Deploy only after persistence, logging, and rollback are documented.
