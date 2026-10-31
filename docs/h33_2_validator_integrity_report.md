# H33.2 Validator Integrity Report

The H33.2 validator is distinct from the historical H33/H33.1 validators. It queries Git for the actual branch, HEAD, baseline ancestry, and remote branch SHA; verifies the ten preserved H32 worktree edits remain unstaged; and checks that any staged `docs/report.md` diff contains only the H33.2 appendix. It also hashes current source files, parses generated evidence, and invokes focused tests/regression validators with their real process exit codes. A recorded claim is not treated as proof that its source file or remote ref matches.

The validator reports code/test failures separately from release blockers. Full-video acceptance remains blocked when the resource preflight fails, and browser acceptance remains manual. This validator does not start full-video inference.

`data/h33_2_validator_integrity.json` records actual test command exit codes and assertion counts. The final remote SHA is checked after publication; the validator output is the runtime observation, while the committed branch and GitHub ref remain directly inspectable.
