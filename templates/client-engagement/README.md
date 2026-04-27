# Client Engagement Template

Scaffold for a new client project. Pre-configured with folder structure, MCP
servers for CRM/accounting/documents, and agent instructions.

## Usage

```bash
# Copy to your projects directory
cp -r templates/client-engagement/ ~/office/client-acme/

# Add to office-forge projects registry
echo "/home/user/office/client-acme" >> projects.conf

# Start CC in the engagement context
cd ~/office/client-acme/ && claude
```text

## Folder Structure

```
client-engagement/
├── README.md              # This file
├── CLAUDE.md              # Agent instructions for this engagement
├── .mcp.json              # Pre-configured MCP servers
├── contracts/             # Signed agreements, SOWs, NDAs
├── invoices/              # Issued invoices and payment records
├── correspondence/        # Emails, meeting notes, client comms
└── reports/               # Deliverables, status reports, analyses
```text

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
```text

## Getting Started

1. Copy this template to your client project folder
2. Edit `CLAUDE.md` with client-specific context (name, contacts, scope)
3. Configure `.mcp.json` with actual API credentials
4. Add the project path to `projects.conf`
5. `cd` into the project and run `claude`
