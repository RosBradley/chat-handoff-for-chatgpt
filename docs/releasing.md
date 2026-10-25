# Building and releasing

## Local build

Run validation, tests and scripts/build.py from README.md. The output directory
contains only chat-handoff-plugin-VERSION.zip and SHA256SUMS.txt. The checksum
file contains one entry for that plugin ZIP. Archives use fixed metadata and
sorted entries for repeatable bytes.

The plugin contains only the manifests, skill and license/notice. It excludes
local handoffs, generated installations, Git internals and secrets. Developers
can clone the repository or use GitHub's automatic source downloads.

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
The plugin ZIP is the installation download for ordinary ChatGPT users and
already includes the skill. Publish only that ZIP and its checksum file. GitHub
also displays automatic Source code downloads; these are for developers.

The release workflow names the plugin ZIP explicitly so older archives left in
a local output directory cannot be uploaded accidentally.

CI runs validation, unit tests and builds on pushes and pull requests.
The release workflow runs for a vMAJOR.MINOR.PATCH tag and checks that the tag
matches the manifest. Only deliberately push a release tag when ready to publish.

The release job publishes build artifacts using the repository's GitHub token.
Repository policies may require enabling Actions or granting release permissions.
Hosted validation and release workflows passed for v1.1.2. Verify the workflow
results and uploaded assets for every future release.

## Public plugin directory

A GitHub release is not a public OpenAI plugin-directory submission. This
repository does not supply verified public listing URLs, support policy,
privacy policy, branding or submission approval. Complete that separate
process if public directory publication is requested.
