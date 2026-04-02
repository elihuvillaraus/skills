---
name: cinematic-marcus
description: Build cinematic websites with AI-generated assets (Marcus/KIE API), scroll-driven animations, and premium interactive modules. Transforms any brand into a scroll-driven cinematic experience using React/Next.js components. Triggers on "cinematic site", "cinematic page", "cinematic-marcus", "transform this site", "premium website", "cinematic landing".
---

# Cinematic Marcus

Build premium cinematic websites with AI-generated hero assets and interactive scroll modules. Uses Marcus (KIE API) for image/video generation, GSAP + Lenis for scroll animations, and 30+ cinematic modules adapted to React.

**Four phases. Any brand. Premium output.**

```
/cinematic-marcus https://example.com
```

---

## HARD RULES

### 1. No emojis -- ever
Use Lucide React icons (`lucide-react`) for all visual indicators. Plain text for logs and docs. Zero exceptions.

### 2. Hero is scroll-driven via canvas frame sequence
The hero MUST scrub with scroll position. Never autoplay loop. Never use `<video>` + `video.currentTime` -- browsers can only seek to keyframes, causing stutter. Canvas + JPEG frames is the only approach.

```tsx
// Scroll-driven canvas pattern:
// 1. Preload JPEG frames into Image[] array
// 2. Canvas draws current frame with cover-fit
// 3. GSAP ScrollTrigger scrubs frame index tied to scroll position
// 4. gsap.to with snap: "frame" for smooth stepping
```

### 3. Marcus/KIE API for all asset generation
Never use Google AI Studio or WaveSpeed. All generation goes through the KIE API at Marcus.

**Credentials location:**
```
/Users/elihuvillaraus/Docs/SaaS/ai-content-machine/marcus/frontend/.env.local
Variables: KIE_API_KEY, KIE_API_BASE_URL (https://api.kie.ai)
```

### 4. React/Next.js components, not standalone HTML
Output is React components using the Zeus design system, not single-file HTML. Components go in `src/components/cinematic/` or the target project's component directory.

### 5. Always inline SVGs, never emojis
Every icon uses `lucide-react`. Custom visuals use inline SVG elements.

### 6. Font contrast minimums
- Dark themes: body text minimum `#999`, labels minimum `#888`
- Buttons: always set explicit color -- white text on dark/accent backgrounds
- `--muted` for captions only, never for body text

### 7. One easing curve for all interactive transitions
```css
transition: all 0.4s cubic-bezier(.16, 1, .3, 1);
```

---

## Phase 1: Brand Analysis

### If transforming an existing site:
```bash
curl -sL "TARGET_URL" -o /tmp/site_raw.html
```

Extract:
- Business name and category
- Color palette (primary, secondary, accent, background, text -- hex codes)
- Typography (heading and body fonts)
- Key copy (headline, tagline, services, CTA, contact)
- Logo URL or screenshot

### If building from scratch:
Ask the user for:
- Brand name
- Industry/category
- Target audience
- Tone (luxury, tech, playful, editorial, etc.)
- Color preferences
- Reference sites they admire

### Output: Brand Card
Generate a summary with color swatches, font samples, extracted copy.

### Pause Point
Show the brand card. Ask: "Does this look right? Any corrections?"

---

## Phase 2: Scene Generation (Marcus/KIE API)

### 2a. Suggest 3 Hero Concepts

Present a table with ONE hero object per concept, distinct visual styles, clear motion descriptions.

**Scene Design Rules:**
- One subject, one action. Single hero item, 2-3 supporting elements max.
- Cinematic, not catalog. Close-ups, shallow depth of field, dramatic angles.
- NO default white backgrounds. Match environment to industry.
- Only generate the FIRST FRAME. Video models animate better from a single image.

### 2b. Cost Check (ALWAYS show before proceeding)

| Asset | Model | Cost |
|-------|-------|------|
| Hero image | nano-banana-pro | Free |
| Hero image (4K) | nano-banana-pro-4k | ~6 credits |
| Hero video (5s) | veo3_fast | ~60 credits |
| Hero video (10s) | veo3 | ~100 credits |
| Frame extraction | ffmpeg (local) | Free |

Ask: "Ready to proceed? This will cost approximately X credits." Wait for confirmation.

### 2c. Generate Image

```bash
source /Users/elihuvillaraus/Docs/SaaS/ai-content-machine/marcus/frontend/.env.local

curl -s -X POST "${KIE_API_BASE_URL}/api/v1/jobs/createTask" \
  -H "Authorization: Bearer ${KIE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana-pro",
    "input": {
      "prompt": "DETAILED_PROMPT_HERE",
      "aspect_ratio": "16:9",
      "output_format": "png"
    }
  }'
```

**Poll status (Nano Banana):**
```bash
curl -s "${KIE_API_BASE_URL}/api/v1/playground/recordInfo?taskId=TASK_ID" \
  -H "Authorization: Bearer ${KIE_API_KEY}"
# state: "waiting" -> "success"
# resultJson.resultUrls[0] = image URL
```

### 2d. Generate Video (Image-to-Video)

```bash
# Upload image to litterbox for URL access
IMAGE_URL=$(curl -s -F "reqtype=fileupload" -F "time=24h" \
  -F "fileToUpload=@path/to/image.png" \
  https://litterbox.catbox.moe/resources/internals/api.php)

# Generate with Veo 3.1 Fast
curl -s -X POST "${KIE_API_BASE_URL}/api/v1/veo/generate" \
  -H "Authorization: Bearer ${KIE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "MOTION_PROMPT",
    "model": "veo3_fast",
    "aspectRatio": "16:9",
    "duration": 5,
    "generationType": "REFERENCE_2_VIDEO",
    "callBackUrl": "https://example.com/noop",
    "imageUrls": ["IMAGE_URL"]
  }'
```

**Poll video status:**
```bash
curl -s "${KIE_API_BASE_URL}/api/v1/veo/record-info?taskId=TASK_ID" \
  -H "Authorization: Bearer ${KIE_API_KEY}"
# response.resultUrls[0] = video MP4 URL
```

**Alternative video models (via /api/v1/jobs/createTask):**

| Model | KIE model name | Duration | Cost |
|-------|---------------|----------|------|
| Kling 2.5 Turbo | `kling/v2-5-turbo` | 5-10s | ~60 credits |
| Kling 3.0 | `kling-3.0/video` | 5-15s | ~300 credits |
| Wan 2.5 | `wan/2-5` | 5-8s | ~60 credits |

### 2e. Extract Frames

```bash
mkdir -p public/assets/hero/frames

# 720p for scroll animation (lighter files)
ffmpeg -i video.mp4 -vf "fps=24,scale=1280:720" -q:v 4 \
  public/assets/hero/frames/frame-%04d.jpg

# Count frames
ls public/assets/hero/frames/ | wc -l
```

### Pause Point
Show the image and video to the user. Wait for approval.

---

## Phase 3: Website Build (React/Next.js)

### Architecture

```
src/app/(marketing)/
  layout.tsx          -- Lenis + GSAP providers, navbar, footer
  page.tsx            -- Landing page with cinematic sections
  components/
    hero-video-canvas.tsx  -- Scroll-driven canvas frame sequence
    page-hero.tsx          -- Reusable hero for subpages

src/components/cinematic/
  glitch-text.tsx          -- RGB channel split on hover
  text-mask-reveal.tsx     -- Scroll-driven text fill
  spotlight-grid.tsx       -- Cursor-tracking card glow
  kinetic-marquee.tsx      -- Scroll-velocity marquee
  cursor-glow.tsx          -- Radial gradient cursor follower
  magnetic-button.tsx      -- Magnetic pull hover
  index.ts                 -- Barrel export

src/components/react-bits/
  Lightning.tsx            -- WebGL lightning shader
  LaserFlow.tsx            -- Three.js vertical beam
  Aurora.tsx               -- Canvas aurora blobs
  Particles.tsx            -- Canvas floating particles

src/lib/motion/
  gsap-provider.tsx        -- GSAP + ScrollTrigger registration
  lenis-provider.tsx       -- Lenis smooth scroll
  use-gsap.ts, use-scroll-trigger.ts, use-magnetic.ts, use-in-view.ts
  motion-tokens.ts         -- Easing curves and durations
```

### Required Dependencies

```bash
pnpm add gsap @gsap/react lenis
# For Three.js effects (optional):
pnpm add three @react-three/fiber @react-three/drei
```

### Hero Section Pattern

```tsx
<section className="hero-scroll-container relative" style={{ height: "300vh" }}>
  <div className="sticky top-0 flex h-screen items-center justify-center overflow-hidden">
    {/* Scroll-driven canvas */}
    <HeroVideoCanvas />
    
    {/* Gradient overlay for text readability */}
    <div className="pointer-events-none absolute inset-0 z-[1]"
      style={{ background: "radial-gradient(ellipse 50% 50% at 50% 40%, transparent 0%, rgba(10,15,30,0.6) 55%)" }} />
    
    {/* Content (fades out on scroll) */}
    <div ref={contentRef} className="relative z-[5] text-center">
      <GlitchText text="BRAND" as="h1" className="font-display text-[clamp(4rem,12vw,10rem)]" />
      <p className="text-text-secondary">Tagline here</p>
    </div>
  </div>
</section>
```

### Hero Text Fade-Out on Scroll

```tsx
useEffect(() => {
  const tween = gsap.to(contentRef.current, {
    opacity: 0, y: -60, ease: "none",
    scrollTrigger: {
      trigger: ".hero-scroll-container",
      start: "10% top",
      end: "35% top",
      scrub: true,
    },
  });
  return () => { tween.scrollTrigger?.kill(); tween.kill(); };
}, []);
```

### Module Selection Guide

| Industry | Recommended Modules |
|----------|-------------------|
| Luxury | Text Mask Reveal, Curtain Reveal, Spotlight Border, Zoom Parallax |
| Food | Color Shift, Zoom Parallax, Kinetic Marquee, Accordion Slider |
| Tech/SaaS | Glitch Effect, Text Scramble, Magnetic Grid, Spotlight Border |
| Creative | SVG Draw, Image Trail, Mesh Gradient, Curtain Reveal |
| Service/B2B | Odometer Counter, Sticky Stack, Particle Button, Kinetic Marquee |

### Quality Standards

- GSAP scroll-triggered fade-up on all content sections
- Noise texture overlay (opacity 0.02-0.04)
- Magnetic button hover on primary CTAs
- Navbar: sticky, transparent at top, glass on scroll
- Responsive 375px to 1440px+
- `prefers-reduced-motion` disables all animations
- Loading state while frames pre-load

---

## Phase 4: Polish and Deploy

### Polish Checklist

- [ ] Hero scroll-drives smoothly (no jank, no frame skipping)
- [ ] Text readable over all backgrounds (text-shadow or backdrop pills)
- [ ] All sections have entry animations (fade-up on scroll-into-view)
- [ ] Section transitions have gradient dividers
- [ ] CTAs have magnetic hover effect
- [ ] Mobile responsive (375px minimum)
- [ ] No console errors
- [ ] `prefers-reduced-motion` tested
- [ ] Lighthouse Performance > 80, Accessibility > 90
- [ ] Three.js/WebGL code-split (only loads on pages that use it)

### Deploy

```bash
# Next.js
pnpm build && npx vercel --yes --prod
```

---

## Pause Points

| After | Action |
|-------|--------|
| Phase 1 | Show brand card. Confirm colors/copy. |
| Phase 2 | Show cost estimate. Confirm before generating. Show image/video. Wait for approval. |
| Phase 3 | Open in browser for review. |
| Phase 4 | Final review before deploy. |

---

## Lessons Learned (from Zeus Implementation)

1. **Canvas frames, not video.currentTime.** The video.currentTime approach stutters. Always use JPEG frames + canvas + ScrollTrigger.
2. **LaserFlow needs alpha: true.** Three.js WebGLRenderer defaults to opaque black. Set `alpha: true`, `setClearColor(0,0,0,0)`, `transparent: true` on material.
3. **next/dynamic for Three.js.** Use `dynamic(() => import(...), { ssr: false })` + `key={pathname}` to force remount on client-side navigation.
4. **Lightning shader alpha.** Output `gl_FragColor = vec4(color, clamp(length(color)*1.5, 0.0, 1.0))` for transparency. Enable GL blend.
5. **Marcus status endpoints differ by model.** Nano Banana: `/api/v1/playground/recordInfo`. Veo: `/api/v1/veo/record-info`. Kling/others: `/api/v1/jobs/recordInfo`.
6. **Never use screen blend on dark backgrounds.** Screen blend makes dark pixels transparent -- on a near-black page, the effect disappears. Use normal blend with alpha transparency instead.
7. **Image opacity + gradient overlay.** Hero image at 0.5-0.7 opacity + radial gradient overlay gives text readability without vignettes.
8. **Match reference images exactly.** Generic particles/gradients are not "premium." Generate actual assets with Marcus that match the brand direction.
