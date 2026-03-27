# office-forge

Manage office projects, files, and tasks with AI agents — the way [polyforge](https://github.com/qte77/polyforge) manages dev repos.

> **USP**: Unified management layer for office work (invoices, contracts, reports, email) across multiple projects — powered by Claude Code and MCP servers.
>
> **ICP**: Office workers, small business owners, and ops teams juggling multiple projects with repetitive document/financial/communication tasks.
>
> **CTA**: `./scripts/status.sh` — see all your office projects at a glance.

## What This Is

A **management repo** — not a workflow engine. Office-forge:

- **Organizes** office projects in one place (`projects.conf`)
- **Configures** MCP servers for business APIs (accounting, CRM, email)
- **Provides** deterministic skills/templates for repeatable tasks
- **Orchestrates** parallel Claude Code sessions across projects
- **Tracks** status and progress across all managed work

Execution happens through Claude Code (or compatible agents). Office-forge sets up the environment, skills, and project structure — the agent does the work.

## Quick Start

```bash
# See status of all managed projects
./scripts/status.sh

# Open parallel CC sessions — one per project
./scripts/sessions.sh

# Run a task across projects
./scripts/run.sh "Organize all invoices by date" ./projects/accounting/

# Interactive: start CC in a project context with office skills loaded
cd projects/client-acme/ && claude
```

## Project Structure

```
office-forge/
├── projects.conf              # Managed project directories (like polyforge's repos.conf)
├── scripts/                   # Management scripts (status, sessions, run)
├── .claude/skills/            # Deterministic office skills (invoice, contract, report)
├── mcp/                       # MCP server configs for business APIs
├── templates/                 # Project templates (new client, quarterly close, etc.)
└── config/                    # Environment and credential setup
```

## Recurring Tasks (/loop)

The `/loop` command in Claude Code runs a task on a schedule — no cron setup, no scripts, no infrastructure. Just describe what to do and how often.

```bash
# In any office-forge managed project, open CC and run:
/loop 30m check invoices/ for new files and log payment status
/loop 1h summarize new correspondence and flag action items
/loop 4h generate daily financial summary from accounting data
/loop 1d scan contracts/ for upcoming renewal dates and alert
/loop 1w generate weekly client status report and save to reports/
```

This is the core differentiator: **deterministic recurring office tasks via a single command**, without external schedulers or automation platforms.

Practical patterns:

| Frequency | Task | Skill |
|-----------|------|-------|
| Every 30m | Check invoices folder for new files | `invoice-processing` |
| Every 1h | Flag urgent emails and draft responses | `email-triage` |
| Every 4h | Generate financial summary | `financial-report` |
| Daily | Organize new documents by date | `doc-organize` |
| Weekly | Compile client status report | `financial-report` |

Start a loop session in any project:

```bash
cd projects/client-acme/ && claude
# Then in CC:
/loop 1h check correspondence/ for client messages and summarize action items
```

## Skills (Deterministic Workflows)

Skills in `.claude/skills/` define **repeatable, deterministic tasks** that CC executes consistently:

| Skill | Purpose |
|-------|---------|
| `invoice-processing` | OCR → extract → validate → spreadsheet |
| `doc-organize` | Content-aware classify → date-taxonomy rename |
| `offer-generation` | Template + CRM data → populated contract |
| `financial-report` | Accounting pull → analysis → Excel + deck |
| `email-triage` | Categorize → priority flag → draft responses |

Skills are SKILL.md files — deterministic prompts with structured input/output contracts.

## MCP Server Setup

Pre-configured MCP definitions for business APIs. Copy to your CC config or use the setup script.

```bash
./scripts/mcp-setup.sh    # Interactive: select and configure MCP servers
```

See [mcp/README.md](mcp/README.md) for available servers.

## Relationship to Polyforge

| | Polyforge | Office-forge |
|---|-----------|-------------|
| **Domain** | Dev repos | Office projects |
| **Manages** | Git repositories | Project folders, files, tasks |
| **Agents** | CC, Cursor, OpenCode | CC, Cowork, compatible agents |
| **Skills** | Code review, testing, validation | Invoices, contracts, reports, email |
| **MCP servers** | GitHub, filesystem | Accounting, CRM, email, documents |
| **Pattern** | Same | Same — unified config, parallel sessions, status dashboard |

## Research

Based on research in [ai-agents-research](https://github.com/qte77/ai-agents-research):

- [CC-office-worker-workflows.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-community/CC-office-worker-workflows.md)
- [CC-office-document-skills.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/plugins-ecosystem/CC-office-document-skills.md)
- [CC-business-api-integrations.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/plugins-ecosystem/CC-business-api-integrations.md)

## License

Apache-2.0
