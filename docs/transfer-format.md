# Transfer format

The authoritative instructions are in
[portable-transfer.md](../skills/chat-handoff/references/portable-transfer.md).

Plain handoff/.push creates a concise Markdown record. Use
`.export [name] [to <AI>]` (or `transfer [name] [to <AI>]`) for an automatic ZIP
of the scoped context and accessible files. `handoff [name] to <AI>` and
`.push [name] to <AI>` select that same full-transfer mode. `export project`
uses the same package format but keeps the current chat active.

For a project export, inventory the chats selected by the user and record which
can be read. Create one handoff per readable chat. For inaccessible or partial
chats, provide a named `.push <chat-name>` request, tell the user to keep that
source chat active as a backup, and ask them to return the handoff plus any
unavailable referenced files to the coordinator. If no project chat inventory
is accessible, ask the user which chats to include. Continue with accessible
material and label interim packages **Partial project export**. Preserve the
original project and chats as backups; exporting does not close or archive them.

For a full transfer, use these relative paths:

| File | Purpose |
| --- | --- |
| START-HERE.md | Scope, reading order, missing inputs and continuation prompt. |
| HANDOFF.md | Current decisions, open work and next step. |
| PROJECT-CONTEXT.md | Project instructions and accepted constraints, when needed. |
| FILE-MANIFEST.csv | Inventory, provenance, inclusion status and actual hashes. |
| files/ | Accessible supporting files needed to continue. |
| handoffs/ | Workstream records for larger projects. |

The format identifier is chat-handoff/1. The manifest columns are path, status,
required_for_next_step, source_reference, version_or_date, sha256 and notes.
Allowed inclusion statuses: included, reference-only, missing and excluded.

Hashes are computed from actual included bytes when tools allow. They detect
byte changes, not factual reliability. Missing required material makes a
transfer partial. Do not substitute a sandbox link for an included file.

For a lightweight handoff or an explicitly requested Markdown-only transfer,
a Markdown record with a continuation prompt is sufficient. It must still state
missing dependencies. Explicit .export creates a ZIP even for a text-only task;
its supporting file list may be empty. No receiving service needs to understand
the command pickup to follow the prompt.
