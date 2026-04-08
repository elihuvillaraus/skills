---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## ACTIVE BASELINE CONFIGURATION

Adjust these values (1–10) based on what you're building:

- **DESIGN_VARIANCE: 8** — How experimental the layout is. (1–3: Clean/centered | 8–10: Asymmetric/modern)
- **MOTION_INTENSITY: 6** — How much animation there is. (1–3: Simple hover | 8–10: Magnetic/scroll-triggered)
- **VISUAL_DENSITY: 4** — How much content fits on one screen. (1–3: Spacious/luxury | 8–10: Dense dashboards)

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## THE CREATIVE VARIANCE ENGINE

Before writing code, silently "roll the dice" and select ONE combination from the following archetypes based on the prompt's context:

### Vibe & Texture Archetypes (Pick 1 based on DESIGN_VARIANCE)
1. **Ethereal Glass (SaaS / AI / Tech):** Deepest OLED black (`#050505`), radial mesh gradients (subtle glowing orbs), Vantablack cards with `backdrop-blur-2xl`, wide geometric Grotesk typography.
2. **Editorial Luxury (Lifestyle / Real Estate / Agency):** Warm creams (`#FDFBF7`), muted sage, or deep espresso. High-contrast Variable Serif fonts. Subtle CSS noise/film-grain overlay (`opacity-[0.03]`) for a physical paper feel.
3. **Soft Structuralism (Consumer / Health / Portfolio):** Silver-grey or white backgrounds. Massive bold Grotesk typography. Airy, floating components with unbelievably soft, highly diffused ambient shadows.
4. **Bold Free-form** (for DESIGN_VARIANCE 7–10): Any combination of the above, broken grid, overlapping layers, experimental. Let the project's personality guide the direction.

### Layout Archetypes (Pick 1)
1. **The Asymmetrical Bento:** CSS Grid with varying sizes (`col-span-8 row-span-2` next to stacked `col-span-4` cards).
2. **The Z-Axis Cascade:** Elements stacked like physical cards, slightly overlapping, varying depth, subtle rotation.
3. **The Editorial Split:** Massive typography on the left (`w-1/2`), interactive scrollable content on the right.
4. **Grid-Breaking Free-form**: For DESIGN_VARIANCE 8+, deliberately break column structure with offset margins, bleeds, and calculated randomness.

**Mobile Override (Universal):** Any asymmetric layout MUST fall back to `w-full`, `px-4`, `py-8` on viewports below `768px`. Never use `h-screen` — always use `min-h-[100dvh]`.

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt for distinctive choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Maximum 1 accent color; saturation below 80%.
- **Motion**: Use animations for effects and micro-interactions. All motion must simulate real-world mass and spring physics. Use custom cubic-beziers (e.g., `transition-all duration-700 ease-[cubic-bezier(0.32,0.72,0,1)]`). Scale motion based on MOTION_INTENSITY.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth. Apply gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, grain overlays.

## HAPTIC MICRO-AESTHETICS

### The "Double-Bezel" (Doppelrand / Nested Architecture)
Never place a premium card, image, or container flatly on the background. Use nested enclosures:
- **Outer Shell:** Wrapper `div` with subtle background (`bg-black/5` or `bg-white/5`), hairline outer border (`ring-1 ring-black/5`), specific padding (`p-1.5` or `p-2`), large outer radius (`rounded-[2rem]`).
- **Inner Core:** Content container inside the shell with its own background, inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and mathematically calculated smaller radius (`rounded-[calc(2rem-0.375rem)]`).

### Button-in-Button Pattern
Primary buttons with arrow icons (`↗`) MUST nest the icon inside its own circular wrapper (`w-8 h-8 rounded-full bg-black/5`) completely flush with the button's right inner padding. Never a naked icon next to text.

### Spatial Rhythm
- **Macro-Whitespace:** Use `py-24` to `py-40` for sections. Let the design breathe.
- **Eyebrow Tags:** Precede major H1/H2s with pill-shaped badge (`rounded-full px-3 py-1 text-[10px] uppercase tracking-[0.2em]`).

## PERFORMANCE GUARDRAILS
- **GPU-Safe Animation:** Animate exclusively via `transform` and `opacity`. Never animate `top`, `left`, `width`, or `height`.
- **Blur Constraints:** Apply `backdrop-blur` only to fixed/sticky elements (navbars, overlays). Never on scrolling containers.
- **Grain/Noise Overlays:** Apply only to fixed, `pointer-events-none` pseudo-elements.
- **Z-Index Discipline:** No arbitrary `z-50` or `z-[9999]`. Establish a clean scale.

## BANNED PATTERNS (HARD FAILURES)
- Overused font families: Inter, Roboto, Arial, system fonts
- Clichéd color schemes: purple gradients on white backgrounds, neon/outer glow shadows
- Predictable layouts: 3-column equal grids, edge-to-edge sticky navbars glued to top
- Standard `linear` or `ease-in-out` transitions — only custom cubic-bezier
- Centering everything — if DESIGN_VARIANCE > 4, centered hero sections are BANNED
- 3-card carousel testimonials with dots
- Generic names: "John Doe", "Acme Corp", "Nexus", "SmartFlow"
- Fake round numbers: `99.99%`, `50%`
- AI copywriting clichés: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer"
- Emojis anywhere
- `height: 100vh` — use `min-height: 100dvh`

## PRE-OUTPUT CHECKLIST

Evaluate your code against this matrix before delivering:
- [ ] No banned fonts, icons, borders, shadows, layouts, or motion patterns above
- [ ] A Vibe Archetype and Layout Archetype were consciously selected and applied
- [ ] DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY values are calibrated to the project
- [ ] All major cards and containers use the Double-Bezel nested architecture
- [ ] CTA buttons use the Button-in-Button trailing icon pattern where applicable
- [ ] Section padding is at minimum `py-24` — the layout breathes heavily
- [ ] All transitions use custom cubic-bezier curves — no `linear` or `ease-in-out`
- [ ] Scroll entry animations are present — no element appears statically
- [ ] Layout collapses gracefully below `768px` to single-column with `w-full` and `px-4`
- [ ] All animations use only `transform` and `opacity` — no layout-triggering properties
- [ ] Code is real and complete — no truncation, no `// rest of code` shortcuts

NEVER use generic AI-generated aesthetics. Interpret creatively and make unexpected choices genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
