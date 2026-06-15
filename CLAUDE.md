# office-forge-orchestrator

Orchestrate parallel AI agents across office projects. See `README.md` for usage.

Scripts in `scripts/` manage all projects listed in `config/projects.conf` (single source of truth).
Config in `config/` handles project list, environment, and credential setup.
Skills in `.claude/skills/` provide deterministic office task workflows.
MCP configs in `mcp/` define business API server connections.
Templates in `templates/` scaffold common project types.
