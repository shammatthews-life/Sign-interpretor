# H33 Repository Checkpoint Audit

**Status:** H32 checkpoint verified; H33 acceptance remains blocked
**Branch:** `r1-articulation-coverage-and-report`
**Audit HEAD:** `b0b11afde3c914a748a96aede43123e4d16a6a36`

The local HEAD is the reported H32 commit, and the H31 commit
`2c2de128b731cb3f59687acd4b0a6ebb09e275e7` is present. The branch is
`r1-articulation-coverage-and-report`; the initial worktree was ahead of its
origin tracking branch by 47 commits. No push, reset, rebase, or merge was
performed.

Ten H32 files already had local, uncommitted edits before H33 work began. Those
changes were preserved. The complete initial list is recorded in
[`data/h33_repository_state.json`](../data/h33_repository_state.json).

## Full-run limitation

The existing H32 benchmark source evaluates a 300-second slice from the
canonical 8,978.9-second WAV and projects a full-video duration. That evidence
is not a completed full-video run. The reported 64.50× result and 139.21-second
duration remain H32 claims, not H33 full-corpus measurements. H33 did not
re-label the projection as a completed run.

The machine had approximately 2.01 GiB available during the CUDA diagnostic
and 2.56 GiB available immediately afterward. A bounded production-ready
full-duration runner, full-corpus WER/CER, event-level dispatch reconciliation,
and cold/warm product TTFS trials remain outstanding. Interactive Chrome
acceptance remains a manual requirement.

See [`data/h33_execution_checkpoint.json`](../data/h33_execution_checkpoint.json)
for machine-readable statuses.
