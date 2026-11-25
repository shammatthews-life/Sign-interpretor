# H1 Sign Coverage Priorities

This is an evidence-based authoring roadmap, not a linguistic validation or motion specification.

## Transparent scoring

`10*G3 corpus frequency + 3*distinct affected sentences + 5*local dictionary entry + 4*existing incomplete motion schema + 8*phrase value; no unmeasured feasibility score.`

The score intentionally awards no points for unmeasured authoring feasibility or uninspected gesture details.

## Current coverage

- Linguistic concepts: 14
- Playable: 3
- Incomplete/not authored: 11
- G3 unavailable concept occurrences: 100

## Top candidates

| Rank | Concept | Frequency | Score | State | Local dictionary | Reference state | Motion state |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| 1 | YOU | 17 | 226 | C. MOTION_INCOMPLETE + reference unavailable | yes | PROJECT_CATALOG_SOURCE_ONLY | NO_MOTION_FILE |
| 2 | WATER | 16 | 217 | B. MOTION_INCOMPLETE + reference available | yes | DIRECTORY_LISTED_POSE_NOT_INSPECTED | incomplete |
| 3 | I | 15 | 195 | B. MOTION_INCOMPLETE + reference available | no | DIRECTORY_LISTED_POSE_NOT_INSPECTED | NO_MOTION_FILE |
| 4 | HELP | 12 | 161 | C. MOTION_INCOMPLETE + reference unavailable | yes | PROJECT_CATALOG_SOURCE_ONLY | NO_MOTION_FILE |
| 5 | ME | 12 | 161 | B. MOTION_INCOMPLETE + reference available | yes | DIRECTORY_LISTED_POSE_NOT_INSPECTED | NO_MOTION_FILE |
| 6 | NEED | 9 | 117 | C. MOTION_INCOMPLETE + reference unavailable | no | NEEDS_REVIEW | NO_MOTION_FILE |
| 7 | DRINK | 7 | 91 | C. MOTION_INCOMPLETE + reference unavailable | no | NEEDS_REVIEW | NO_MOTION_FILE |
| 8 | TOMORROW | 6 | 83 | C. MOTION_INCOMPLETE + reference unavailable | yes | PROJECT_CATALOG_SOURCE_ONLY | NO_MOTION_FILE |
| 9 | NOT | 3 | 39 | C. MOTION_INCOMPLETE + reference unavailable | no | NEEDS_REVIEW | NO_MOTION_FILE |
| 10 | THANK_YOU | 2 | 39 | C. MOTION_INCOMPLETE + reference unavailable | yes | PROJECT_CATALOG_SOURCE_ONLY | NO_MOTION_FILE |
| 11 | HOW | 1 | 18 | C. MOTION_INCOMPLETE + reference unavailable | yes | NEEDS_REVIEW | NO_MOTION_FILE |

## Technical motion coverage simulation

This is concept-occurrence coverage in the G3 corpus, not linguistic accuracy.

| Vocabulary | Covered / total occurrences | Coverage |
| --- | --- | ---: |
| Current | 10/110 | 9.09% |
| Current + top 5 | 82/110 | 74.55% |
| Current + top 10 | 109/110 | 99.09% |

## Realistic speech fixture

The recorded base.en CUDA float16 fast-fixture hypothesis was: `And so my phone asked what your country can do for you, ask what you can do for your country.`. Exact overlap with the current non-playable concept catalog: YOU (2). This does not validate the G3 corpus as representative; it demonstrates a substantial out-of-domain vocabulary gap.

## Recommended first authoring batch

- WATER: high corpus frequency and an official directory entry has been located, but the pose is still uninspected.
- I: high corpus frequency and an official directory entry has been located, but the pose is still uninspected.
- ME: high corpus frequency and an official directory entry has been located, but the pose is still uninspected.

Do not create motion files from this report. The next phase must first inspect the corresponding official ISLRTC video entries and complete technical reference intake.
