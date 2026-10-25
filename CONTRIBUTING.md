# Contributing

Start with AGENTS.md. Edit the maintained files in skills/chat-handoff, not a
generated installation. Describe the concrete problem, changed behavior and
how you validated it.

For documentation-only edits, run validation. For installer or build changes,
also run the unit tests and build packages. Use temporary directories for tests.

For workflow changes, try realistic prompts with the relevant files supplied:
a complete pickup, an incomplete transfer, a conflicting writer and a fold with
unverified proposals. Record what was actually tested. Automated packaging tests
do not establish model behavior across products.

For a versioned release, update both manifests, the skill Version line and
CHANGELOG.md together. Follow docs/releasing.md. Do not copy private conversations
or project handoffs into examples.
