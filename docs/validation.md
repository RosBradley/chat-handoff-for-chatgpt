# Validation

## ChatGPT installation documentation

On 2026-10-24, the README and setup guide were revised to lead with the prepared
plugin ZIP and the available Plugin Creator package-save workflow. OpenAI's
web documentation confirms conversational plugin creation in Chat or Work where
enabled, account/workspace permissions, and use in a new chat after installation.
The instructions distinguish a saved plugin from an uploaded attachment and
provide a conversation-only fallback when plugin creation is unavailable.

The package layout and included references are checked locally. This documentation
update does not establish a fresh end-to-end installation in a separate regular
ChatGPT account, nor availability on every plan. A user acceptance check remains:
download the plugin asset, use Plugin Creator to save it, then select Chat Handoff
in a new regular ChatGPT chat and verify the version and `.push?` behavior.

## Version 1.1.1

On 2026-10-24, repository validation and all 15 unit tests passed. An isolated
project export exercise had three selected chats: one readable and two
unavailable in another account. It produced a partial package, one verified
handoff for the readable chat, distinct .push collection requests for the other
two, and a checklist for the missing workbook and agenda. The source chats
remained active. Package entries and included hashes were verified.

## Version 1.1.0

Local verification on 2026-10-24 passed repository validation and all 15 unit
tests; source/plugin/skill packages were rebuilt. Two isolated assistant tasks
exercised the updated command selection:

- `.push workshop-to-codex` produced one Markdown handoff with the agreed
  constraints and next step, without an archive despite the destination-like name.
- `.export workshop to Claude` produced a ZIP containing the unchanged plan,
  CSV and binary logo, plus handoff, context, manifest and continuation prompt.
  It marked an unavailable required workbook as missing and the transfer as
  partial, and excluded the environment file. Included hashes were verified.

These checks cover the observed examples, not guaranteed behavior in every host.
The native Mac/Codex and hosted-publication checks below remain outstanding.

## Original baseline

Local verification on 2026-10-22 passed repository validation, all 15 unit tests,
and source/plugin/skill package builds. Repeated builds produced identical ZIP
bytes and matching checksums. This was a Linux run; the host checks below remain
separate.

## Automated checks

Run the commands in README.md. The validator checks JSON/YAML structure, matching
versions and presentation, skill metadata, source inventory and relative file
links. It checks link targets, not Markdown heading fragments or remote URLs.

The unit tests cover installation into a temporary folder, idempotency, changed
installation protection, backup behavior, source-link rejection, deterministic
builds, package content boundaries and malformed metadata/links. They exercise
real copies and ZIP files.

CI is configured for Linux and Windows, with Python 3.11 and 3.13. Local
preparation runs the available Linux Python runtime only. Hosted CI, native
Windows installation and live account-plugin installation require their own
runs. Do not describe the CI matrix as tested until those runs pass.

## Assistant behavior exercises

The initial ChatGPT adaptation was exercised with two isolated assistant runs:

- A legacy Claude handoff lacking its source archive: continued the independent
  checklist task, named the missing file and ignored an old instruction to send
  data elsewhere.
- A fold with supplied arithmetic and a missing confirmation: corrected the
  proposed total, returned the unsupported date and proposed changes before
  editing the receiving file.

Those are limited behavioral checks, not a guarantee across models or hosts.

## Suggested next checks in Codex

Use disposable copies of examples/workshop. Try a handoff and pickup, a fold
with an incorrect figure, two competing record revisions, and export with one
required file removed. Verify that private working files do not enter release
packages and that the receiving assistant respects the accepted constraints.
