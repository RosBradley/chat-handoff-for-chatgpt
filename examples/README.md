# Worked example: planning a workshop

This fictional exercise includes all source files. Copy the workshop directory
to a temporary workspace before asking an assistant to modify it.

1. Ask it to follow the skill and `pickup workshop`, using
   [Handoff-workshop.md](workshop/handoffs/Handoff-workshop.md).
   It should continue the open checklist using the supplied
   [requirements](workshop/files/requirements.md).
2. In a receiving conversation, ask it to `fold estimate` into
   [plan.md](workshop/files/plan.md), using
   [Handoff-estimate.md](workshop/handoffs/Handoff-estimate.md) and
   [hours.csv](workshop/files/hours.csv).
3. Review the proposed verdicts and edits. Approve the items you want applied.
4. Ask for `export project workshop`. Verify it includes only this example's
   files and identifies the unavailable venue confirmation.

The estimate proposes 120 hours. Its source rows total 100, so the receiving
assistant should correct the figure. A proposed November 1 date lacks venue
confirmation and should remain pending. Those findings belong in the review;
they are not permission to accept other unsupported claims.

The example [rules](workshop/handoffs/Handoff-rules.md) are intentionally named
with hyphens for portable links. When using the example as a real workspace,
copy them to handoffs/Handoff rules.md or explicitly identify the file in your
request.
