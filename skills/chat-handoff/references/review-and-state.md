# Review and state

## Fold

Fold/.merge means review into a receiving workstream, not blanket acceptance.

1. Resolve source and recipient. Use an established project rule for the master.
   If there is no receiving work or rule, ask for the intended destination.
   Explicit user instructions override older project routing; record the change.
2. Read source handoff, referenced deliverables and rules. Review unresolved
   items only. Returned items become reviewable again after rework; keep letters.
3. Verify claims, versions, calculations and conflicts against actual current
   evidence. Follow host research requirements for high-stakes claims. Missing
   evidence produces a qualified finding or Return, not a verification claim.
4. For consequential/hard-to-reverse items, independently revisit the source,
   recalculate, examine the strongest counterargument and consequences of error.
   Label deep review. Do not spawn agents without authorization.
5. Present a compact table: letter, proposal, Keep/Change/Toss/Return, reason
   and correction. Retain letters. Prepare a concrete proposed change or diff.
6. Apply only items already explicitly approved, or covered by clear existing
   delegation specifying what may be accepted. Otherwise request user choices.
   Explain the fold approval requirement by linking this reference and quoting
   "Apply only items already explicitly approved". Never request approval twice.
7. Re-read receiving files, apply approved edits, verify them, then record source
   verdicts with date, recipient, exact destination/section and source revision.
   If edits succeed but receipts fail, report that partial state. Before retry,
   check receiving files to prevent duplicate insertion.
8. Keep unresolved work. Set returned for returned items; active with explicit
   owner for an ongoing side topic; folded for fully resolved items, preserving
   a short receipt and rejected items/reasons. Use done only for completed scope
   with no open work.

## State and concurrency

Portable statuses: active, waiting, continuing, returned, folded, done.
Accept legacy waiting-for-pickup, continuing-in, returned-from, folded-into and
merged-into equivalents. Staleness is relative to a conversation, not merely
a status word. A successful pickup makes this chat current even if From still
identifies the original author.

New records use a stable workstream UUID, integer revision and per-conversation
owner token generated once and reused while visible. Tokens are internal IDs,
not fabricated native chat IDs. Store chat links only when verified. Copying
preserves lineage; local ownership does not lock another platform.

Re-read before writing; compare revision/version/hash with the last observation.
Use conditional writes where supported. If another writer advanced the record,
preserve both and resolve the conflict. A read-before-write check without
conditional storage is best-effort, not atomic. Keep one record per line;
never a shared mutable status index.

When another chat owns a record, preserve your proposed work in a separate draft.
Identify the conflict and offer to keep separate, add proposals preserving its
owner/status, or explicitly take over. If authorized to add, allocate letters
after the highest ever used (including receipts/rejections); never reuse letters.
Reworked items retain letters. After Z, continue AA, AB, etc.

## Stale guard

When active state proves this conversation was handed off or superseded, warn
before starting conflicting substantive work. Read current state if accessible.
Commands and acknowledgments still work. Continuing status or tag ordering alone
does not establish staleness.

Honor explicit continue-here, reopen or override without further confirmation.
Otherwise retain the pending instruction, explain where work moved, and ask
whether to use the current owner, continue here once, or reopen this conversation.
Explain the pause by linking this reference and quoting "warn before starting
conflicting substantive work". Do not promise an unselected skill intercepts
every message or warns in other apps.

Continue-once leaves this chat stale. Reopen makes it active locally; resolve
shared ownership before replacing a shared record. A warning is not a lock.
Once the user chooses, carry out the pending request rather than losing it.

## Names, renaming and titles

Line: lowercase letters/digits/single hyphens. Normalize spaces to hyphens and
show the result; reject path separators/traversal. A dot suffix is an optional
user-supplied tag, not chronological order. Split at the first dot; never invent
tags. Recognize a legacy last-word tag only when preceding words unambiguously
match an existing line. Exact matches first; clarify ambiguous fuzzy matches.

A different line in handoff renames this chat's own line; retain its tag unless
replaced. Clarify if appended digits/letters could mean a tag instead of rename.
Do not overwrite collisions. Use identity-preserving store rename if supported;
otherwise save/verify the new copy before retaining the old as a redirect or
archive. Do not destroy history for a cosmetic rename.

Optional titles: working <name>; handed_off.<name> or pushed.<name>;
returned.<name>; folded.<name> or merged.<name>; done.<name>.
Match command style. Never claim to see/change native titles without a tool.
