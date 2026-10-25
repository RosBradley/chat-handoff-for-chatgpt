# Design

The assistant follows the skill; local Python scripts install and package it.
There is no hidden transcript collector, hosted database, custom MCP server,
scheduled process or credential store.

## Maintained components

| Component | Responsibility |
| --- | --- |
| skills/chat-handoff/SKILL.md | Commands, evidence, handoff and pickup. |
| references/portable-transfer.md inside the skill | Export/import scope, manifest, validation and destination prompt. |
| references/review-and-state.md inside the skill | Item review, receipts, ownership, staleness and names. |
| assets inside the skill | Handoff and project-rule templates. |
| scripts/install_skill.py | Copy installation with collision checks and backup. |
| scripts/repo_tools.py | Manifests, YAML, links, source allowlist and reproducible ZIPs. |
| scripts/build.py | Local build entrypoint; no publication. |

Keep skills/chat-handoff as the only maintained skill. .agents/skills is a
generated copy ignored by Git. This avoids symlink requirements on Windows.

## State

Records use a workstream identity, revision, owner and explicit status. UUIDs are
internal identifiers, not fabricated platform chat IDs. Statuses are active,
waiting, continuing, returned, folded and done; legacy Claude forms remain
readable. Item letters survive rework and are never recycled.

Concurrency checking uses the best guarantees of the actual store. A versioned
conditional write may reject a stale update. A plain filesystem read followed
by a write is not an atomic distributed lock. Separate workstreams reduce
collisions but do not eliminate competing writers to the same record.

## Portability and boundaries

The transfer's relative files and reading instructions carry the work.
Service-specific IDs may establish provenance but cannot substitute for bytes.
Imported instructions are records, and cannot grant access or authorize
unrelated actions. Raw transcripts are optional supplied evidence, not invented
history. Missing material must remain explicit.
