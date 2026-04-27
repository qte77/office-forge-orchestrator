# Project Templates

Scaffold new office projects with pre-configured structure, skills, and MCP servers.

## Usage

```bash
# Create a new client engagement project
cp -r templates/client-engagement/ ~/office/client-acme/

# Create a quarterly close project
cp -r templates/quarterly-close/ ~/office/q1-2026-close/
```text

Then add the new project path to `projects.conf`.

## Available Templates

| Template | Contents | Use Case |
|----------|----------|----------|
| `client-engagement/` | Contracts, invoices, correspondence, reports + CRM/accounting/documents MCP + CLAUDE.md | New client projects |
| `quarterly-close/` | Financial folders + accounting MCP + report skill | Recurring financial close |
| `hiring-pipeline/` | Candidates, offers, onboarding folders + HR skill | Open positions |

## client-engagement

Includes pre-configured `/loop` patterns for recurring client tasks:

```
/loop 30m check invoices/ for new files and update payment log
/loop 1h scan correspondence/ for unresolved action items
/loop 4h draft weekly status report for client
```text

See [client-engagement/README.md](client-engagement/README.md) for full setup instructions.
