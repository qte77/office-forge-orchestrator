# Client Engagement Template

Scaffold for a new client project. Pre-configured with folder structure, MCP
servers for CRM/accounting/documents, and agent instructions.

## Usage

```bash
# Copy to your projects directory
cp -r templates/client-engagement/ ~/office/client-acme/

# Add to office-forge projects registry
echo "/home/user/office/client-acme" >> projects.conf

# Start CC in the engagement context, with the office-forge skills loaded
cd ~/office/client-acme/ && claude --add-dir /path/to/office-forge-orchestrator
```

## Folder Structure

```
client-engagement/
├── README.md              # This file
├── AGENTS.md              # Agent instructions for this engagement
├── .mcp.json              # Pre-configured MCP servers
├── contracts/             # Signed agreements, SOWs, NDAs
├── invoices/              # Issued invoices and payment records
├── correspondence/        # Emails, meeting notes, client comms
└── reports/               # Deliverables, status reports, analyses
```

## MCP Servers Included

See `.mcp.json` for pre-configured servers:

- **CRM** — contact and deal management
- **Accounting** — invoice creation and financial tracking
- **Documents** — file access across the engagement folders

## Recurring Tasks (via /loop)

Once CC is open in this project, use `/loop` for automatic recurring tasks:

```
/loop 30m check invoices/ for new files and log payment status
/loop 1h summarize new correspondence and flag action items
/loop 4h generate client status report from reports/ folder
```

## Getting Started

1. Copy this template to your client project folder
2. Edit `AGENTS.md` with client-specific context (name, contacts, scope)
3. Configure `.mcp.json` with actual API credentials
4. Add the project path to `projects.conf`
5. `cd` into the project and run `claude --add-dir /path/to/office-forge-orchestrator`
   (or use `scripts/sessions.sh`, which passes it for you)

> **Keep `AGENTS.md` as the only instructions file.** Claude Code reads
> `AGENTS.md` only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or
> `CLAUDE.local.md` in the project folder or any folder above it. Adding a
> `CLAUDE.local.md` for personal notes therefore stops Claude from reading
> `AGENTS.md`, unless **Project instructions** in `/config` is set to
> `claude-md-and-agents-md`. See [When Claude Code reads AGENTS.md][agents-md].

[agents-md]: https://code.claude.com/docs/en/memory#when-claude-code-reads-agents-md
