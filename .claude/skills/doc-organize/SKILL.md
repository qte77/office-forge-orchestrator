---
name: doc-organize
description: Read document content → classify by type → apply YYYY-MM-DD taxonomy naming → move to organized subdirs → generate manifest. Use when organizing chaotic document folders.
compatibility: Designed for Claude Code
metadata:
  argument-hint: [source-dir] [output-dir]
  allowed-tools: Read, Write, Glob, Bash
  mcp-servers: [filesystem]
---

# Document Organization

**Source**: $ARGUMENTS (defaults: `./inbox/` → `./archive/`)

Deterministic pipeline: read content → classify → rename → move → manifest.

## Document Types

| Type | Subdir | Naming pattern |
|------|--------|----------------|
| invoice | `invoices/` | `YYYY-MM-DD_invoice_<vendor>.ext` |
| receipt | `receipts/` | `YYYY-MM-DD_receipt_<vendor>.ext` |
| contract | `contracts/` | `YYYY-MM-DD_contract_<counterparty>.ext` |
| correspondence | `correspondence/` | `YYYY-MM-DD_<sender>_<subject-slug>.ext` |
| report | `reports/` | `YYYY-MM-DD_report_<title-slug>.ext` |
| unknown | `unsorted/` | original filename (unchanged) |

## Workflow

1. **Discover files** — glob `$SOURCE_DIR` recursively for all non-hidden files
2. **Read content** — read each file (not just filename) to determine type and extract:
   - `type` — classify using Document Types table above
   - `date` — find most specific date in content; normalize to YYYY-MM-DD; fallback to file mtime
   - `key_name` — vendor / counterparty / sender (lowercase, spaces → hyphens, max 30 chars)
3. **Generate target path** — apply naming pattern from table; truncate slug to 40 chars
4. **Detect conflicts** — if target path already exists, append `_2`, `_3`, etc.
5. **Move files** — move `$SOURCE_DIR/<file>` → `$OUTPUT_DIR/<subdir>/<new-name>`
6. **Write manifest** — create `$OUTPUT_DIR/manifest.csv` with columns:
   `Original | NewPath | Type | Date | KeyName | Action`
   - `Action`: `moved` | `conflict-renamed` | `skipped-unreadable`
7. **Print summary** — count per type, count skipped

## Input Contract

```text
$SOURCE_DIR/
  **/*    — any document files (PDF, DOCX, TXT, images, etc.)
```

## Output Contract

```text
$OUTPUT_DIR/
  invoices/        — invoice documents
  receipts/        — receipt documents
  contracts/       — contract documents
  correspondence/  — letters, emails
  reports/         — report documents
  unsorted/        — unclassified files
  manifest.csv     — full audit trail of all moves
stdout             — summary counts per type
```

## Constraints

- Do NOT delete source files — move only (manifest allows reversal)
- Do NOT rename files in `unsorted/` — preserve originals for human review
- If a file cannot be read, move to `unsorted/` with `skipped-unreadable` in manifest
- Idempotent: running twice on same source does not duplicate files (conflict detection handles it)
