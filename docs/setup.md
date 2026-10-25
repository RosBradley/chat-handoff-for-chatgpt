# Installation and setup

## Install in ChatGPT

Use **chat-handoff-plugin-1.1.1.zip**, the ready-made plugin download. There is
nothing to build, and this route needs no Codex, Python, Terminal or API key.
Keep the ZIP intact when attaching it.

Plugin Creator must be available in your ChatGPT account or workspace, with
permission to create and use plugins. The conversation can be in regular Chat
or Work where those features are enabled.

1. Open [GitHub Releases](https://github.com/RosBradley/chat-handoff-for-chatgpt/releases)
   and choose **chat-handoff-plugin-1.1.1.zip** under the release's assets.
   If no release asset is available yet, use the ZIP supplied by the maintainer.
   GitHub's automatic **Source code (zip)** contains the repository files.
2. Start a new ChatGPT chat. Type `@`, search for **Plugin Creator**, and select it.
3. Attach the ZIP and send this request:

   > Install the attached Chat Handoff package as a private plugin in my current
   > account or workspace. Preserve its bundled skill and supporting files. If
   > I already have an editable Chat Handoff plugin, update that one instead of
   > creating a duplicate. Tell me if installation is unavailable.

4. Follow Plugin Creator's prompts. Open the returned plugin link and complete
   any installation prompt. Start a new chat and select **Chat Handoff** from
   the `@` menu.

The installed package supplies the skill, its references and templates. Simply
attaching a ZIP or pasting SKILL.md into a chat does not persistently install it.
Confirm a saved plugin link was returned and that Chat Handoff is selectable
in the new chat. Installation applies to the selected account or workspace;
it does not install into your other accounts automatically.

### Check it works

In the new chat, select Chat Handoff and ask it to list its supported commands
and installed skill version without creating files. This package's version is
1.1.1. Then try `.push?`, which assesses handoff readiness without saving anything.
For a useful first task, use the skill in a conversation containing work you
want to carry forward.

If the plugin does not appear, check the account/workspace, whether installation
finished, and whether you started a new chat. Ask Plugin Creator to inspect the
saved plugin rather than create another copy. If it reports saving as unavailable
or failed, the installation is not complete.

### Update an existing plugin

Download the newer plugin ZIP. In Plugins, open Chat Handoff and choose
**Edit Plugin** if available. Attach the new ZIP and ask it to update this
existing plugin while preserving its identity. Complete the prompts, then start
a new chat and check the installed version. Editing requires access to that plugin.

### If Plugin Creator is unavailable

There is no verified universal **Create skill > Upload ZIP** menu for regular
ChatGPT in this guide. The ZIP cannot enable plugin features that your account
does not have. In a managed workspace, check with the administrator if plugin
creation is disabled. A published or shared plugin may be installable without
creating your own, but this project has no public directory listing yet.

For use in one conversation, unzip the package and attach SKILL.md plus the
Markdown files in its references/ and assets/ folders. They are inside
chat-handoff/skills/chat-handoff/. Ask ChatGPT to follow those instructions for
your handoff task. If it cannot read an attachment, paste the relevant text.
This fallback applies to that conversation; it does not install a reusable skill.
Available file tools still determine whether it can create a downloadable ZIP
or needs to provide copyable handoff text.

### Which download?

| File | Intended use |
| --- | --- |
| chat-handoff-plugin-1.1.1.zip | ChatGPT Plugin Creator installation above. |
| chat-handoff-for-chatgpt-1.1.1.zip | Full source repository for development or the local Codex installer. |
| chat-handoff-skill-1.1.1.zip | Standalone skill folder for clients that explicitly support that format. |

The plugin package contains the skill; you do not also need to install the
standalone skill. Avoid enabling both copies in the same scope.

### Basis and availability

Checked 2026-10-24 against OpenAI's [Build plugins](https://learn.chatgpt.com/docs/build-plugins),
[Plugins](https://learn.chatgpt.com/docs/plugins) and
[package format](https://developers.openai.com/plugins/build/plugins), plus the
available Plugin Creator package-save workflow. Plugin Creator accepts a prepared
skills-only package and saves a private plugin in the active workspace, or the
personal account when no workspace is active.

This is a supported workflow with account-dependent availability, not a claim
that every plan has the same controls. Package validation does not establish
successful installation in a different user's account. See [validation](validation.md).

## Install locally in Codex

These steps are for local Codex users. ChatGPT users can use the installation
above without running these commands.

Download and extract the full source ZIP. Open a terminal in its
chat-handoff-for-chatgpt folder. Python 3.10 or newer is required; on Windows
substitute `py -3` for `python3`.

For your local user across repositories:

```bash
python3 scripts/install_skill.py --scope user
```

For this repository only:

```bash
python3 scripts/install_skill.py --scope repo
```

For a different local project:

```bash
python3 scripts/install_skill.py --scope repo --project /path/to/project
```

Repository installations use the target project's .agents/skills/chat-handoff
directory. User installation uses ~/.agents/skills/chat-handoff. These discovery
locations follow the [official skill documentation](https://learn.chatgpt.com/docs/build-skills),
checked 2026-10-24. Use $chat-handoff to invoke it explicitly; restart Codex if
the new skill does not appear.

The installer is idempotent for identical files. It refuses to overwrite a
different installation by default. After inspecting that copy, use --replace
to preserve it outside the skill discovery directory and install the new copy.
Re-run installation after changing the maintained source.

Choose one active installation in a scope; avoid enabling a local copy and a
plugin copy together. Extracting the source ZIP does not automatically install it.

## Move actual work

Select Chat Handoff in the source conversation and ask:

```text
.export my-project to Claude
```

This creates a ZIP with the scoped context, actual accessible project files,
an inventory and a continuation prompt. Review the reported scope and missing
files. In the destination, extract or attach the package as that service allows,
then use the prompt in START-HERE.md. The receiving AI does not need this plugin.

For a fresh chat with a short Markdown handoff, use `.push my-project`.
For a project snapshot that keeps the source active, use `export project my-project`.
The older `handoff my-project to Claude` spelling still selects the full export.

For a coding project, retain repository identity, current commit and relevant
uncommitted work. A remote link does not make local edits available elsewhere.

## Develop the source in Codex

The repository is [RosBradley/chat-handoff-for-chatgpt](https://github.com/RosBradley/chat-handoff-for-chatgpt).
Once the initial source is uploaded, contributors can clone it:

```bash
git clone https://github.com/RosBradley/chat-handoff-for-chatgpt.git
cd chat-handoff-for-chatgpt
```

Use an empty destination for the clone. To contribute through your own GitHub
copy, fork the repository first and clone your fork's URL instead.

Open that local folder in Codex and ask it to read AGENTS.md and
docs/CODEX-HANDOFF.md before making changes. Build commands are in the README's
maintainer section; ordinary ChatGPT users download the already-built plugin
package. The source ZIP is also available to seed the initial repository or
inspect the code without Git history.

## Upload the initial source to the existing GitHub repository

The maintainer has created
[chat-handoff-for-chatgpt](https://github.com/RosBradley/chat-handoff-for-chatgpt).
For the first upload to an empty GitHub repository, extract the current source
ZIP into ~/Developer/chat-handoff-for-chatgpt. Preserve any older local folder
separately before extracting. Then run:

```bash
cd ~/Developer/chat-handoff-for-chatgpt
git init -b main
git add .
git commit -m "Initial Chat Handoff release"
git remote add origin https://github.com/RosBradley/chat-handoff-for-chatgpt.git
git push -u origin main
```

These commands assume the extracted folder has not already been initialized
and the GitHub repository has no commits. If it already contains files, clone
it first, copy the source files into that checkout while retaining its .git
directory, and commit and push from there. Do not force-push to replace history.

This source package does not itself upload files or publish release assets.
After the source is on GitHub, use [releasing](releasing.md) to publish the plugin
ZIP for regular ChatGPT users. Do not reuse the Claude repository's remote.
