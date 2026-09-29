---
name: edit-video
description: "Edit a raw talking-head video end to end: transcript, silence trimming, mistake review, visual layer, motion graphics, and a verified HyperFrames render. Use for a complete edit of raw footage ('edita este video', 'límpiame este video', 'quita silencios y errores', 'edit this raw recording'); route a single requested operation straight to its specialist skill."
---

# Edit a video

Router for a full edit of raw talking-head footage. Vendored from the HyperFrames Student Kit (MIT, Nate Herk) and rewired to this catalog's skills. It owns the order of the steps; each specialist owns its own details.

A single operation goes straight to its specialist: silences → `cut-silences`; stutters, repeats, retakes → `cut-mistakes`; captions only → `embedded-captions`; designed cards over the footage → `talking-head-recut`; a reel or Short → `short-form-edit`.

Keep the project in its own directory (`npx hyperframes init <slug>`, see `hyperframes`), and never overwrite the source recording: every cut writes a new file.

1. Inspect duration, streams, and resolution with `ffprobe`. Copy the source into the project's `assets/` or reference the local path the user gave.
2. Get a word-level transcript with a top-level `words` array. Reuse a matching one; otherwise run `npx hyperframes transcribe <source>` (Whisper, local; see `media-use`) and wrap a bare array with `jq '{words: .}'` if needed. Say what a service call uploads or costs before making it.
3. `cut-silences`: produce the EDL and the retimed transcript, and render the silence pass once editing is authorized.
4. `cut-mistakes`: review every candidate in context and keep intentional emphasis. Record the approved cuts. If nothing needs cutting, carry the silence output forward. Every transcript must match the video it was made from.
5. Visual layer: `video-storytelling` for the arc (one persistent world, not a stack of graphics), then a beat sheet with transcript anchors, one visual idea per beat, and deliberate callbacks. For information cards over the footage use `talking-head-recut`; for captions use `embedded-captions`.
6. Author the composition through the `hyperframes` flow (`hyperframes-core`, `hyperframes-animation`, `hyperframes-keyframes`), sourcing assets with `media-use`. Read the [motion philosophy](../motion-showreel/references/motion-philosophy.md) for pacing. If `style-library` is installed, pick or adapt a card there. Localize every asset the composition uses.
7. Lint and check from the project (`hyperframes-cli`), then review in Studio before the draft.
8. Render a draft, inspect encoded frames and transitions, and listen across every cut boundary. Check face framing, text legibility, black frames, and A/V sync. Resolve failures before the final render. Don't repeat an approval request for an action the user already authorized.

Deliver the final MP4 path, the edit decisions, the retimed transcript, the composition, and a `VERIFY.md` stating what was checked and the remaining limitations. An automated detector proposes edits; editorial judgment stays with you and the user.
