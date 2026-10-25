# Building and releasing

## Local build

Run validation, tests and scripts/build.py from README.md. The output directory
contains a source ZIP, a plugin ZIP, a standalone skill ZIP and SHA256SUMS.txt.
Archives use fixed metadata and sorted entries for repeatable bytes.

The source package includes repository documentation and tests. Plugin packages
contain only the manifests, skill and license/notice. Neither includes local
handoffs, generated installations, Git internals or secrets.

## Version

Update plugin.json, .codex-plugin/plugin.json, the skill Version line and
CHANGELOG.md together. The root plugin name remains chat-handoff. Release
versions currently use stable major.minor.patch strings.

An existing account plugin is a separate deployment. Building this source does
not update it; use its existing identity and current-release guard when an
update is requested. Do not create a duplicate account plugin for every release.

## GitHub workflows

The source repository is
[RosBradley/chat-handoff-for-chatgpt](https://github.com/RosBradley/chat-handoff-for-chatgpt).
Publish downloads on its
[Releases page](https://github.com/RosBradley/chat-handoff-for-chatgpt/releases).
The plugin ZIP is the installation download for ordinary ChatGPT users; the
source ZIP is for repository setup and development.

CI runs validation, unit tests and builds on pushes and pull requests.
The release workflow runs for a vMAJOR.MINOR.PATCH tag and checks that the tag
matches the manifest. Only deliberately push a release tag when ready to publish.

The release job publishes build artifacts using the repository's GitHub token.
Repository policies may require enabling Actions or granting release permissions.
No hosted workflow has been run as part of the local repository preparation.

## Public plugin directory

A GitHub release is not a public OpenAI plugin-directory submission. This
repository does not supply verified public listing URLs, support policy,
privacy policy, branding or submission approval. Complete that separate
process if public directory publication is requested.
