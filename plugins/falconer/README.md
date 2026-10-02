# Falconer

Use Falconer documents from supported agent clients through hosted HTTP MCP.

This plugin package is remote-only and connects to:

```text
https://falconer.com/api/mcp
```

Supported v1 clients are Cursor, Claude Code, and Codex.

The shared `falconer-knowledge` skill discovers guidance through `falconer_knowledge({})` and loads `falconer_knowledge({"topic":"document-format"})` before document authoring.
Load `document-components`, `html-components`, or `diagrams` when using those features.
Clients may also attach the corresponding MCP resources under `falconer://knowledge/`.

The plugin contains workflow instructions; current formatting and component guides come from the connected Falconer server.
Retrieval failures must be reported instead of replaced with an offline formatting snapshot.
