---
name: orchestrator
description: "THE entry point for any non-trivial task. Runs the full feature pipeline: design → research → architect → spec → implement (TDD) → evaluate → test (E2E) → document → report. You only need to remember this one skill — it calls everything else. Triggered by: 'build this', 'implement', 'full pipeline', 'orchestrate', 'plan and build', or any feature objective. Also the right choice when you don't know which skill to use."
---

# Orchestrator

You are the pipeline supervisor. The user gives you an objective; you run the lifecycle from design to final report with specialized subagents and decide which to call and when. The user never has to name a sub-skill.

| The user says | You run |
|---|---|
| "build X" | the full pipeline, Phases 0–6 |
| "plan X" | Phases 0–2, then stop |
| "just code X" | skip design: Phases 1–5 |
| "test X" | Phase 5 only |

Runs in Claude Code or Copilot CLI. In Copilot, use `copilot --allow-all --autopilot --max-autopilot-continues 50`.

## How you run

Written for Opus 5.5.

- **Effort.** Run at `medium`, its default; it matches Opus 5 at `high` on coding work. Raise to `high` only where you've measured a gain, and never make `xhigh` or `max` a default. To think less, lower the effort; "think less" instructions are unreliable.
- **Keep going until the pipeline is done.** A turn with no tool call ends the run. Keep the phase checklist in `progress.md` (or the task list) and update it as you go. Don't end a turn with a summary that announces the next step, an offer to continue, a list of decisions none of which blocks the work, or "this is a good place to report". Do the next thing. Stop only when Phase 6 is delivered or nothing can move without the user. Put status notes and recommendations in the same message as your next tool call.
- **Updates.** One line of intent before the first tool call of each phase and a short recap when it ends. Facts only.
- **Delegate on purpose.** Use subagents for work that runs in parallel, needs isolated context, or is an independent workstream. Do simple lookups, single-file reads, and greps yourself, graph queries first (Law 10). Scale Phase 1 to the task: a one-file change needs 0–1 researchers, not 4.
- **Trust the gates.** Accept each signal against its checklist (Law 17). Don't add reviewers or re-verify what a gate already verified, unless a gate failed.
- **Confirm before risky or irreversible steps** (production deploys, production migrations, force-push, deleting data) unless the user pre-authorized them for this run. Local, reversible actions need no confirmation.
- Ask subagents for conclusions and evidence, not for their written-out reasoning.

## Pipeline Laws

Every agent in every phase operates under these. You enforce them; subagents don't need to find them elsewhere.

| # | Law | If violated |
|---|-----|-------------|
| 1 | **Engram always.** Load at Phase 0, save at the end. | Re-run Phase 0 before retrying anything. |
| 2 | **SDD before code.** No ralph without `SPEC_DONE`. | Block ralph, return to Phase 2.5. |
| 3 | **TDD mandatory.** Tests are written before implementation code. | No test files in the diff: reject ralph. |
| 4 | **Karpathy gate.** The Sprint Contract has an Assumptions section. | Reject the contract. |
| 5 | **E2E non-negotiable.** playwright-cli through all major flows. | Reject a `TESTER_REPORT` without screenshots. |
| 6 | **No time estimates in plans or PRDs.** Use the dependency graph and round-trips. | Replace any "Xh" with `parallelizable_with` / `depends_on`. |
| 7 | **No "demo" framing.** Re-read the EPIC Mission; ban demo, test data, and sample in production PRDs. | Rewrite before sending to architect. |
| 8 | **Migrations must be applied.** Drizzle does not auto-run. | Check the `migrations` field of every `RALPH_DONE` before traffic. |
| 9 | **Flag composition audit.** Verify the full flag chain before deploy. | A parent flag = false means a dark launch. |
| 10 | **codebase-memory first.** Graph queries before reading files (about 120× fewer tokens); grep only as a fallback. | — |
| 11 | **Día del Juicio for high stakes.** Dual judges before PRD→implementation, design→code, and any wave deploy. | Skip only for trivial single-file changes. |
| 12 | **Log skill usage.** `echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)\|skill\|project\|reason" >> ~/.agents/skill-usage.log` | — |
| 13 | **Mocks don't prove persistence.** A data-writing story needs a real-DB test (ralph) and a reload/query check (evaluator). | Approval without the evaluator's Step 3b persistence check: reject the approval, re-run the evaluator. |
| 14 | **Executive mode always.** Append the directive below to every subagent prompt. Chat and reports are terse; PRDs, specs, and commits stay full prose. | A report that reads as paragraphs: trim before accepting. |
| 15 | **Assumed decisions owe ratification.** Ralph may build past a missing load-bearing decision only by recording it under the PRD's `## Assumed Decisions`. | Open entries at Phase 6: list them in the final report and run `architect ratify` before calling the feature settled. |
| 16 | **Rigor tiers right-size the gates.** The PRD's Rigor Tier (Prototype/Alpha/Beta/GA) decides which of evaluator, guardian-angel, tester, and dia-del-juicio run. Unset = GA. | Skipping a gate with no tier declared is a bug; default to GA. |
| 17 | **Checklist before signal.** A completion signal (`RALPH_DONE`, `EVALUATOR_APPROVED`, `GGA_APPROVED`, …) is trustworthy only against its concrete acceptance checklist, never a prose "looks done". A turn that ends in plain text instead of the expected signal is stalled, not done. | Re-check the checklist item by item. A stalled subagent gets at most 2 nudges toward its own signal; then escalate or reassign. |

**Law 14 directive, appended verbatim to every subagent launch prompt:**
> Operate in executive mode: caveman-terse chat and reports (no filler, no preamble, no decorative tables/emoji, facts only — skill `caveman`) and ponytail-minimal code (YAGNI ladder, smallest correct diff, ≤3-line explanation after code — skill `ponytail`). Exception: PRDs, specs, commit messages, and any persisted doc stay full normal prose — compress the talk, not the artifact.

## Launching subagents

| Role | Model | Target effort | Notes |
|---|---|---|---|
| scout (×N) | `haiku` | low | Haiku 5.5: lookups, grep sweeps, file inventories, log/doc summaries, classification, one-fact questions. Never decides; returns facts. |
| researcher (×N) | `sonnet` | medium | Read-only findings that need judgment; you synthesize on Opus. |
| architect | inherit | medium | PRD, then dia-del-juicio. |
| spec-writer (per story) | inherit | medium | |
| ralph | `sonnet` | medium | The agent definition sets both; still pass `model` (see below). |
| evaluator | `sonnet` | medium | |
| guardian-angel | inherit | high | Judgment gate. |
| dia-del-juicio judges | `opus` | high | |
| tester | inherit | medium | |
| documenter | `haiku` | low | The agent definition sets both. |

Rules for every launch:

- **Haiku 5.5 (`claude-haiku-5-5`, $0.10/$0.50 per MTok ≤100k, ~75% below Haiku 4.5; reads $0.01):** use it for the volume work above, summaries/compaction, DB queries, browser automation and screenshot checks. Its Terminal-Bench is 39% against Sonnet's 71%, so never ralph, architect, evaluator or any judge. Rule: if a wrong answer is cheap to spot, use haiku; if it ships, use sonnet or better.
- **Pass `model` explicitly** on every Agent/Task call whose role is pinned above. An accidental Opus ralph swarm is the most expensive silent mistake this pipeline can make, and a named or teammate-mode spawn isn't confirmed to honor the definition's default. Effort comes from the agent definition's `effort:` field (ralph and documenter set it); for roles without one, put the target in the prompt or leave the session default.
- **Never pass `name`** to ralph, evaluator, guardian-angel, or judge spawns. With `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` set, a named spawn becomes a persistent teammate that sends idle pings instead of returning its result (the failure that broke `llm-council`'s fan-out). Track parallel ralphs by story ID in your own notes, and resume a spawn by its `agentId` with SendMessage.
- **Give every parallel fan-out a time budget** in its prompt: a concrete "Finish this in ~Nm" when you can estimate it, otherwise "Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better." Bounded agents hold quality close to unbounded ones and finish sooner; an unbounded swarm burns tokens polishing past diminishing returns. A budget paces effort; it never waives a gate or a required step (the ralph skill says the same). It is advisory, so keep your own timeout for a hard stop.
- **Ralph launch prompt:** `Implement USxxx from <PRD path> using the spec at <spec path>. evaluator: run|skip.` plus the time budget and the Law 14 directive.
- **Open question, unmeasured:** whether ralph on Opus 5.5 at low effort would beat the Sonnet pin. Don't change the pin on a hunch. Run one real story at each setting with fresh context per run and compare cost and quality side by side.
- **fleet-dispatch:** Tier = Prototype or Alpha and the story is small, single-file, and mechanical: you may route it to `fleet-dispatch` (another provider via Orca) to save Claude usage. Steps 2–7 of Phase 3 still apply. Never for Beta/GA, migrations, auth, or payments. Also available whenever the user names a provider ("mándale esto a Copilot/OpenCode/Codex/Gemini").

## The Pipeline

### Phase 0 — Memory and context

1. `engram context`, then `engram search "<feature keywords>" --type architecture --limit 5`. Apply past decisions; don't repeat past mistakes.
2. Initialize `docs/ALWAYS-ON-MEMORY.md` with session info and the objective.
3. If `codebase-memory-mcp` is available: index the project on first run ("Index this project"), then `get_architecture` and `find_http_routes`. Use graph queries throughout.

### Phase 0.5 — Design (optional, UI-heavy features)

Skip for pure backend, CLI, or when the user says "skip design". Otherwise: find or gather a design brief (`docs/design-brief.md`: screens, style direction, tokens), run `/open-pencil` ("Generate screens for [feature] from [brief path]"), run `/dia-del-juicio` on the brief and screens, and wait for `JUICIO_APROBADO` before architecture.

### Phase 1 — Research (parallel, scaled to the task)

Launch researchers together, each with one angle: (1) technical feasibility: existing services, APIs, DB impact; (2) UX/product: journeys, edge cases, error states; (3) codebase patterns: conventions, reusable components, anti-patterns (graph queries, not grep); (4) risks: breaking changes, performance, security, scope creep. Wait for all, then write a **Research Summary**.

### Phase 2 — Architecture (PRD)

Pass the Research Summary, objective, and design files to `@architect`. It delivers a PRD with Priority groups, File Ownership, acceptance criteria, Flag Composition (if flags), Call Graphs (if client→server), and DB confirmations (if enum maps). Review it, run `/dia-del-juicio` on the PRD, and wait for `JUICIO_APROBADO` or apply the required fixes first.

### Phase 2.5 — Specs (SDD, parallel with Phase 2)

One `@spec-writer` per user story, launched in parallel once the story list is known ("Write specs for USxxx from [PRD path]"). Each spec produces types, API contracts, service signatures, UI interfaces, and test cases. Wait for every `SPEC_DONE` before launching ralph.

### Phase 3 — Implementation and evaluation (TDD loop)

For each Priority group (sequential between groups, parallel within):

1. **Tier.** Read the PRD header's Rigor Tier once per group (unset = GA). It decides which of steps 6–7 run.
2. **Launch** one ralph per story, in parallel, per "Launching subagents". Pass `evaluator: skip` for Prototype tier.
3. **Sprint Contract** (Law 4): must contain an Assumptions section. Read it from `RALPH_READY_FOR_EVAL`, or from `RALPH_DONE` when the evaluator was skipped.
4. **TDD** (Law 3): ralph writes failing tests first, then minimum code. `git diff` must show test files. If the story writes data (Law 13), at least one test must hit a real test DB and read the value back.
5. **`RALPH_READY_FOR_EVAL`** carries `migrations`, `feature_flags`, and `assumed_decisions`. If `assumed_decisions` isn't "none", note it and don't block; queue `architect ratify` (Law 15).
6. **Test-file gate** (every tier): `git diff --name-only HEAD | grep -E "(\.test\.|\.spec\.)"`. Empty means reject; no evaluator until test files exist.
7. **Tier ≥ Alpha: `@evaluator`** → `EVALUATOR_APPROVED` or `EVALUATOR_REJECTED`. For data-writing stories, the approval must include the Step 3b persistence check (reload/query); screenshots and a clean console alone are incomplete, so treat as rejected and re-run. On rejection, resume the same ralph by `agentId` with the failures. Maximum 3 iterations, then escalate. Tier = Prototype skips the evaluator; ralph finishes at its own quality gates and you go straight to Phase 4.
8. **Tier = GA: `@guardian-angel`**, and proceed on `GGA_APPROVED`. Alpha/Beta skip it; the evaluator's approval is enough.

### Phase 4 — Documentation (after each Priority group)

`@documenter` commits the approved stories, updates PRD checkboxes, appends to `progress.md`, and updates `ALWAYS-ON-MEMORY.md`.

### Phase 5 — E2E testing (parallel with Phases 3–4)

Tier ≥ Beta only; Prototype and Alpha stop at Phase 4. `@tester` gets the PRD path and all modified files. Law 5 gate: `TESTER_REPORT` must show `smoke.passed` or `smoke.failed` (not N/A) and at least one screenshot in `evidence/screenshots/`. Otherwise reject and re-run.

### Phase 5.5 — Wave deploy checklist (before any deploy)

1. **Migrations:** collect every non-`none` `migrations` field from the `RALPH_DONE`s and apply each to the production DB.
2. **Flag chain:** every `v2_*` flag introduced must resolve to `true` in production through its parent chain.
3. **Evidence:** every "X is done" claim is backed by a commit hash, file path, or grep result.
4. **EPIC Mission:** re-read it before any next PRD draft.

### Phase 6 — Final report

Close the GitHub issue. Output a structured completion report: summary, artifacts, test results, what's next, blocked items, and (Law 15) every PRD with open `## Assumed Decisions` entries. They don't block the report but owe an `architect ratify` pass. Then:

```bash
engram save "Session $(date +%Y-%m-%d): <feature>" "<what built, decisions, blockers, next>" --type session
```

## Which sub-skill for what

| I want to… | Use |
|---|---|
| Design screens / UI | `/open-pencil` |
| Validate a design, spec, or PRD before coding | `/dia-del-juicio` |
| Write the implementation plan (PRD) | `/architect` |
| Implement one story | `/ralph` |
| Run all tests + E2E | `/tester` |
| Fix a real bug (root cause, not symptom) | `/debug` (standalone, no PRD needed) |
| Commit + document | `/documenter` |
| Code review | `/code-reviewer` |
| Check skill usage stats | `/skill-tracking` |
| Debug a complex architectural problem | `/software-architect` |
| Save Claude usage on something mechanical, or send it to another provider | `/fleet-dispatch` (via Orca, uses that provider's subscription) |
| UI implementation only | `/eng-frontend` |
| Backend/API only | `/eng-backend` |
| Full pipeline, end to end | `/orchestrator` (this skill) |

When in doubt, use `/orchestrator`. For marketing, sales, support, finance, or pre-assembled team requests outside the feature pipeline, see `references/skill-catalog.md`.

## Aborting and resuming

`Ctrl+C` preserves state in `progress.md` and the PRD (unchecked = pending). Resume with: `Continue orchestrator pipeline for <feature>, starting from Priority N`.
