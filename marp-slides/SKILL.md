---
name: marp-slides
description: Create premium MARP presentation decks with SVG charts, dashboard components, animations, dark/light themes, and optional AI-generated hero images via Marcus (KIE API). Triggers on "marp", "slides", "presentation", "deck", "slide deck", "create slides", "pitch deck", "make a presentation".
version: 1.0
---

# MARP Slides

Build production-quality MARP presentation decks. Uses the full HTML/SVG feature set for charts, dashboards, and animations. Optionally generates hero images and backgrounds via Marcus when the deck needs cinematic visuals.

## Prerequisites

```bash
# VS Code extension: "Marp for VS Code"
# settings.json:
"markdown.marp.enableHtml": true
"markdown.marp.allowLocalFiles": true

# Export:
npx @marp-team/marp-cli slides.md --pdf --allow-local-files
npx @marp-team/marp-cli slides.md --html --allow-local-files
npx @marp-team/marp-cli slides.md --pptx --allow-local-files
```

## Workflow

### Step 1 — Understand the deck

Before writing a single slide:
- **Purpose**: What decision or action should this deck drive?
- **Audience**: Technical, executive, consumer, internal?
- **Format**: Pitch deck, report, tutorial, showcase, data story?
- **Assets**: Does the user have a logo or images? Are AI-generated visuals needed?

### Step 2 — Select theme and design direction

| Content type | Theme | Vibe |
|---|---|---|
| Data / dashboard / KPIs | Dark (default) | Dense, analytical |
| SaaS pitch / product showcase | Dark + Marcus hero | Cinematic, premium |
| Executive / strategy | Light business | Clean, corporate |
| Tutorial / how-to | Dark tech | Code-forward |
| Lifestyle / editorial | Light editorial | Airy, typographic |
| Creative / brand | Dark gradient | Expressive |

### Step 3 — Decide Marcus usage

Use Marcus (KIE API) for AI-generated images **only** when:
- The deck needs a cinematic hero slide background
- The deck is a product showcase needing brand visuals
- The user explicitly asks for AI-generated imagery
- The deck covers lifestyle, travel, or editorial content needing atmosphere

**Do NOT use Marcus for:**
- Data/dashboard slides (use SVG charts instead)
- Every slide (max 2–3 Marcus images per deck)
- Slides where SVG icons or CSS components do the job

### Step 4 — Generate Marcus images (if needed)

See the [Marcus Image Generation](#marcus-image-generation) section below.

### Step 5 — Write the deck

Follow the structure and component rules below. Save the file as `./slides.md` or `./slides/deck-name.md` in the project directory.

---

## Dark Theme (Default)

The dark theme uses Outfit 800 for headings and Raleway 100–200 for body text.

```markdown
---
marp: true
theme: default
paginate: true
header: '![w:80](./logo.png)'
style: |
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Raleway:wght@100;200;300&display=swap');
  :root {
    --accent: #ff6b1a; --accent-hover: #ff8c4a;
    --dark: #000; --card: #080808; --border: #111;
    --body: #999; --label: #666; --muted: #555; --light: #fff;
    --green: #22c55e; --red: #ef4444; --yellow: #f5a623;
  }
  section { background: var(--dark); color: var(--light); font-family: 'Raleway', sans-serif; font-weight: 200; padding: 56px 72px; }
  h1 { font-family: 'Outfit'; font-weight: 800; font-size: 3em; color: var(--light); margin: 0; }
  h2 { font-family: 'Raleway'; font-weight: 100; font-size: 1.3em; color: #888; }
  h3 { font-family: 'Outfit'; font-weight: 600; font-size: 0.6em; color: var(--muted); text-transform: uppercase; letter-spacing: 0.2em; }
  strong { color: var(--accent); font-weight: 300; }
  section.lead { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
  .tag { font-family: 'Outfit'; font-weight: 600; font-size: 0.55em; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 10px; border-radius: 4px; }
  details { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; margin-top: 8px; }
  details summary { color: var(--accent); font-family: 'Outfit'; font-weight: 600; font-size: 0.8em; cursor: pointer; }
  details p { color: var(--body); font-size: 0.78em; margin-top: 8px; }
  .row { transition: background 0.2s; border-radius: 6px; }
  .row:hover { background: #0c0c0c; }
  abbr { text-decoration: none; border-bottom: 1px dotted #333; cursor: help; }
---
```

## Light Theme (Business / Editorial)

Swap these variables. Use Space Grotesk + IBM Plex Mono or Plus Jakarta Sans.

```css
:root {
  --accent: #2563eb; --dark: #fafafa; --card: #fff; --border: #eee;
  --body: #666; --label: #bbb; --light: #1a1a1a;
}
```

---

## Heading Hierarchy

- `h1` — Title slides only (white, extra large)
- `h2` — Section title (grey, thin) — max 6–8 words
- `h3` — Section label (muted, uppercase, small caps)

---

## Font Pairings (Tested)

| Heading | Body | Use |
|---|---|---|
| Outfit 800 | Raleway 100 | Dashboard, data (default) |
| DM Serif Display | DM Sans 300 | Recipes, editorial, lifestyle |
| Space Grotesk 700 | IBM Plex Mono 300 | Travel, light themes |
| Sora 700 | Sora 200 | Product comparisons |
| Urbanist 800 | Urbanist 100 | Music, consumer brand |
| Plus Jakarta Sans 800 | Plus Jakarta Sans 200 | Retros, team decks |

**Banned fonts:** Inter, Roboto, Arial, Open Sans, Helvetica — these look generic and break the premium feel.

---

## Slide Structures

### Title Slide
```markdown
<!-- _class: lead -->
<!-- _header: '' -->

# Product Name

## The one-line pitch that makes them lean in

---
```

### Content Slide (text + image split)
```markdown
## Section Title

![bg right:40% brightness:0.2 blur:2px](./hero.jpg)

- Key point one — keep it to one line
- Key point two — no sub-bullets
- Key point three — max 5 items
- Key point four
- Key point five
```

### Marcus Hero Slide
```markdown
<!-- _header: '' -->
<!-- _paginate: false -->

![bg brightness:0.12](./marcus-hero.jpg)

# **Product Launch**

## Q2 2026 — Confidential

---
```

### Data Dashboard Slide (cards)
See [Dashboard Components](#dashboard-components) below.

---

## Images

```markdown
# Logo header (hide per slide)
header: '![w:80](./logo.png)'
<!-- _header: '' -->   ← hides on specific slide

# Photo backgrounds
![bg brightness:0.15](./photo.jpg)
![bg right:35% brightness:0.2 blur:3px](./photo.jpg)
![bg left:30%](./photo.jpg)

# Inline centered image
<div style="display:flex; justify-content:center;">
  <img src="./diagram.png" style="width:600px; border-radius:12px;" />
</div>

# CDN logos (no relative path issues)
<img src="https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/vercel.png" style="width:120px;" />
```

**CRITICAL:** Always use relative paths (`./image.png`). Absolute paths break in preview.

---

## Marcus Image Generation

When the deck needs AI-generated visuals, use Marcus (KIE API).

### Credentials
```
/Users/elihuvillaraus/Docs/SaaS/ai-content-machine/marcus/frontend/.env.local
Variables: KIE_API_KEY, KIE_API_BASE_URL (https://api.kie.ai)
```

### Model: nano-banana-2
Always use `nano-banana-2`. It is faster, cheaper, and produces the same quality as nano-banana-pro for backgrounds and editorial images.

### API call (Node.js / fetch)
```javascript
const response = await fetch(`${process.env.KIE_API_BASE_URL}/api/generate/image`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.KIE_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'nano-banana-2',
    prompt: prompt,
    aspect_ratio: '16:9',   // for slide backgrounds
    num_images: 1
  })
});
const { images } = await response.json();
// Download and save as ./marcus-hero.jpg
```

### Prompt formula for slide backgrounds
```
[Subject/scene], cinematic, shallow depth of field, soft bokeh, 
moody [warm/cool] lighting, editorial photography style, 
high-end commercial look, [dominant color palette],
16:9 composition, no text, no UI elements
```

### Example prompts by deck type
- **SaaS/tech hero:** `"Abstract digital infrastructure, fiber optic cables, deep navy and cyan, cinematic DOF, editorial, no text"`
- **Lifestyle/consumer:** `"Morning light pouring through floor-to-ceiling windows, warm amber tones, editorial lifestyle photography, no people, no text"`
- **Finance/executive:** `"Aerial view of a city at dusk, warm streetlights, mist, deep tones, luxury travel editorial, no text"`
- **Health/wellness:** `"Minimalist clean space, natural textures, morning light, soft shadows, lifestyle editorial, neutral palette, no text"`

### Save and reference
```bash
# Save the generated image
curl -o ./marcus-hero.jpg "<image_url_from_api>"

# Then use in Marp:
![bg brightness:0.12](./marcus-hero.jpg)
```

---

## Dashboard Components

### Metric Card (gradient top border)
```html
<div style="background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; position:relative; overflow:hidden; flex:1;">
  <div style="position:absolute; top:0; left:0; right:0; background:linear-gradient(90deg, var(--accent), transparent); height:2px;"></div>
  <div style="font-family:'Outfit'; font-weight:600; font-size:0.55em; color:var(--muted); text-transform:uppercase; letter-spacing:0.15em;">Revenue</div>
  <div style="font-family:'Outfit'; font-weight:800; font-size:2.2em; color:var(--light); margin:8px 0;">$48.2K</div>
  <div style="font-size:0.7em; color:var(--green);">↑ 12.4% vs last month</div>
</div>
```

### Card Row (3 metrics)
```html
<div style="display:flex; gap:14px; margin-top:20px;">
  <!-- paste 3 metric cards here -->
</div>
```

### Status Dots
```html
<svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill="#22c55e"/></svg> Active
<svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill="#f5a623"/></svg> Paused
<svg width="8" height="8" viewBox="0 0 8 8"><circle cx="4" cy="4" r="4" fill="#ef4444"/></svg> Inactive
```

### Verdict Tags
```html
<span class="tag" style="background:#22c55e12; color:var(--green); border:1px solid #22c55e22;">Scale</span>
<span class="tag" style="background:#ef444412; color:var(--red); border:1px solid #ef444422;">Kill</span>
<span class="tag" style="background:#f5a62312; color:var(--yellow); border:1px solid #f5a62322;">Review</span>
```

### Hover Rows (tables / lists)
```html
<div class="row" style="display:flex; justify-content:space-between; padding:10px 12px; font-size:0.8em;">
  <span style="color:var(--body);">Item name</span>
  <span style="color:var(--accent); font-family:'Outfit'; font-weight:600;">$1,200</span>
</div>
```

---

## SVG Charts

### Donut Ring (single metric)
```html
<!-- r=74, circ=465, 89% → offset=51 -->
<svg width="160" height="160" viewBox="0 0 160 160">
  <circle cx="80" cy="80" r="74" fill="none" stroke="#111" stroke-width="16"/>
  <circle cx="80" cy="80" r="74" fill="none" stroke="var(--accent)" stroke-width="16"
    stroke-dasharray="465" stroke-dashoffset="51" stroke-linecap="round"
    transform="rotate(-90 80 80)"/>
  <text x="80" y="86" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="28" fill="white">89%</text>
</svg>
```

### Sparkline (inline)
```html
<svg width="50" height="16"><polyline points="0,14 8,12 16,10 24,8 50,2" fill="none" stroke="#22c55e" stroke-width="1.2"/></svg>
```

### Stacked Bar
```html
<div style="display:flex; height:14px; border-radius:7px; overflow:hidden; width:200px;">
  <div style="width:45%; background:var(--accent);"></div>
  <div style="width:30%; background:#444;"></div>
  <div style="width:25%; background:#222;"></div>
</div>
```

### Vertical Bar Chart
```html
<div style="display:flex; align-items:flex-end; gap:8px; height:120px;">
  <div style="width:32px; height:40%; background:linear-gradient(180deg, var(--accent), #cc5515); border-radius:3px 3px 0 0;"></div>
  <div style="width:32px; height:65%; background:linear-gradient(180deg, var(--accent), #cc5515); border-radius:3px 3px 0 0;"></div>
  <div style="width:32px; height:90%; background:linear-gradient(180deg, var(--accent), #cc5515); border-radius:3px 3px 0 0;"></div>
</div>
```

---

## Interactive Elements

```html
<!-- Collapsible -->
<details><summary>See details</summary><p>Hidden content here</p></details>

<!-- Tooltip -->
<abbr title="Return on Ad Spend">ROAS</abbr>

<!-- Progress bar -->
<progress value="76" max="100" style="accent-color:var(--accent); width:100%;"></progress>

<!-- Checkbox -->
<input type="checkbox" checked style="accent-color:var(--accent);" /> Completed
```

---

## Layout Components

### Terminal Mockup
```html
<div style="background:#0d0d0d; border-radius:10px; border:1px solid #222; padding:16px;">
  <div style="display:flex; gap:6px; margin-bottom:12px;">
    <div style="width:12px;height:12px;border-radius:50%;background:#ef4444;"></div>
    <div style="width:12px;height:12px;border-radius:50%;background:#f5a623;"></div>
    <div style="width:12px;height:12px;border-radius:50%;background:#22c55e;"></div>
  </div>
  <pre style="font-family:'JetBrains Mono',monospace; font-size:0.7em; color:#22c55e; margin:0;">$ npm run deploy</pre>
</div>
```

### Timeline
```html
<div style="border-left:2px solid var(--border); padding-left:20px; margin-top:16px;">
  <div style="position:relative; margin-bottom:16px;">
    <div style="width:10px;height:10px;border-radius:50%;background:var(--accent);position:absolute;left:-25px;top:3px;"></div>
    <div style="font-family:'Outfit';font-weight:600;font-size:0.75em;color:var(--light);">Q1 2026</div>
    <div style="font-size:0.7em;color:var(--body);">Launch description</div>
  </div>
</div>
```

### Before/After Split
```html
<div style="display:flex; gap:16px; margin-top:16px;">
  <div style="flex:1; background:var(--card); border-top:3px solid var(--red); border-radius:8px; padding:14px;">
    <div style="font-family:'Outfit';font-weight:700;font-size:0.65em;color:var(--red);margin-bottom:8px;">BEFORE</div>
    <!-- content -->
  </div>
  <div style="flex:1; background:var(--card); border-top:3px solid var(--green); border-radius:8px; padding:14px;">
    <div style="font-family:'Outfit';font-weight:700;font-size:0.65em;color:var(--green);margin-bottom:8px;">AFTER</div>
    <!-- content -->
  </div>
</div>
```

---

## Animations (HTML export only)

```css
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
@keyframes glow { 0%,100%{box-shadow:0 0 12px var(--accent)66} 50%{box-shadow:0 0 24px var(--accent)} }

.float { animation: float 4s ease-in-out infinite; }
.glow { animation: glow 2s ease-in-out infinite; }
/* Stagger: animation-delay: 0.3s, 0.6s, 0.9s */
```

---

## Pipeline Integration

### From autoresearch
When `autoresearch` produces a report, this skill can convert it to a MARP deck:
```
The AutoResearch report is at /tmp/autoresearch-<skill>-report.md.
Create a MARP deck summarizing: hypothesis, methodology, results, and next experiments.
Use the dark dashboard theme with SVG charts showing before/after metrics.
```

### From architect / orchestrator
PRDs and sprint plans can be converted to MARP decks for stakeholder reviews:
```
Convert this PRD to a MARP pitch deck. Hero slide + 1 slide per Priority Group.
Show user stories as timeline, acceptance criteria as checklist cards.
```

### From exec-summary
Executive summaries naturally map to slide decks:
```
Take this exec summary and produce a MARP deck following McKinsey SCQ structure:
Situation → Complication → Question → Answer → Recommendation → Next Steps.
One slide per section. Use business light theme.
```

---

## Design Rules (Non-Negotiable)

1. **One idea per slide.** Overflow clips silently in MARP — never cram.
2. **h1 = white.** Accent color (`--accent`) for data highlights only.
3. **Body text `#999`, labels `#666`.** Never darker than `#555` on dark backgrounds.
4. **Max 6 rows per list slide.** Beyond 6, split into two slides.
5. **Charts over numbers.** If you have data, visualize it. Mix chart types across slides.
6. **Relative paths only.** `./image.png` works. Absolute paths break in preview.
7. **Always preview before delivering.** No overflow warnings in source — overflow clips silently.
8. **No Inter, Roboto, or Arial.** These look generic. Use the font pairings table above.
9. **Marcus images: max 2–3 per deck.** Hero slides and backgrounds only. SVG for data.
10. **No emojis.** Use SVG icons (see icons section below).

---

## SVG Icons Reference

All icons: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.5">`

| Icon | SVG path |
|---|---|
| Dollar | `<path d="M12 2v20M17 5H9.5a3.5 3.5 0 1 0 0 7h5a3.5 3.5 0 1 1 0 7H6"/>` |
| Heartbeat | `<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>` |
| Check (green) | `<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>` |
| Arrow up | `<polyline points="18 15 12 9 6 15"/>` |
| Arrow down | `<polyline points="18 9 12 15 6 9"/>` |
| Lightning | `<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>` |
| Users | `<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>` |
| Globe | `<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>` |
| Lock | `<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>` |

---

## Pre-Output Checklist

Before delivering any deck:
- [ ] Theme matches content type and audience
- [ ] CSS is fully embedded in frontmatter — no external files
- [ ] Title slide uses `<!-- _class: lead -->`
- [ ] Section titles are concise (6–8 words max)
- [ ] No more than 6 bullet points per slide
- [ ] All images use relative paths (`./image.png`)
- [ ] Data is visualized with SVG charts, not raw numbers
- [ ] No banned fonts (Inter, Roboto, Arial, Open Sans, Helvetica)
- [ ] Marcus images downloaded and saved locally (not remote URLs in bg)
- [ ] Export command documented at top of file or in README
- [ ] No emojis — SVG icons used instead
- [ ] No truncated slides — every slide is complete

---

## Copilot CLI Operations

### Signal
- On deck complete: `MARP_DONE: [filename] — [slide count] slides`
- On blocked (missing assets, credentials): `MARP_BLOCKED: [reason]`

### Invocation examples
```
/marp-slides Create a 10-slide pitch deck for [product]. Dark theme. No images needed.
/marp-slides Make an autoresearch report deck for the orchestrator skill. Include before/after metrics.
/marp-slides Build an executive Q1 review deck. Business light theme. Generate a hero with Marcus.
```
