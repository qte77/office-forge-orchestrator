---
name: invoice-processing
description: OCR and extract invoice/receipt data → validate → output organized spreadsheet. Use when processing invoices, receipts, or expense documents.
compatibility: Designed for Claude Code
metadata:
  argument-hint: [source-dir] [output-file.xlsx]
  allowed-tools: Read, Write, Glob, Bash
  mcp-servers: [filesystem, xero, quickbooks]
---

# Invoice Processing

**Source**: $ARGUMENTS (defaults: `./inbox/` → `./output/invoices.xlsx`)

Deterministic pipeline: scan documents → extract fields → validate → write spreadsheet.

## Workflow

1. **Discover documents** — glob `$SOURCE_DIR` for `*.pdf`, `*.png`, `*.jpg`, `*.jpeg`
2. **Extract fields** — for each document read/OCR and extract:
   - `vendor` (company name)
   - `date` (normalize to YYYY-MM-DD)
   - `amount` (numeric, preserve currency symbol)
   - `invoice_number` (as printed; `null` if absent)
   - `category` (auto-classify: travel, office, software, meals, other)
3. **Validate** — flag anomalies before writing:
   - Duplicate `invoice_number` across documents
   - `amount` = 0 or negative
   - `date` more than 90 days in the past or any future date
   - Missing required fields (`vendor`, `date`, `amount`)
4. **Write spreadsheet** — create `$OUTPUT_FILE` with columns:
   `File | Vendor | Date | Amount | Currency | Invoice# | Category | Flag`
   - Sort by `Date` ascending
   - Highlight flagged rows (add `[FLAG: reason]` in `Flag` column)
5. **Print summary** — total count, total amount per currency, flagged count

## Input Contract

```text
$SOURCE_DIR/
  *.pdf | *.png | *.jpg | *.jpeg   — invoice/receipt files
```

## Output Contract

```text
$OUTPUT_FILE.xlsx    — populated spreadsheet, sorted by date
stdout               — summary: N docs processed, N flagged, totals by currency
```

## Constraints

- Do NOT move or delete source files
- Do NOT push to accounting system — output only (human reviews before upload)
- If a document cannot be read, add row with `[UNREADABLE]` flag and continue
- Currency: preserve original; do not convert
