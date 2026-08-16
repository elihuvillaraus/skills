---
name: journey-map
description: Generate a single-file, self-contained HTML "game map" of a product's user journey — a winding level path (one node per journey stage, per persona) colored by real build progress, plus a gap callout for stages nobody has built yet and a win-conditions checklist. Reads USER-JOURNEY.md (from the user-journey skill) as the journey's skeleton and infers each stage's status by matching it against the EPIC's PRDs/progress.md. Different from epic-panel: epic-panel is a PRD-first status dashboard (waves/PRDs/stories); journey-map is user-first — it shows what's built through the lens of the experience a real user walks through, why each step exists, and what's missing. Use when the user wants to SEE the product as a journey/game map, asks "qué tanto hemos avanzado" in terms of the user experience (not just tickets), wants to spot journey stages with no PRD behind them, or says "mapa del journey", "diagrama de progreso del juego", "level map", "journey progress". Triggers on "/journey-map", "mapa del journey", "mapa de niveles", "actualiza el mapa del journey".
---

# Journey Map

Turn a product's `USER-JOURNEY.md` + its EPIC's real build progress into ONE self-contained `journey-map.html` — a vertical, winding level path (Duolingo/game-map style) where each node is a journey stage, lit up if it's built, pulsing if it's in progress, locked if it's not started, and flagged if **no PRD addresses it at all** (the single most valuable thing this surfaces — a designed step nobody has built). A win-conditions checklist at the bottom mirrors the journey's own Completeness Checklist.

You are producing a file, not a chat summary. The map is the deliverable, and it must be honest: a stage's status comes from real PRD/story completion, inferred by actually reading both documents — never guessed from vibes, and never silently upgraded to "done" when the evidence is ambiguous (use `unknown` and say so).

## Relationship to other skills — don't confuse these

- **`user-journey`** produces `USER-JOURNEY.md` — the journey's skeleton (personas, stages, entry conditions, Mermaid flowchart, Completeness Checklist). journey-map **requires this file to exist**; it does not invent journey structure. If it's missing, offer to run `/user-journey` first — don't fabricate stages from the EPIC alone.
- **`epic-panel`** is PRD-first (waves → PRDs → stories) — the engineering-management view. journey-map is user-first (personas → stages) — the product-experience view of the exact same underlying progress. Both read the same PRDs/progress.md; they just organize the same truth around a different spine. Generate both if the user wants both views; don't merge them into one artifact — the shapes are genuinely different (dashboard vs. game path).
- **`process-flow-diagram`** is a generic, non-progress-aware flow diagram. Not used here.

## What the map contains (already built into the template)

- **Persona tabs** (only shown if the journey has more than one persona) with a per-persona completion stat.
- **Gap banner** — if any stage has no PRD/story addressing it at all, a callout leads the page: it's a bigger problem than an unstarted-but-planned stage.
- **The path** — one winding vertical route per persona, a node per journey stage: done (lit, checkmark), doing (pulsing, in progress), todo (locked, dim), gap (broken outline, warning). Click a node to see its detail.
- **Stage detail panel** — for the selected node: entry condition, user action, system response, success metric, which PRD(s) implement it, and what's left. Defaults to the stage most worth looking at (a gap, else something in progress, else the first unstarted stage).
- **Win conditions** — the journey's own Completeness Checklist, rendered as a checklist with `done | todo | unknown` per item (`unknown` when the extraction couldn't confirm it either way — never fabricate certainty here).

## Workflow

1. **Require `USER-JOURNEY.md`.** Locate it at `docs/epics/<epic>/USER-JOURNEY.md` (or wherever the project keeps it). If it doesn't exist, tell the user and offer to run `/user-journey` first — that produces the personas/stages/checklist this skill depends on. Do not proceed by inventing a journey structure yourself.

2. **Extract and match — delegate this.** Spawn ONE subagent (general-purpose) to read `USER-JOURNEY.md` in full (personas, per-persona stage breakdowns, Completeness Checklist) and every PRD/`progress.md` in the EPIC, then infer, per persona per stage:
   - **status**: `done` (the PRD(s)/stories that clearly implement this stage are complete) | `doing` (in progress) | `todo` (planned but not started) | `gap` (no PRD or story addresses this stage's entry condition/user action at all — not even partially).
   - **implementedBy**: the PRD id(s) whose scope matches this stage, or `[]` for a gap.
   - **whatsLeft**: one short honest line — what's missing to call it done. Empty for `done`.
   Tell it explicitly: **match by what the PRD/stories actually do, not by name similarity** — a PRD titled "Onboarding revamp" doesn't count as covering the Onboarding stage unless its stories actually implement that stage's entry condition/user action. When the match is genuinely ambiguous, it must say so rather than picking a status to look tidy — pass that stage through as `todo` with a note, not a confident-looking `done`. Also have it evaluate the Completeness Checklist items the same way: `done | todo | unknown` — `unknown` whenever the checklist item can't be confirmed from the docs alone (e.g. it needs a live test to verify, like a timing claim).

3. **Fill the template.** Copy `template.html` (next to this SKILL.md) to the output path (`journey-map.html` in the EPIC folder, or where the user says), then replace the single `const JOURNEY = {…}` object using the schema in the template's header comment. Rules that keep it honest:
   - Never set `status:"done"` on a stage or checklist item without the subagent's evidence — when in doubt it's `todo`/`unknown`, not `done`.
   - A stage's `implementedBy` list should only name PRDs that genuinely implement it — an empty list is what makes it render as a `gap`, which is the point.
   - Keep `whatsLeft` short (one line) and specific, not "needs more work."
   - Update `meta` (name, code, branch, commit `git rev-parse --short HEAD`, generatedAt = today).
   - Do NOT edit the CSS or the logic below the data block — only the `JOURNEY` object and the `<title>`.

4. **Write it, verify, deliver.** Write the file. Sanity-check: every `implementedBy` id exists among real PRDs; every persona has at least one stage; the gap banner count matches the actual number of `gap` stages. Then publish as an artifact (the template already carries the design — no need to load `artifact-design`) and `SendUserFile` the local file. Report: overall completion per persona, the gap count (call these out by name — they're the most actionable finding), and any checklist item marked `unknown` that the user should verify manually.

## Design notes (already handled; don't redo)

Same visual family as `epic-panel` — reuses its color tokens, spacing scale, material/shadow system (`--shadow-card`/`--shadow-sm`), typography, and tactile `:active`/`:hover` feedback, so a project's panel and journey map read as one system, not two random pages. The one deliberate design difference is the layout, because the metaphor genuinely calls for it:

- **The path is a hand-rolled SVG game map, Duolingo-style**: nodes positioned along a sine-wave centerline (`nodePos()` in the script — swing amplitude and vertical step are the two constants to tune if a journey has an unusual stage count), connected by per-segment cubic-bezier `<path>`s so the route can be colored segment-by-segment (a "cleared" segment out of a done node, a dim/dashed segment ahead of it) instead of one flat line.
- **Node states are per-stage, not a single "current position" marker.** Real delivery isn't strictly sequential — two stages can be `doing` at once, or a later stage can finish before an earlier one. Don't collapse this into a fake single "you are here" pin; render each node by its own status.
- **The gap banner leads the page, above the map.** A stage with zero PRDs behind it is a bigger, more surprising problem than an unstarted-but-planned one — per `apple-design`'s wayfinding principle, the most important finding shouldn't be buried at the bottom.
- **The detail panel is separate from the path**, not an inline expansion inside it — expanding a node in place would reflow every node below it on every click. Clicking a node updates one fixed panel instead.
- Centered, width-constrained path column (`~520px`) inside the wider page — the map is the focal point of its section, not a full-bleed dashboard element (`apple-design` grouping: give the thing that needs focus its own stage).
- No `terms` vocabulary override like `epic-panel` has — "persona" and "journey stage" are the right words for effectively any product, dev or not, so this skill doesn't need that generalization knob.

## Notes

- One file, zero dependencies — no CDNs, no build, self-contained SVG.
- Scale: a winding path reads well up to ~15-18 stages per persona (typical journeys have ~10-12 from the `user-journey` stage list). Beyond that the page just gets tall — scrolling a long path is exactly the game-map metaphor, not a problem to fix.
- If the EPIC has no PRDs yet (pre-build), every stage renders `todo` and the gap banner stays empty — that's a legitimate, if uninteresting, starting state.
