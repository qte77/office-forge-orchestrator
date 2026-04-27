# Client Engagement — Agent Instructions

This project is a client engagement managed by office-forge.

## Context

- **Client**: [CLIENT_NAME]
- **Engagement type**: [consulting | project | retainer]
- **Primary contact**: [NAME, email]
- **Start date**: [YYYY-MM-DD]
- **Scope**: [brief description]

## Folder Conventions

| Folder | Contents | Naming Convention |
|--------|----------|-------------------|
| `contracts/` | Signed agreements, SOWs, NDAs | `YYYY-MM-DD_type_version.pdf` |
| `invoices/` | Issued invoices, payment records | `INV-NNNN_YYYY-MM-DD.pdf` |
| `correspondence/` | Emails, meeting notes, comms | `YYYY-MM-DD_subject.md` |
| `reports/` | Deliverables, status reports | `YYYY-MM-DD_report-type.md` |

## Skills Available

Load these skills from the office-forge `.claude/skills/` directory:

- `/invoice-processing` — extract, validate, and log invoice data
- `/doc-organize` — classify and rename documents by date taxonomy
- `/email-triage` — categorize correspondence and flag action items

## Recurring Tasks

```text
/loop 30m check invoices/ for new files and update payment log
/loop 1h scan correspondence/ for unresolved action items
/loop 4h draft weekly status report for client
```

## Rules

- Never send emails or create invoices without explicit confirmation
- Always validate invoice amounts against contract terms before logging
- Flag any scope-creep signals in correspondence for human review
- Keep correspondence/ entries dated and attributed
