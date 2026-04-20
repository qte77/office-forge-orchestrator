---
name: doc-search
description: Ingest documents into RAG index → search with hybrid retrieval (vector + tree filter) → return results with source citations. Use when searching across office documents.
compatibility: Designed for Claude Code
metadata:
  argument-hint: [target-dir-or-query]
  allowed-tools: Read, Write, Glob, Bash
---

# Document Search

**Source**: $ARGUMENTS (defaults: `./documents/` for ingest, query string for search)

Hybrid retrieval pipeline: discover documents → ingest (parse + chunk + embed) → search → format results.

## Workflow

1. **Discover documents** — `Glob` for `*.pdf`, `*.docx`, `*.md`, `*.txt` in target directory
2. **Ingest** — parse, chunk by headings, embed, and index:
   ```bash
   uv run --project memory/ doc-memory ingest <document-dir>
   ```
3. **Search** — embed query, vector search, tree filter, return ranked results:
   ```bash
   uv run --project memory/ doc-memory search "<query>"
   ```
4. **Format results** — present with source citations (file, page, heading path)

## Input Contract

```
$TARGET_DIR/
  *.pdf | *.docx | *.md | *.txt   — document files to index
```

## Output Contract

```
stdout   — ranked results with source, page number, heading path, and content excerpt
```

## Constraints

- Do NOT modify source documents
- Do NOT delete or overwrite existing index without user confirmation
- Index persists in `.doc_memory_index/` — reuse across searches
- If no index exists, ingest before searching
