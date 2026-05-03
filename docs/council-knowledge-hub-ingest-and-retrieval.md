# Council Knowledge Hub Ingest And Retrieval

## Purpose

Describe where the council knowledge hub lives, how it gets ingested, and how the agents should retrieve from it.

## Source Of Truth

The knowledge hub has two storage layers.

### Text Layer

Lives in:

- [knowledge-hub/](/home/dank/Projects/holden-capital-agentic-workflows/knowledge-hub)

This is the durable git-tracked source for:

- principles
- patterns
- templates
- worked examples
- postmortems

### Structured Layer

Lives in:

- one `Council Knowledge` workbook or table base

Schema:

- [council-knowledge-sheets-schema.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/council-knowledge-sheets-schema.md)

This is the exact-query source for:

- decision journals
- deal scorecards
- red flags
- operator principles

## Ingest Flow

Recommended ingestion model:

```text
knowledge-hub markdown
  -> split into chunks
  -> attach metadata
  -> generate embeddings
  -> write to vector store
```

Recommended metadata on each chunk:

- `role`
- `source_type`
- `topic`
- `decision_type`
- `source_title`
- `version`

Recommended vector-store options in n8n:

- `Simple Vector Store` for v1
- `Chroma Vector Store` for a more durable dedicated store

## Retrieval Flow

Recommended retrieval model:

```text
Council agent
  -> query vector retriever for role-relevant text
  -> query structured sheet or sub-workflow for exact facts
  -> combine both into final reasoning
```

## Per-Agent Retrieval Guidance

### Discipline

Should retrieve:

- discipline principles
- execution and workload patterns
- prior examples of overload or strong execution design

Should query structured data for:

- workload checklists
- decision journal entries tagged with execution failure or success

### Wealth

Should retrieve:

- wealth principles
- underwriting patterns
- capital allocation templates

Should query structured data for:

- deal scorecards
- red flags related to downside, leverage, concentration, or uncertainty

### Strategy

Should retrieve:

- strategy principles
- fit and trade-off patterns
- sequencing templates

Should query structured data for:

- operator principles
- red flags related to dilution, incoherence, and capability mismatch

### Wisdom

Should retrieve:

- wisdom principles
- values and doubt patterns
- commitment templates

Should query structured data for:

- operator principles
- decision journal entries tagged with regret, misalignment, or good judgment

## Recommended V1 Tool Surface

Use:

- one `Vector Store Retriever`
- one `Google Sheets` tool surface
- optional `Code Tool` for simple calculations

Then add role-specific sub-workflows later if needed.
