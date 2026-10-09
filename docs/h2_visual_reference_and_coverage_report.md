# H2 Visual Reference and Coverage Report

## Result

No new motion was authored in H2. This is the safe outcome: the official ISLRTC directory URLs for WATER and I, Me were located, but their visual media could not be inspected from this environment. Direct requests on 2026-10-06 timed out after 30 seconds. An official directory listing is provenance, not a pose specification.

| Concept | Exact source URL | Provenance | Visual inspection | H2 state | Motion decision |
| --- | --- | --- | --- | --- | --- |
| WATER | `https://divyangjan.depwd.gov.in/islrtc/listpage.php?type=W` | ISLRTC, DEPwD, Government of India | Not completed: request timed out | NEEDS_REVIEW; LINGUISTICALLY_UNCERTAIN | Retain `signs/water.json` as `MOTION_INCOMPLETE` |
| I | `https://divyangjan.depwd.gov.in/islrtc/listpage.php?type=I` | ISLRTC, DEPwD, Government of India | Not completed: request timed out | NEEDS_REVIEW; LINGUISTICALLY_UNCERTAIN | No motion file |
| ME | `https://divyangjan.depwd.gov.in/islrtc/listpage.php?type=I` | ISLRTC, DEPwD, Government of India | Not completed: request timed out | NEEDS_REVIEW; LINGUISTICALLY_UNCERTAIN | No motion file |

`VERIFIED_VISUAL_REFERENCE`: none. `PARTIALLY_VERIFIED`: none. The individual intake records list every missing visual parameter, including handshape, orientation, location, movement, contact, and start/end pose.

## Coverage

The reproducible H2 evaluator reports no change:

| Measure | Before H2 | After H2 |
| --- | ---: | ---: |
| Playable concepts | 3/14 | 3/14 |
| Covered G3 concept occurrences | 10/110 | 10/110 |
| Technical motion coverage | 9.09% | 9.09% |
| Remaining missing concept occurrences | 100 | 100 |

Remaining top missing concepts are YOU (17), WATER (16), I (15), HELP (12), ME (12), NEED (9), DRINK (7), TOMORROW (6), NOT (3), THANK_YOU (2), and HOW (1).

All remaining concepts are blocked by missing or uninspected authoritative visual references. None is blocked only by avatar motion authoring. If the ranked next three candidates (YOU, WATER, I) were independently visually verified and then safely authored, they would add 48 occurrences and yield 58/110 (52.73%) coverage. The H1 recommended trio (WATER, I, ME) would add 43 occurrences and yield 53/110 (48.18%). These are simulations, not authorization to author.

## Verification

Run `node tools/validate_phase_h2_coverage.mjs` to reproduce the post-H2 coverage decision. Existing G1/G2/G3/H1 regressions were also run; no sign motion or scheduler code changed in H2.

## Next batch

Do not begin a motion batch until an authoritative, directly inspectable visual reference is available. Once it is, re-intake WATER, I, and ME independently; do not infer that the co-listed `I, Me` entry permits sharing a motion. A Deaf/ISL specialist should review variant choice and any avatar approximation before a sign becomes playable.
