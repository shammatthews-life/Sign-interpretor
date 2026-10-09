# H4 Sign Learn Evidence Report

## Official app route

ISLRTC’s [current homepage](https://islrtc.nic.in/) links to both the Sign Learn Android and iOS applications. The [Google Play listing](https://play.google.com/store/apps/details?id=com.islrtc) identifies Sign Learn as ISLRTC’s ISL dictionary, names the developer as Indian Sign Language Research and Training Centre / Department of Empowerment of PwD, and shows an update date of 26 August 2026. The [Apple listing](https://apps.apple.com/us/app/sign-learn/id1644466408) identifies the developer as Islrtc NewDelhi and the copyright as © ISLRTC; retrieved store metadata lists version 1.12 and an earlier player-playback fix in version 1.10.

The ISLRTC notification index also lists “Important Notice: Technical Issues Resolve – ISLRTC Sign Learn App (ISL Dictionary)”. This confirms current official maintenance context, not successful playback of any individual sign.

## Candidate access test

The available browsing environment can inspect store and website metadata but cannot install, launch, or interact with Sign Learn. It therefore cannot enter any of the required exact queries, observe an entry, or play a candidate video. For YOU, WATER, I, ME, HELP, NEED, and DRINK, all app-entry and visual-motion fields are `NOT_INSPECTED` in the companion JSON record.

| Concept | H1 frequency | Exact in-app search executed? | Entry/video result | Variants | H4 authoring gate |
| --- | ---: | --- | --- | --- | --- |
| YOU | 17 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |
| WATER | 16 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |
| I | 15 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |
| ME | 12 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |
| HELP | 12 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |
| NEED | 9 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |
| DRINK | 7 | No | NOT_INSPECTED | NOT_INSPECTED | Blocked |

This table does not say the app lacks any entry. It says the entry and its video were not testable through this environment.

## Manual evidence protocol

On an Android or iOS device with Sign Learn installed, search one exact English candidate at a time in this order: YOU, WATER, I, ME, HELP, NEED, DRINK. For each result, record its exact label and every displayed `Sign 1` / `Sign 2` (or other variant) label. If a video loads, provide either a 5–10 second screen recording or several ordered screenshots/keyframes showing the full sign: neutral/start pose, complete movement, end/return pose, signer orientation, both hands when relevant, and visible face/head movement.

Do not capture unrelated app material. Label the submission with the query, entry label, platform, app version if shown, and capture date. The project will then mark only directly visible properties as `OBSERVED`; occluded or ambiguous properties remain `UNCLEAR`.

## Variant safety and provenance

I, ME, and YOU were not queried in-app, so their lexical relation, contextual differences, regional forms, and variant labels remain unknown. Do not collapse I and ME.

ISLRTC’s [FAQ](https://islrtc.nic.in/faq/) permits dictionary use for research, teaching, and technology development provided the data are not resold or used for profiteering and ISLRTC is acknowledged. It does not grant an explicit redistribution licence for source video, screenshots, or derived frame collections. This repository must therefore retain provenance and manually authored pose data only; do not commit source videos, screen recordings, or extracted frames without explicit rights confirmation.

## Coverage and next action

No sign passed the evidence gate, none was authored, and G3 remains **10/110 (9.09%)**. The next highest-value action is a human capture of the exact Sign Learn result/video for **YOU** (17 occurrences), followed by WATER (16) and I (15). The first candidate that has an inspectable, unambiguous official video should be ranked by `G3 frequency × evidence quality × motion feasibility × variant certainty`; until then, each factor’s evidence quality is zero and authoring is ineligible.
