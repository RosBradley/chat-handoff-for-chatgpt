# What changed from the Claude repository

The supplied source contains documentation, setup instructions, templates,
examples, plugin/marketplace metadata and release automation. Its skill is
v0.3.5 and exactly matches the earlier attachment.

| Original component | ChatGPT/Codex adaptation |
| --- | --- |
| README | Rewritten around continuation and portability; no fixed usage or speed claims. |
| Claude-specific setup | Codex discovery/install commands, plugin package route and Markdown fallback. |
| Claude marketplace metadata | Portable plugin.json and Codex compatibility manifest; no claimed hosted marketplace. |
| Skill | Retains commands, item review, lineage and receipts; uses actual host tools and explicit missing-file coverage. |
| Project-write and chat-search assumptions | Capability discovery; durable files where supported; attachment/paste fallback. |
| Rename/delete behavior | Identity-preserving rename or verified copy plus redirect/archive. |
| Always-on stale guard | Reminder only when the skill and relevant state are available. |
| 400-word handoff cap | Concise summary with supporting context where needed for completeness. |
| Original worked example | Self-contained fictional planning exercise with its source CSV. |
| Release-on-version-change | Explicit version-tag release with validation and tests first. |
| License | Original MIT text retained verbatim. |
| Local runtime settings, prior Git internals, working handoffs | Omitted from the new source and release packages. |

Retained commands: handoff, handoff?, pickup, fold, handoffs and their dot aliases.
Added user-facing workflows: .export/transfer for automatic packages to another
AI, handoff-to-another-AI, and export-project snapshots. Plain .push remains a
lightweight Markdown handoff; an explicit .push to another AI creates a package.

Folding still requires accepted decisions or clear prior delegation. The workflow
must not repeatedly request approval already given. It distinguishes a local
continuation from taking ownership of a shared record.

The archive is evidence of the supplied working tree, not proof of the latest
remote revision. Future upstream changes should be reviewed selectively.
