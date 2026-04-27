---
name: email-triage
description: Read email threads → categorize by urgency → draft responses for review → flag priorities → identify newsletters for unsubscribe. Use when processing an email backlog.
compatibility: Designed for Claude Code
metadata:
  argument-hint: [mailbox-export-dir] [output-dir]
  allowed-tools: Read, Write, Glob, Bash
  mcp-servers: [filesystem, google-workspace, m365]
---

# Email Triage

**Source**: $ARGUMENTS (defaults: `./emails/` → `./triage/`)

Deterministic pipeline: read threads → categorize → draft → output review package.

## Urgency Categories

| Priority | Label | Criteria |
|----------|-------|----------|
| P1 | `urgent` | Deadline within 24h, financial/legal matter, executive sender |
| P2 | `action-needed` | Requires response or decision, no immediate deadline |
| P3 | `fyi` | Informational only, no action required |
| P4 | `newsletter` | Marketing, subscription, automated digest |
| P5 | `spam` | Unsolicited, phishing indicators, irrelevant |

## Workflow

1. **Discover emails** — read `$SOURCE_DIR` for `.eml`, `.mbox`, or `.json` export files
2. **Parse threads** — group by thread/subject; for each thread extract:
   - `subject`, `sender`, `date` (most recent message), `body` (latest + context)
3. **Categorize** — assign priority label using Urgency Categories table
4. **Draft responses** — for P1 and P2 threads only:
   - Write a concise draft response (≤150 words)
   - Mark draft as `[DRAFT — REVIEW BEFORE SENDING]`
   - Do NOT include personal sign-off — leave placeholder `[Your name]`
5. **Flag newsletters** — for P4 threads, extract unsubscribe link if present
6. **Write outputs**:
   - `$OUTPUT_DIR/triage-summary.md` — all threads sorted by priority with drafts inline
   - `$OUTPUT_DIR/urgent.md` — P1 threads only (quick action view)
   - `$OUTPUT_DIR/unsubscribe-list.md` — P4 newsletter unsubscribe links
7. **Print summary** — count per priority label

## Input Contract

```text
$SOURCE_DIR/
  *.eml | *.mbox | *.json   — exported email files or mailbox dumps
```

## Output Contract

```text
$OUTPUT_DIR/
  triage-summary.md     — full categorized list with response drafts
  urgent.md             — P1-only quick action list
  unsubscribe-list.md   — newsletter unsubscribe links
stdout                  — counts: P1=N, P2=N, P3=N, P4=N, P5=N
```

## Constraints

- Do NOT send any emails — output drafts only for human review
- Do NOT store email content outside `$OUTPUT_DIR`
- Draft responses for P1/P2 only; P3–P5 get categorization only
- If thread body is empty or unreadable, categorize as P3 with note `[body-unavailable]`
- Phishing indicators (mismatched sender domains, suspicious links) → P5 + note `[phishing-suspected]`
