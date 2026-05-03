# Decision Review Council Tooling

## Purpose

Recommend a practical tool layout for the four council agents and a shared knowledge hub that can support them inside n8n.

This document is intentionally tool-oriented. It complements the council operating contract and the standalone prompts.

## Shared Knowledge Hub

The strongest shared pattern is:

```text
Curated source material
  -> chunked and embedded into a vector store
  -> retrieved through role-specific queries
  -> optionally combined with structured scorecards and operator worksheets
```

Recommended shared layers:

1. `Vector Store Retriever`
   Use this as the primary role knowledge hub for principles, patterns, templates, and examples.

2. `Google Sheets`
   Use this for structured scorecards, checklists, decision journals, underwriting sheets, and review logs.

3. `MCP Client Tool`
   Use this when agents need controlled access to internal systems, docs, or structured connected tools.

4. `HTTP Request Tool`
   Use this for bounded external facts when they materially improve a decision.

5. `Call n8n Workflow Tool`
   Use this to break specialized tasks into reusable sub-workflows such as underwriting, fit scoring, or reflection workflows.

## Recommended Knowledge Hub Design

Use one shared vector corpus with role metadata, or four logical corpora if you want stricter separation.

Recommended content sources for the vector corpus:

- [knowledge-hub/](/home/dank/Projects/holden-capital-agentic-workflows/knowledge-hub) role docs
- role principles
- role patterns
- role templates
- example reviews
- operator-specific heuristics and postmortems

Recommended metadata fields:

- `role`
- `source_type`
- `topic`
- `decision_type`
- `source_title`
- `version`

Recommended vector-store options in n8n:

- `Simple Vector Store` for fast local experimentation
- `Chroma Vector Store` when you want a more durable dedicated vector store
- any team-standard external vector database if already adopted

## Agent Tool Recommendations

### Discipline

Primary tools:

- `Vector Store Retriever`
- `Google Sheets`
- `Code Tool`
- `Call n8n Workflow Tool`

Best uses:

- retrieve habit, focus, workload, and execution frameworks
- score implementation burden
- compute time-budget or workload pressure
- run structured execution-readiness subflows

### Wealth

Primary tools:

- `Vector Store Retriever`
- `Google Sheets`
- `Code Tool`
- `HTTP Request Tool`
- `Call n8n Workflow Tool`

Best uses:

- retrieve wealth principles and underwriting templates
- run downside, concentration, and sensitivity analysis
- pull public rates, market data, or other bounded external facts
- run separate underwriting or comparable-analysis workflows

### Strategy

Primary tools:

- `Vector Store Retriever`
- `Google Sheets`
- `MCP Client Tool`
- `HTTP Request Tool`
- `Call n8n Workflow Tool`

Best uses:

- retrieve strategy frameworks and trade-off templates
- score fit, sequencing, or initiative coherence
- inspect internal planning artifacts and workflow metadata
- fetch market or competitor facts when relevant
- run capability-fit or roadmap-evaluation subflows

### Wisdom

Primary tools:

- `Vector Store Retriever`
- `Google Sheets`
- `MCP Client Tool`
- `Call n8n Workflow Tool`

Best uses:

- retrieve values, doubt, and reflection frameworks
- reference decision journals or commitment-review sheets
- inspect internal notes or structured reflections when permitted
- run dedicated reflection or commitment-check workflows

## Recommended Minimal V1

If you want the smallest useful tool set first, use:

- one shared `Vector Store Retriever`
- one shared `Google Sheets` tool surface
- one shared `Code Tool`

Seed those from:

- [knowledge-hub/](/home/dank/Projects/holden-capital-agentic-workflows/knowledge-hub)
- [council-knowledge-sheets-schema.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/council-knowledge-sheets-schema.md)

Then add:

- `HTTP Request Tool` for Wealth and Strategy
- `MCP Client Tool` for Strategy and Wisdom
- sub-workflow tools as complexity grows

## Source References

These recommendations align with current n8n docs for:

- AI Agent Tool
- Call n8n Workflow Tool
- HTTP Request as an AI tool
- MCP Client Tool and instance-level MCP server
- Vector Store Retriever and RAG patterns
