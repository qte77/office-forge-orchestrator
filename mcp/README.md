# MCP Server Configuration

Pre-configured MCP server definitions for business APIs. Copy relevant configs to your Claude Code MCP settings or run:

```bash
../scripts/mcp-setup.sh   # Interactive setup
```

## Available Configs

| Config | Servers | Domain |
|--------|---------|--------|
| `accounting.json` | Stripe, Xero, QuickBooks, FreshBooks | Payments + bookkeeping |
| `productivity.json` | Google Workspace, Slack, Notion | Email + communication |
| `crm.json` | HubSpot, Salesforce | Client management |
| `documents.json` | Word MCP, Excel MCP, DocCreator | File manipulation |

## Usage

Each `.json` file contains `mcpServers` entries compatible with Claude Code's `.mcp.json` format. Merge the servers you need into your project's `.mcp.json` or user-level CC config.

## Sources

- [CC-business-api-integrations.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/plugins-ecosystem/CC-business-api-integrations.md) — Full landscape with auth details
- [CC-office-document-skills.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/plugins-ecosystem/CC-office-document-skills.md) — Document skill ecosystem
