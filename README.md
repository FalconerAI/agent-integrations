# Falconer agent integrations

Falconer Agent Integrations packages [Falconer](https://falconer.com) for AI agent clients that support hosted HTTP MCP servers.

This repository is pre-release. Static manifest validation has passed, but live hosted HTTP OAuth smoke tests in Cursor, Claude Code, and Codex are still pending. Do not submit or resubmit marketplace listings from this repository until those client smoke tests pass.

This repository intentionally does not document local stdio MCP installs. Clients are added only after hosted HTTP OAuth is verified end to end.

## Supported clients

| Client | Status | Install surface |
| --- | --- | --- |
| Cursor | Pending live validation | Cursor plugin package and hosted MCP configuration |
| Claude Code | Pending live validation | Claude Code plugin marketplace package |
| Codex | Pending live validation | Codex plugin marketplace package |

## What this integration provides

- Hosted HTTP MCP connection to `https://falconer.com/api/mcp`.
- Agent guidance for reading, writing, and updating Falconer documents safely.
- Falconer-specific Markdown and rich block formatting guidance.
- Marketplace/plugin metadata for Cursor, Claude Code, and Codex.

## Cursor

Falconer is packaged as a Cursor plugin under [`plugins/falconer`](plugins/falconer). The package includes:

- `.cursor-plugin/plugin.json`
- `mcp.json`
- `skills/falconer-knowledge/SKILL.md`

The MCP server configuration is:

```json
{
  "mcpServers": {
    "falconer": {
      "url": "https://falconer.com/api/mcp"
    }
  }
}
```

Live Cursor OAuth, install, `search`, and `read` smoke tests are still required before marketplace submission.

## Claude Code

Add this repository as a Claude Code marketplace, then install the `falconer` plugin from that marketplace.

The Claude package uses hosted HTTP MCP through:

```json
{
  "mcpServers": {
    "falconer": {
      "type": "http",
      "url": "https://falconer.com/api/mcp"
    }
  }
}
```

Live Claude Code OAuth, install, `search`, and `read` smoke tests are still required before treating this package as supported.

## Codex

Add this repository as a Codex plugin marketplace and install the `falconer` plugin. The plugin includes a bundled hosted HTTP MCP configuration and the shared Falconer skill.

Live Codex OAuth, install, `search`, and `read` smoke tests are still required before treating this package as supported.

## Compatibility policy

New clients are added only when all of the following are true:

- The client can connect directly to `https://falconer.com/api/mcp`.
- Hosted HTTP OAuth works end to end.
- `search` and `read` succeed in a smoke test.
- Tool permission behavior is verified for write and admin tools.
- The working path does not require local stdio.

## Security

Do not commit credentials, OAuth tokens, local MCP configuration, customer content, organization IDs, document IDs, screenshots containing private data, or local environment files to this repository.

Report security issues through the process in [SECURITY.md](SECURITY.md).

## License

Code and documentation are licensed under Apache-2.0. Falconer names, logos, and marks are not licensed under Apache-2.0; see [TRADEMARKS.md](TRADEMARKS.md).
