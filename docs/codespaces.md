# Codespaces

Operator notes for running office-forge-orchestrator inside GitHub
Codespaces. It covers the devcontainer lifecycle, rebuilds, codespace
management, ports and GitHub token precedence. Secrets and credential
injection sections will land as the corresponding wiring matures (see
the Status section at the bottom).

## Devcontainer lifecycle

The devcontainer is single-root: one image
(`mcr.microsoft.com/vscode/devcontainers/base:ubuntu`) with one lifecycle
hook, set in `.devcontainer/devcontainer.json`:

```json
"onCreateCommand": "make setup_all"
```

`make setup_all` runs `generate_tasks` (writes `workspace.code-workspace`
from `config/projects.conf`) and then `start_workspace` (runs
`code -r workspace.code-workspace` when the `code` CLI is on the path).

The Dev Container spec runs the lifecycle hooks in this order
([reference](https://containers.dev/implementors/json_reference/)):
`initializeCommand`, `onCreateCommand`, `updateContentCommand`,
`postCreateCommand`, `postStartCommand`, `postAttachCommand`. If one
fails, the later ones are skipped. This repo sets only `onCreateCommand`,
which runs when the container is first created, and again on a rebuild
(see below).

No `postAttachCommand` is configured. It would run each time a tool
attaches to the container; add one only for a step that must repeat on
every reconnect, which nothing here needs today.

The devcontainer also installs the `anthropic.claude-code` VS Code
extension and sets the VS Code dotfiles settings to use
`qte77/dotfiles` (`install.sh`, cloned to `~/dotfiles`).

## Rebuild

A rebuild applies changes made to `.devcontainer/devcontainer.json` to an
existing codespace; new codespaces pick them up automatically
([docs](https://docs.github.com/en/codespaces/developing-in-a-codespace/rebuilding-the-container-in-a-codespace)).

- VS Code: open the Command Palette, run **Codespaces: Rebuild
  Container**, then choose **Rebuild** or **Full Rebuild**.
- CLI:

```bash
gh codespace rebuild          # reuses cached image layers
gh codespace rebuild --full   # clears the cache, pulls fresh images
```

A rebuild runs `onCreateCommand` again. Files under `/workspaces` (this
checkout and your edits) survive; changes outside it, except `/tmp`,
are lost. Anything needed after a rebuild must be set up by the
lifecycle hook or the dotfiles.

## Management

Run from any machine with the GitHub CLI; `gh cs` is an alias for
`gh codespace`. Without `-c`, the CLI prompts you to pick a codespace
([docs](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-github-codespaces-with-github-cli)).

```bash
gh codespace create -r qte77/office-forge-orchestrator  # new codespace
gh codespace list                                       # name, state
gh codespace ssh -c <name>                              # shell in
gh codespace logs -c <name>                             # creation log
gh codespace stop -c <name>                             # stop
gh codespace delete -c <name>                           # delete
```

`logs` shows the creation log only, which is where an `onCreateCommand`
failure appears. The CLI docs describe no `start` subcommand; reopen a
stopped codespace from the web or VS Code.

## Ports and forwarding

The devcontainer declares no `forwardPorts`. General behaviour
([docs](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)):

- A port is forwarded automatically when a process prints a
  `http://localhost:PORT` URL to the terminal.
- Forward one by hand from the **Ports** tab, or with the CLI.
- Forwarded ports are private (only you) by default. `org` and `public`
  can be set; an organization policy may restrict them, and anyone with
  the URL can open a `public` port.
- To forward a port in every codespace from this repo, add it to
  `forwardPorts` in `devcontainer.json`, then rebuild existing
  codespaces.

```bash
gh codespace ports                                    # list forwarded ports
gh codespace ports forward <remote>:<local> -c <name>
gh codespace ports visibility <port>:private -c <name>
```

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

This document covers lifecycle, rebuild, management, ports and token
precedence. The following sections are intentionally deferred until the
corresponding wiring exists or scope expands:

- **Secrets** (Codespaces user-secret scoping for `GH_PAT` and
  business-API credentials consumed by the MCP servers)
- **Token scopes** (capability table for `GITHUB_TOKEN` vs `GH_PAT`)
- **Business-API credential injection** (the env vars referenced by
  `mcp/*.json` configs — Stripe, HubSpot, Xero, QuickBooks,
  FreshBooks, Google Workspace, Composio)
