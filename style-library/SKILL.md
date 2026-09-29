---
name: style-library
description: Select, customize, or extend the project's reusable motion-graphics card library and style templates. Use for choosing a visual style, adding a card, building a new style pack, or reusing a template in a HyperFrames video.
---

# Reuse the style library

Read [the guide](library/GUIDE.md), then [the registry](library/registry.json) (paths inside it are relative to `library/`). Filter by
style, tier, and purpose before opening individual cards. Read the selected
style's `DESIGN.md`, `tokens.css`, and manifest slot limits.

For an overlay, preserve transparency outside the card and the speaker's face.
For a takeover, use an opaque background. Copy the chosen card into the video's
`compositions/`, localize its CSS, fonts, and GSAP dependency, fill its named
`data-slot` values, and wire its timing using the HyperFrames skill. Copying a
card without its relative dependencies does not produce a complete asset.

Use `templates/` (in this skill) for a whole-scene starting point. A media template may
require the student's own `assets/source.mp4`; check its README before rendering.

The catalog contains draft resources, not a promise that every card has passed
rendered QA. Lint and render the selected card at actual project resolution,
inspect its hero frame and transition, and check slot text at its maximum length.

When adding a style, clone `library/_blueprint/` into `library/NN-slug/`, then complete its design tokens, manifest, and cards, and add its cards to `registry.json` by hand (the kit's `new-style` and `build-registry` scripts are not shipped). Keep project-specific copy in the project, leaving reusable library cards generic.

## Provenance and placeholders

Vendored from the HyperFrames Student Kit by Nate Herk (MIT; the pipeline resources carry a permission to produce personal or commercial videos). The original kit's brand assets belong to AI Automation Society and are not included: card sample copy that named that brand now says `ACME`. Statistics, names, and source labels inside cards are illustrative placeholders. Replace them with verified copy before publishing. "Vox" and "Kallaway" are aesthetic reference names, not official brand assets. The `_blueprint` palette and card content are generic; retheme with the project's own brand tokens.
