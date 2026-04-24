# INSTRUCTIONS.md - .github Node Workflow

## Purpose

Use this node to define how work is captured and reviewed on GitHub.

## Current Operating Pattern

- Epic issues hold the full epic details.
- Story issues should become the direct implementation unit.
- PRs should reference the relevant issue numbers and explain contract changes.

## Editing Guidance

- Issue templates should be explicit and implementation-ready.
- PR template should force agents to state docs/schema/prompt/workflow impact.
- Keep labels and naming simple.

## Do Not

- encode environment secrets
- add repo automation that assumes unavailable infra
- create templates that depend on hidden local files
