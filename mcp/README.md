# MCP Server Configuration

Pre-configured MCP server definitions for business APIs. Copy relevant configs to your Claude Code MCP settings or run:

```bash
# See issue #11 for interactive setup (planned)
```

## Available Configs

| Config | Servers | Domain |
|--------|---------|--------|
| `accounting.json` | Stripe, Xero, QuickBooks, FreshBooks | Payments + bookkeeping |
| `productivity.json` | Google Workspace (Gmail, Calendar, Drive, Docs, Sheets) | Email + communication |
| `crm.json` | HubSpot, Salesforce (via Composio) | Client management |
| `documents.json` | Office-Word-MCP-Server, excel-mcp-server, mcp-server-doccreator | File manipulation |

## Auth Requirements

### accounting.json

| Server | Auth | Env Vars |
|--------|------|----------|
| Stripe | API key | `STRIPE_API_KEY` |
| Xero | OAuth 2.0 | `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET` |
| QuickBooks | OAuth 2.0 | `QB_CLIENT_ID`, `QB_CLIENT_SECRET`, `QB_REALM_ID` |
| FreshBooks | OAuth 2.0 | `FRESHBOOKS_CLIENT_ID`, `FRESHBOOKS_CLIENT_SECRET` |

### productivity.json

| Server | Auth | Env Vars / Setup |
|--------|------|-----------------|
| Google Workspace | OAuth 2.0 | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` — covers Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, Contacts, Chat. Source: [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) |

### crm.json

| Server | Auth | Env Vars / Setup |
|--------|------|-----------------|
| HubSpot | OAuth 2.0 | `HUBSPOT_PORTAL_ID` — requires HubSpot CLI v7.60.0+. Run `hs mcp setup` to complete OAuth flow. Currently read-only. |
| Salesforce | API key (Composio) | `COMPOSIO_MCP_URL`, `COMPOSIO_API_KEY` — full CRUD via Composio hub. See [composio.dev](https://composio.dev/toolkits/salesforce/framework/claude-code) |

### documents.json

| Server | Auth | Env Vars / Notes |
|--------|------|-----------------|
| Office-Word-MCP-Server | None | No auth required. Source: [GongRzhe/Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server) |
| excel-mcp-server | None | `EXCEL_MCP_PAGING_CELLS_LIMIT` controls paging (default 4000). Source: [negokaz/excel-mcp-server](https://github.com/negokaz/excel-mcp-server) |
| mcp-server-doccreator | None | Multi-format: PDF, DOCX, PPTX, XLSX. Source: [Git-Fg/mcp-server-doccreator](https://github.com/Git-Fg/mcp-server-doccreator) |

## Usage

Each `.json` file contains `mcpServers` entries compatible with Claude Code's `.mcp.json` format. Merge the servers you need into your project's `.mcp.json` or user-level CC config.

## Sources

- [CC-business-api-integrations.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/plugins-ecosystem/CC-business-api-integrations.md) — Full landscape with auth details
- [CC-office-document-skills.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/plugins-ecosystem/CC-office-document-skills.md) — Document skill ecosystem
