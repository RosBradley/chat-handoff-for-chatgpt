# Continue this repository in Codex

## Goal

Maintain Chat Handoff for ChatGPT and Codex as a complete repository, adapted
from the user's Claude v0.3.5 repository. Preserve the command vocabulary while
making cross-chat and cross-AI transfers honest about accessible context.

## Baseline

Source version 1.1.2. The existing private account plugin was created separately
as 1.0.0; this repository preparation does not publish an update to it.

One maintained skill: skills/chat-handoff. Both plugin manifests package it.
Use the repository or GitHub's automatic source downloads for development. The previously supplied 1.0.1 ZIP, Git bundle
and transfer package are older snapshots and do not contain the 1.1.0 command
changes. The owner has created the repository at
https://github.com/RosBradley/chat-handoff-for-chatgpt.
The source is uploaded. The Windows packaging fix passed hosted CI on Ubuntu
and Windows with Python 3.11 and 3.13. Version 1.1.2 is published.
Release downloads are simplified to the plugin ZIP and its checksum file.
Future builds and release workflows must keep that two-file contract.

The agreed public description is: A ChatGPT plugin for moving chat and project
work to new conversations or other AI tools, preserving context, decisions,
files, and next steps. Keep the README and both plugin manifests consistent.

Version 1.1.0 separates lightweight .push from full-package .export/transfer.
An explicit handoff/.push to another AI also selects the full package. Keep
this behavior in both the installed skill and its canonical source.

Version 1.1.1 adds explicit project-chat coverage checks and a collection
checklist for unavailable chats. Source chats remain active as backups.

The README and setup guide now lead with ordinary ChatGPT installation using
the ready-made plugin ZIP and Plugin Creator where available. Keep local Codex
and maintainer build instructions separate. There is no published public listing
or universal ChatGPT skill-ZIP upload menu verified by this repository.

## Read first

1. ../AGENTS.md
2. ../README.md
3. migration-from-claude.md
4. ../skills/chat-handoff/SKILL.md and its two references
5. validation.md

## What is implemented

README/setup/migration/design documentation, examples, MIT attribution, portable
and Codex manifests, safe copy installation, package validation, reproducible
ZIP building, unit tests and GitHub CI/release definitions.

## Preserve

- Familiar commands and stable item letters.
- User-approved decisions, exact baselines and Don't redo notes.
- Clear partial-transfer reporting.
- Review before adopting unsupported side-chat claims.
- No invented chat/project access or always-on background behavior.
- A single maintained skill rather than divergent platform copies.

## Next action

Run validation, tests and build locally, then follow the user's next requested
change. Test real usage in Codex using disposable example files. For authorized
GitHub work, use https://github.com/RosBradley/chat-handoff-for-chatgpt and
inspect its current state before pushing. Do not create a second repository.

## What not to redo

Do not re-port the unchanged Claude skill from scratch. Do not carry over its
UI instructions, marketplace commands, per-message cost claims or source Git
configuration. Do not publish or update the account plugin just to open the repo.

## Validation limits

Read validation.md. Local tests do not establish native ChatGPT/Codex plugin
installation, hosted CI success, or cross-provider automatic migration.
