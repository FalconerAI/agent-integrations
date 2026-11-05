# Falconer OpenAI plugin 0.1.2

[Download the plugin ZIP](falconer-openai-plugin-0.1.2.zip).

This release adds five positive and three negative review scenarios to the [readable submission manifest](plugin.json).
The hosted MCP endpoint, public OAuth client, bundled skill, icons and other packaged files are unchanged from 0.1.1.
The 0.1.1 archive remains unchanged.

SHA-256: `ac2222148b585e43b5df2d9107b4cb5f363741170ed4d62cb1b75344b13a15bb`.

## Maintained source and build

Edit the [maintained OpenAI manifest](../../../../plugins/falconer/.openai-plugin/plugin.json) when changing review cases or listing metadata.
The manifest in this release folder is a generated snapshot.
The [package builder](../../../../scripts/build-openai-plugin.py) assembles the OpenAI metadata, connection settings, README and shared skills/assets from source.
It reproduces this existing archive byte-for-byte and refuses to overwrite archived versions with different contents.
See the [source build instructions](../../../../README.md#openai-directory-package).

## Review scenarios

Positive cases cover current format guidance, search, document reading and citations, formatted document creation, and targeted editing.
Each document-writing case creates its own clearly named private disposable sample document; no existing named customer document or third-party integration is required.
The search case passes only after the created document actually appears in search, allowing for indexing delay.
Negative cases cover inaccessible workspace data, ambiguous destructive cleanup, and unsupported bank transfers.

## Validation and remaining review materials

The ZIP integrity, metadata shape, required fields, exact five/three counts and unchanged packaged files have been checked locally.
These scenarios are expected behavior, not live execution receipts.
Run them in ChatGPT with the dedicated OpenAI reviewer account before submitting for final review.
Provide the private demo login and account/workspace setup through Review details, and ensure the video walkthrough demonstrates the submitted cases.
No credentials, customer content or private account identifiers are included in this public package.
A Google OAuth review video or previously tested Google connection does not establish that these ChatGPT plugin cases have passed.

See [OpenAI submission requirements](https://developers.openai.com/plugins/deploy/submission) for the review fields.
