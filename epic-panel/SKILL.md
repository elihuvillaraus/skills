---
name: epic-panel
description: Generate a single-file, self-contained HTML tracking panel for any project's progress — visual "waves" (phases/sprints/milestones) of work items (PRDs, workstreams, campaigns, whatever the project calls them) with dependency chips, per-item progress bars, a filterable/sortable task table with click-to-cycle status persisted to localStorage, a blockers rail, and a reconciliation-deltas note. Works for software EPICs (PRDs/user stories/migrations) and equally for non-dev projects (marketing campaigns, ops rollouts, event planning, any phased initiative) via a configurable vocabulary. Use when the user wants to SEE where a project/epic stands (what's done, in progress, blocked, what's left), asks for a "panel"/"dashboard"/"tracker"/"diagrama por olas" of work, or wants to regenerate an existing panel.html from updated progress sources. Triggers on "/epic-panel", "panel del epic", "tracker de proyecto", "diagrama por olas", "actualiza el panel".
---

# EPIC Panel

Turn a project's work items + progress into ONE self-contained `panel.html` the user opens in a browser to see, at a glance, what's done / in progress / blocked / left — grouped into implementation **waves** with dependency arrows, and a live, clickable task table.

Built for software EPICs (PRDs, user stories, migrations) by default, but the vocabulary is configurable (`meta.terms` — see step 3) so the exact same panel works for any phased project: a marketing campaign's phases/workstreams/deliverables, an ops rollout's stages/tracks/tasks, event planning, whatever the project actually calls its units of work. Pick dev defaults or ask the user what to call things — don't force PRD/migration language onto a non-dev project.

You are producing a file, not a chat summary. The panel is the deliverable. It must be accurate (driven by the project's own progress sources — `progress.md`/PRD files for dev EPICs, whatever tracking doc exists for other projects) and self-contained (no external assets — opens offline, publishable as an artifact).

**See also `journey-map`** — same underlying progress data, organized around the user's experience (a game-like level path per persona) instead of PRDs/waves. Reach for that one when the user wants the product-experience view or asks "what does a real user actually get right now."

## What the panel contains (already built into the template)

- **Header stat** — overall % (by task count) as a compact number + segmented progress bar (done/doing/todo), no decorative ring.
- **Meta chip row** — items completed, waves completed, planned count, high-severity blockers — plain inline chips, not a card grid.
- **Wave groups** — each wave is a plain section (index badge, title, goal, status badge) holding its item cards directly on the page background — never a card nested inside a card. A wave auto-labels itself *ola completa / en curso / en espera / planeada* from its items' status, with a small inline "depende de {Ola N-1}" note.
- **Item cards** — title, scope, status pill (dot + label), progress bar, task count, and chips with real inline-SVG icons (not emoji/unicode glyphs): depends-on, owns/deliverable, story-level interleave, gated/blocked start, planned. Click a card to filter the table.
- **Reconciliation deltas** — a `was → now` list for how the plan diverged from its original version (optional; pass `[]` to hide).
- **Blockers rail** — severity dot, code, title, and what unblocks it.
- **Task table** — filter by wave/item/status + free-text search, sortable columns (with a visible sort-direction indicator), status dots (outline/half-pie/filled), a priority bar-icon, and a status button that cycles `pendiente → en curso → hecho`, persisted to `localStorage` per browser. Export JSON button dumps `{byPrd:{ITEM:[{id,status}]}}`.

The whole thing is data-driven: everything renders from one `const EPIC = {…}` object, including its vocabulary (`meta.terms`). Generating a panel = **filling that object accurately, nothing else.**

## Workflow

0. **Decide the vocabulary.** Dev EPIC (PRDs, user stories, migrations) → use the defaults, skip to step 1. Non-dev project → briefly ask (or infer from context) what the project calls its phase-level grouping, its mid-level work item, and its smallest tracked unit (e.g. a marketing campaign: fase / workstream / tarea; an ops rollout: etapa / track / acción). This becomes `meta.terms` in step 3 — it's the only thing that changes; the schema, chips, and logic are identical for every project type.

1. **Locate the project.** Ask which EPIC/project only if ambiguous. A dev EPIC folder typically holds an `EPIC-*.md`, per-PRD subfolders (`PRD-0X-*/` each with a `PRD-*.md` + `progress.md`), and often a reconciliation/roadmap doc. A non-dev project may just have a single plan/roadmap doc or a list the user describes verbally — that's fine, the schema doesn't require PRD-shaped inputs. Note the output path: `panel.html` in the project folder (or where the user says).

2. **Extract the data — delegate this.** Spawn ONE subagent (general-purpose) to read the roadmap, any reconciliation/authoritative doc, and every item's progress source (`progress.md` + PRD body for dev EPICs; whatever tracking doc exists otherwise), and return: item inventory (title, one-line scope, owned deliverable, depends-on), the full task list per item with **status** and **priority**, the wave/phase grouping with dependency edges, blockers/open decisions, and any "reconciliation deltas" (where an authoritative doc overrides the original plan). Tell it: **implementation status (checkboxes/real completion) is the source of truth for done/todo — not "spec written" status**; call out any place trackers are stale or dependencies form a cycle (those become `interleave`/`gated` chips, not clean waves). If the user only wants a refresh and the last extract is recent, skip re-extraction and just update statuses.

3. **Fill the template.** Copy `template.html` (next to this SKILL.md) to the output path, then replace the single `const EPIC = {…}` object using the schema documented in the template's header comment. Rules that keep it honest:
   - `stories[].s` is one of `done | doing | todo`; the %/counts derive from these (equal weight per task) — so counts always match the checkboxes.
   - Priority `p` is `P1..P4` or `null` — only set it where the source states it; don't invent priorities.
   - A future item with no tasks yet → `planned:true, stories:[]` (renders as "planeado / por definir", excluded from the % denominator).
   - An item whose start is blocked → `gated:"F17"` (chip with the alert icon). A pair coupled at task level (can't be clean parallel waves) → `interleave:"PRD-05"` on both (chip with the shuffle icon) — don't fake it as sequential.
   - `owns:"mig 0003"` for whatever deliverable/artifact it owns — a migration for a dev EPIC, a specific asset/campaign/deliverable for anything else — else `"—"`.
   - Keep `deltas` truthful (`was → now → ref`) or `[]`. Keep `blockers` real, `sev: alta|media|baja`, `cls: ""|"warn"|"low"`.
   - Set `meta.terms` per step 0 (omit entirely to keep the PRD/Ola/historia defaults).
   - Update `meta` (name, code, branch, commit `git rev-parse --short HEAD`, generatedAt = today). For a non-dev project without a git branch/commit, use whatever version/date marker makes sense, or drop that clause from the sub-line copy.
   - Do NOT edit the CSS or the logic below the data block — only the `EPIC` object and the `<title>`.

4. **Write it, verify, deliver.** Write the file. Sanity-check: task counts per item match the source; overall done/total is right; every `depends`/`interleave` id exists in `prds`; every item's `wave` exists in `waves`. Then publish as an artifact (load `artifact-design` is NOT needed — the template already carries the design; just call Artifact) so the user gets a viewable link, and `SendUserFile` the local file. Report the done/total and any item that looks stale in the source so the user can fix the underlying tracking doc.

## Design notes (already handled; don't redo)

Dark, dense **Operate-mode** dashboard (per `impeccable`'s Operate depth: scanability and consistency outrank expression) with a Linear-inspired information architecture, refined per `apple-design`'s materials/typography/craft guidance for generosity of space and a sense of depth — this went through two passes: the first (Linear-flat) read as too austere/utilitarian, so the second pass added room to breathe and soft material elevation without giving up the Operate-mode density rules (no nested cards, no decorative ring, real icons not glyphs). Near-black neutrals (`#09090b`), a single restrained indigo accent (`#6c78ea`) reserved for primary actions/selection/links, semantic state color kept strictly separate — teal=done, amber=in-progress, rose=blocked, slate=dependency. System font stack first (`-apple-system, BlinkMacSystemFont...`, per apple-design's "default to the platform font" rule) with Inter as fallback; monospace only for genuinely tabular/measurement values, never as a "technical" costume.

Structural choices that matter if you ever touch the CSS/JS below the data block:
- **No nested cards.** Waves are plain sections (divider + heading), not a bordered box containing item cards — item cards sit directly on the page background. Don't reintroduce a wave-level card wrapper.
- **No decorative progress ring, no KPI card grid.** The header shows one large number + a segmented progress bar; rollup stats are a single row of inline pill chips, not six bordered boxes.
- **Elevation is a material system, not a border.** Cards carry no hairline border — depth comes from a slightly lighter fill (`--panel`/`--panel2`/`--panel3` steps) plus a soft two-layer shadow (`--shadow-card`/`--shadow-sm`: a 1px inset top highlight to catch light + a wide, low-opacity ambient shadow). Apply the existing `--shadow-*` tokens to any new card-like element instead of inventing a border+shadow combo.
- **Generous spacing is load-bearing, not decoration.** Section rhythm runs 40–60px, card padding 22px, grid gaps 16–18px. If you add a section, match the existing vertical rhythm rather than the tighter spacing of the first draft.
- **Status is a dot, not just a colored pill background** — outline circle (todo), half-filled via `conic-gradient` (doing), filled (done). Same visual language in item-card pills and the task table's status button.
- **Priority is a 3-bar ascending icon** (filled-bar count = urgency), next to the `P1..P4` text — not just colored text.
- **Chips use real inline-SVG icons** (`ICO.dep`, `ICO.inter`, `ICO.gated`, `ICO.owns` in the script) instead of unicode glyphs/emoji — extend that object if a new chip type is ever needed, don't reach for a glyph.
- **Tactile feedback on press** (`apple-design` §1): buttons and the status pill scale down slightly on `:active`, cards lift with a bigger shadow on `:hover`. Keep transitions on `transform`/`opacity`/`box-shadow` only (compositor-friendly).
- The filter/search bar is `position: sticky` with a translucent, blurred background (`backdrop-filter`) so it stays usable while scrolling a long task table — an `apple-design` §12 materials touch, not decoration; keep content scrolling *under* it.
- Focus-visible outlines, themed `::selection`, and a themed scrollbar are already wired — keep them if you edit the CSS.

It commits to a single dark theme on purpose (background + all colors painted explicitly, so it holds on any host). Both redesign passes were validated by actually rendering the file (headless Chrome, then the Claude-in-Chrome extension) and inspecting real screenshots, not just reading the CSS — do the same if you touch this file, a stylesheet that looks right in the diff can still read as flat/cramped on screen. Keep the current look unless the user asks for a reskin; if they do, the CSS `:root` tokens at the top (colors) and the `--shadow-*`/spacing values are the things to swap first.

## Keeping it current

The panel reads from a snapshot baked into the file at generation time; it does not live-read the source. Two ways to keep it true:
- **Regenerate** (`/epic-panel actualiza`) after the progress source changes — re-runs extraction and rewrites the data block. This is the source of truth.
- **Viewer edits** (clicking statuses) are local to that browser's `localStorage` and meant for "what-if"/personal tracking; the Export JSON button lets someone reflect them back into the tracking source. Say this plainly so nobody mistakes local clicks for committed state.

## Notes

- One file, zero dependencies — no CDNs, no build. It opens by double-click and publishes as an artifact unchanged.
- The Export/download button works when the file is opened locally; inside the artifact viewer a plain download is inert (sandbox) — that's fine, the artifact is for viewing, the repo file is for exporting.
- Scale: designed for ~5–15 items and up to a few hundred tasks. Beyond that the table stays usable (filters + search) but consider splitting the project.
