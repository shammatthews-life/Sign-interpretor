# Honest User-Perspective Review: Avatar Interaction

## What this review represents

This is an evidence-based tester review after exercising the unpacked
extension in native Chrome. It is not a recruited-user study, and it does not
rate translation accuracy or sign-language correctness.

## What worked well

- The avatar can be detached from the options panel, moved, and left at a
  chosen viewport position.
- Closing the panel exposed a small reopen handle; clicking it restored the
  options without hiding the avatar.
- The avatar did not shift YouTube's primary content area.
- The floating avatar allowed clicks through to the underlying video. Pause
  and resume both worked while clicking beneath the avatar.
- HELLO produced actual arm-bone rotation. HELLO, GOOD, MORNING, and WATER
  then completed sequentially through extension controls with no missing
  completion lifecycle event.
- The transparent WebGL renderer used the NVIDIA GeForce RTX 4050 renderer in
  the tested Chrome instance.

## Friction and trust concerns

- Moving the avatar is a two-step interaction: enable Move avatar, then drag
  the visible grip. This is safer for YouTube click-through, but first-time
  users may not discover the grip immediately.
- The avatar occupies about 320 by 520 CSS pixels in the tested viewport. It
  can visually cover part of the video even though clicks pass through.
- The sign-test shortcuts are in the expandable Details area and require
  scrolling. They are useful for development, but are not an obvious
  end-user translation workflow.
- Testing proves that some stored motions play. It does not prove that the
  translations are correct, that the signs are linguistically valid, or that
  every spoken word has a suitable sign.
- A later test run showed the Chrome page hidden while its animation frame
  stopped advancing. The observed four-sign completion run succeeded while
  Chrome was visible; hidden-window and background-tab behavior still need
  dedicated tests.
- Although the tested WebGL renderer was NVIDIA, Chrome's reported context
  attributes said `powerPreference: low-power` while the viewer source requests
  `high-performance`. Performance and power behavior should be measured on
  more than one device.

## Overall assessment

**Avatar interaction: promising prototype. Translation/accessibility
readiness: not established.**

I would use the movable avatar and panel controls for a limited demonstration.
I would not rely on this build as a production sign-language translator or
accessibility aid until an ISL expert validates the vocabulary and grammar,
missing-sign behavior is tested on cleared material, and end-to-end ASR and
translation are accepted.

The selected compilation was used only to check the native extension overlay
and YouTube click-through. Its captions and transcript were not processed, so
this review makes no claim about the video's word coverage.

## Recommended next steps

1. Use a short video that the project owns or is authorized to process.
2. Measure bone motion and completion for each available test sign while
   Chrome is visible, and separately test background-tab pause/resume.
3. Have an ISL specialist review sign choice, grammar, and the WATER motion.
4. Test honest unavailable-sign messages and source-word coverage against that
   authorized clip before making production claims.
