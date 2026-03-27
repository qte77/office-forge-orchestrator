# Project Templates

Scaffold new office projects with pre-configured structure, skills, and MCP servers.

## Usage

```bash
# Create a new client engagement project
cp -r templates/client-engagement/ ~/office/client-acme/

# Create a quarterly close project
cp -r templates/quarterly-close/ ~/office/q1-2026-close/
```

Then add the new project path to `projects.conf`.

## Available Templates

| Template | Contents | Use Case |
|----------|----------|----------|
| `client-engagement/` | Contracts, invoices, correspondence folders + CRM MCP | New client projects |
| `quarterly-close/` | Financial folders + accounting MCP + report skill | Recurring financial close |
| `hiring-pipeline/` | Candidates, offers, onboarding folders + HR skill | Open positions |
