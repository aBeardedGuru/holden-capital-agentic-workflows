# Council Knowledge Hub

## Purpose

This folder is the source-of-truth text corpus for the Decision Review Council.

It is designed to be:

- human-readable in git
- chunkable for embedding and vector retrieval
- role-scoped for the council agents
- stable enough to version and review

## Structure

```text
knowledge-hub/
  discipline/
    principles.md
    patterns.md
    templates.md
  wealth/
    principles.md
    patterns.md
    templates.md
  strategy/
    principles.md
    patterns.md
    templates.md
  wisdom/
    principles.md
    patterns.md
    templates.md
  examples/
    good-decisions.md
    bad-decisions.md
    postmortems.md
```

## Intended Runtime Use

This folder should be ingested into a vector store and exposed to the council agents through a `Vector Store Retriever` tool.

Recommended ingestion metadata:

- `role`
- `source_type`
- `topic`
- `decision_type`
- `source_title`
- `version`

## Writing Rules

- Keep each file role-specific.
- Prefer short sections with strong headings over long undifferentiated prose.
- Store reusable reasoning content here, not one-off conversations.
- Put prior-case narratives under `examples/`, not inside role docs.
- Update this corpus when the council’s judgment standards change.

## Companion Structured Data

This text corpus is only one half of the knowledge hub.

Structured companion data should live in a sheet or table surface using the schema in:

- [docs/council-knowledge-sheets-schema.md](/home/dank/Projects/holden-capital-agentic-workflows/docs/council-knowledge-sheets-schema.md)

The structured layer should hold:

- decision journals
- deal scorecards
- red flags
- operator principles
