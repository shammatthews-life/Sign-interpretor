# H5 Human Evidence Capture Protocol

H5 collects reviewable evidence from the official Sign Learn application. It does not author a sign.

> Recording a sign does not automatically make it authoring-eligible.

## Capture order

Capture **YOU**, then **WATER**, then **I**. Do not substitute an English explanation, a search result, or another sign-language source.

For each concept, use Sign Learn on a real Android or iOS device and search the exact English term. Record the exact dictionary result label and every variant label displayed, such as `Sign 1` or `Sign 2`. For I, search and record ME separately too; do not assume a shared result is a shared sign.

## What to provide

Provide one short 5–10 second screen recording per result, or several ordered screenshots/keyframes if recording is unavailable. The supplied material must show:

- the search result and exact dictionary label;
- the selected variant label, if any;
- the signer throughout the sign;
- complete start pose, movement, and end/return pose;
- both hands whenever they are used; and
- visible face/head movement whenever present.

Name the file descriptively, for example `you_sign-1_android_2026-10-06.mp4`. Do not upload unrelated app content.

## Metadata submission

Do not commit the recording, screenshots, or extracted video frames to this repository. Instead, create one metadata JSON file per reviewed capture under `docs/sign_references/captured/metadata/`, following [h5_evidence_intake_schema.json](h5_evidence_intake_schema.json). Set `capture_filename` to the locally retained capture name and record the capture date, platform, Sign Learn label, variant, and official provenance.

For each motion parameter, use only `OBSERVED`, `UNCLEAR`, or `NOT_APPLICABLE`. An ambiguous finger position, off-screen hand, or occluded contact remains `UNCLEAR`.

## Review outcomes

The reviewer assigns exactly one outcome:

- `VERIFIED_VISUAL_REFERENCE`: identity, variant, complete visible motion, and provenance are sufficient for a later authoring decision.
- `PARTIALLY_VERIFIED`: official video was reviewed, but one or more motion-critical properties are unclear.
- `NEEDS_HUMAN_REVIEW`: useful evidence exists but needs Deaf/ISL specialist confirmation.
- `REJECTED_INSUFFICIENT_EVIDENCE`: the capture is incomplete, wrong, or cannot establish the intended entry.

The validator can reject incomplete metadata or an unsupported `authoring_eligible: true`; it cannot determine linguistic correctness. The project owner must explicitly begin a separate authoring phase before any motion asset is created.
