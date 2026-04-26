# Codespaces

Operator notes for running office-forge-orchestrator inside GitHub
Codespaces. This doc currently covers GitHub token precedence only —
devcontainer lifecycle, secrets management, and MCP credential
injection sections will land as the corresponding wiring matures (see
the Status section at the bottom).

## Token precedence — what wins when multiple are set

When more than one credential source is present, both `gh` and `git`
follow this precedence:

1. **`GITHUB_TOKEN`** env var — wins outright if set
2. **`GH_TOKEN`** env var — wins over hosts.yml
3. **hosts.yml OAuth token** — used only when neither env var is set

The trap: `GITHUB_TOKEN` or `GH_TOKEN` set in your environment
**silently shadows** the hosts.yml OAuth token. If the env-var token has
narrower scope than the OAuth one, cross-repo writes can fail with `403`
even though `gh auth status` looks healthy.

### Convention: `GH_PAT` as the named override

Standardize on a single named env var, `GH_PAT`, as the *intentional*
override. The intended `containerEnv` wiring in
`.devcontainer/devcontainer.json` is:

```json
"containerEnv": {
    "GH_PAT": "${localEnv:GH_PAT}",
    "GH_TOKEN": "${localEnv:GH_PAT}"
}
```

When you want write access through a fine-grained PAT, set `GH_PAT` in
your local environment. Everything else flows from there. No need to
set `GITHUB_TOKEN` or `GH_TOKEN` directly.

> **Status note:** the office-forge devcontainer does not yet ship the
> `containerEnv` block above — it has only `onCreateCommand: make
> setup_all` and dotfiles wiring. The convention is documented here
> first; the wiring will follow in a separate PR.

### Escape hatch: explicitly drop env precedence

When env-var precedence must be dropped (e.g. third-party install
scripts that fight your token), prefix the command with explicit
clearing:

```bash
GITHUB_TOKEN= GH_TOKEN= some-command
```

This is the canonical pattern for any automation that must run under a
different token (or no token at all).

## See also

- [`docs/pat-scoping.md`](pat-scoping.md) — fine-grained PAT scopes,
  branch protection, push-protection checklist
- `qte77/qte77/docs/gpg-signing.md` — signed-commit policy that pairs
  with the PAT-scoping branch-protection rule

## Status

This document currently covers token precedence only. The following
sections are intentionally deferred until the corresponding wiring
exists or scope expands:

- **Devcontainer lifecycle** (`onCreateCommand`, `postAttachCommand`)
- **Rebuild / Management** (`gh codespace rebuild|list|stop|ssh|delete`)
- **Secrets** (Codespaces user-secret scoping for `GH_PAT` and
  business-API credentials consumed by the MCP servers)
- **Token scopes** (capability table for `GITHUB_TOKEN` vs `GH_PAT`)
- **Business-API credential injection** (the env vars referenced by
  `mcp/*.json` configs — Stripe, HubSpot, Xero, QuickBooks,
  FreshBooks, Google Workspace, Composio)
- **Ports and Forwarding**
