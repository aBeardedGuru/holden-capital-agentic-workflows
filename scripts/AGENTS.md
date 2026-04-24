# AGENTS.md - scripts Node Access Rules

This node contains local automation scripts, especially the Codex worker that processes finance job packets.

## Rules

- Scripts must respect schema contracts.
- Scripts must keep runtime state under `runtime/`.
- Scripts must not require committed secrets.
- Changes here must be reflected in docs when behavior or CLI usage changes.
