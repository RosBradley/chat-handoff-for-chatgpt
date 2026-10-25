# Chat Handoff for ChatGPT and Codex

A ChatGPT plugin for moving chat and project work to new conversations or other
AI tools, preserving context, decisions, files, and next steps.

[GitHub repository](https://github.com/RosBradley/chat-handoff-for-chatgpt)

**Repository version: 1.1.2.** Plugin and skill ID: `chat-handoff`.
Adapted from Chat Handoff for Claude v0.3.5 under its MIT license.

## Why use Chat Handoff?

Chat Handoff gives repeated moves between chats and AI tools a consistent
process, so you do not have to remember and explain every migration step.
It is most useful when work spans several chats, files and decisions, or when
you switch tools regularly.

- **Preserve the reasoning behind the work.** Carry forward accepted decisions,
  constraints, rejected approaches and unfinished tasks.
- **Make gaps visible.** Check which selected chats and files are accessible,
  explain what to collect, and label incomplete project exports.
- **Bring usable files.** Full exports include accessible supporting files and
  an inventory, with checks for missing dependencies and package integrity.
- **Make the next step clear.** Supply a reading order and continuation prompt
  that the receiving AI can use without this skill installed.

For a short, simple chat, asking an AI for a continuation summary may be enough.
The skill's value grows with the amount of context to preserve and how often
you move work. It cannot grant extra access or guarantee a complete migration
or lower token usage.

## Install in ChatGPT

Use the ready-made **`chat-handoff-plugin-1.1.2.zip`**. You do not need Codex,
Python, Terminal or an API key for this installation.

This route requires **Plugin Creator** to be available in your ChatGPT account
or workspace. It works through a ChatGPT conversation where plugin creation
is enabled; it does not require switching to Codex.

1. Download the plugin ZIP from the project's
   [GitHub Releases](https://github.com/RosBradley/chat-handoff-for-chatgpt/releases),
   or use the maintainer-supplied ZIP if no release asset is available. Keep it zipped.
2. Start a ChatGPT chat, type `@`, and select **Plugin Creator**.
3. Attach the ZIP and send:

   > Install the attached Chat Handoff package as a private plugin in my current
   > account or workspace. Preserve its bundled skill and supporting files. If
   > I already have an editable Chat Handoff plugin, update that one instead of
   > creating a duplicate. Tell me if installation is unavailable.

4. Open the returned plugin link and complete any installation prompt. Start a
   new chat, select **Chat Handoff** from the `@` menu, and try `.push?`.

Uploading a ZIP alone does not install it; wait for the saved plugin link and
confirm it appears in the new chat. If Plugin Creator is missing, see
[installation help](docs/setup.md#if-plugin-creator-is-unavailable).

Choose the release asset named above; GitHub's automatic **Source code (zip)**
contains the repository files. Creating the repository or pushing source does
not publish the plugin download. A public ChatGPT plugin-directory listing has
not been published as part of this project preparation.

See [setup](docs/setup.md) for updates, troubleshooting and local Codex installation.

## Commands

| Request | Alias | Result |
| --- | --- | --- |
| `handoff [name]` | `.push [name]` | Save a short Markdown handoff for a fresh chat. |
| `handoff?` | `.push?` | Assess whether this is a good stopping point. |
| `pickup [name]` | `.pull [name]` | Read a handoff and continue the next authorized step. |
| `fold <name>` | `.merge <name>` | Review a side chat and apply approved items. |
| `handoffs` | `.status` | List handoffs visible in the selected scope. |
| `transfer [name] [to <AI>]` | `.export [name] [to <AI>]` | Package project context and accessible files in a ZIP for another AI. |
| `handoff project-name to Claude` | `.push project-name to Claude` | Use the same full-package transfer as .export. |
| `export project project-name` | Natural-language request | Snapshot available project context and files; keep this chat active. |

These are instructions to the assistant, not shell commands. Plain git
`push`, `pull` and `merge` retain their ordinary meaning.

Use `.push my-project` for a lightweight handoff that uses the skill without
building an archive. Use `.export my-project to Claude` or
`.export my-project to Codex` to automatically package the scoped work, current
files, file inventory and continuation prompt. `.export` also works without a
name or destination when the current scope is clear. It creates the package;
you carry it to the receiving AI. It does not send data to another service.

All required accessible project files are included in a full transfer; missing
material is reported. Ordinary `.push` does not trigger a repository inventory,
ZIP build or checksums. Both modes preserve constraints and next steps. No
fixed token savings are promised.

For `export project [name]`, the coordinator checks coverage of the chats you
want to move. If it cannot read one, it gives you a named handoff request to run
in that chat and lists any files to bring back. It assembles what is available,
labels incomplete packages **Partial project export**, and keeps the original
project and chats active as backups.

## What carries forward

- Goal, acceptance criteria and user-provided project instructions.
- Accepted decisions, constraints, unresolved questions and next action.
- Exact working baselines, accessible supporting files and validation results.
- Rejected or completed approaches, so they are not repeated.
- A file inventory that explicitly identifies missing inputs.

Plain handoff/.push creates a short Markdown record. Full transfer/.export includes
`START-HERE.md`, `HANDOFF.md`, optional `PROJECT-CONTEXT.md`,
`FILE-MANIFEST.csv` and supporting files. The receiving AI gets a paste-ready
prompt; it does not need this plugin. See [transfer format](docs/transfer-format.md).

## What this does not promise

It does not copy native chat histories automatically, recreate a service's
project settings, reach unseen conversations, or synchronize accounts.
File retrieval, durable saving and chat search depend on the host's actual tools.
A stale-chat reminder works only while the workflow is active and can see
relevant state. Separate records reduce collisions but do not provide atomic
locking. Missing required files make a transfer partial.

No fixed token, cost or speed savings are claimed. The benefit is deliberately
preserving the information needed to continue.

## One source, multiple packages

Maintain [skills/chat-handoff](skills/chat-handoff/) only. The installer creates
a local copy for Codex discovery; build scripts package that same source.

| Location | Purpose |
| --- | --- |
| [skills/chat-handoff/SKILL.md](skills/chat-handoff/SKILL.md) | Core workflow. |
| [plugin.json](plugin.json) | Portable plugin manifest. |
| [.codex-plugin/plugin.json](.codex-plugin/plugin.json) | Codex compatibility manifest. |
| [AGENTS.md](AGENTS.md) | Repository instructions for Codex. |
| [docs](docs/) | Setup, migration, transfer format, release and validation guides. |
| [examples](examples/) | A complete local exercise with source data. |
| [scripts](scripts/) | Installation, validation and package building. |
| [tests](tests/) | Packaging and installation regression checks. |

## Develop in Codex

Clone the [repository](https://github.com/RosBradley/chat-handoff-for-chatgpt)
or extract the full source ZIP. Open the
`chat-handoff-for-chatgpt` folder in Codex and ask it to read `AGENTS.md` and
`docs/CODEX-HANDOFF.md` before making changes.
To install the skill for this local repository, run:

```bash
python3 scripts/install_skill.py --scope repo
```

Use `$chat-handoff` in Codex. For installation across your local projects, use
`--scope user` instead. Python 3.10 or newer is required for these local scripts;
on Windows, use `py -3` in place of `python3`. See [setup](docs/setup.md) for details.

## Validate and build (maintainers)

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

Builds produce three ZIPs and checksums in `dist/`: full source, plugin and
standalone skill. Building never publishes or updates an installed account
plugin. CI checks pushes and pull requests. Release publication runs only for
an intentionally pushed version tag; see [releasing](docs/releasing.md).

## Documentation

This README is the starting point. Detailed guides are in `docs/`, with a
worked example in `examples/` and the assistant's workflow in `skills/chat-handoff/`.

- [ChatGPT installation, updates and Codex setup](docs/setup.md)
- [Transfer package contents and project coverage](docs/transfer-format.md)
- [Changes from the Claude repository](docs/migration-from-claude.md)
- [Worked example](examples/README.md)
- [Design and maintenance](docs/design.md)
- [Validation and remaining checks](docs/validation.md)
- [Packaging and releases](docs/releasing.md)
- [Contribution guidance](CONTRIBUTING.md)

The original license is preserved in [LICENSE](LICENSE). Attribution and the
reviewed source fingerprint are in [NOTICE.md](NOTICE.md).
