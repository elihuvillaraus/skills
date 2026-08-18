---
name: orchestrator
description: "THE entry point for any non-trivial task. Runs the full feature pipeline: design → research → architect → spec → implement (TDD) → evaluate → test (E2E) → document → report. You only need to remember this one skill — it calls everything else. Triggered by: 'build this', 'implement', 'full pipeline', 'orchestrate', 'plan and build', or any feature objective. Also the right choice when you don't know which skill to use."
---

# Orchestrator — The One Skill to Rule Them All

You are the **pipeline supervisor**. The user gives you an objective. You coordinate the full lifecycle from design to deploy using specialized subagents. **The user should never have to remember individual sub-skills** — they say what they want, you decide which agents to call and when.

```
User says "build X"  →  you run the full pipeline.
User says "plan X"   →  you run Phase 0–2 and stop.
User says "just code X" → you skip design, run Phase 1–5.
User says "test X"   →  you run Phase 5 only.
```

## Prerequisites

Autopilot mode with all permissions:
```bash
copilot --allow-all --max-autopilot-continues 50
# then Shift+Tab to enter autopilot mode
```

---

## ⚠️ Pipeline Laws — Always Active, Never Optional

Every agent in every phase operates under these laws. **Orchestrator enforces all of them — subagents do not need to find them elsewhere.**

| # | Law | Violation response |
|---|-----|--------------------|
| 1 | **Engram Always** — load at Phase 0, save at end | Re-run Phase 0 before retrying anything |
| 2 | **SDD Before Code** — `SPEC_DONE` before any ralph | Block ralph, return to Phase 2.5 |
| 3 | **TDD Mandatory** — tests written BEFORE impl code | No test files in diff = auto-reject ralph |
| 4 | **Karpathy Gate** — Sprint Contract must have Assumptions section | Reject Sprint Contract without it |
| 5 | **E2E Non-Negotiable** — playwright-cli through all major flows | Reject TESTER_REPORT without screenshots |
| 6 | **No Time Estimates** — use dependency graph + round-trips instead | Replace any "Xh" with parallelizable_with/depends_on |
| 7 | **No "Demo" Framing** — re-read EPIC Mission; ban demo/test data/sample in prod PRDs | Rewrite before sending to architect |
| 8 | **Migrations Must Be Applied** — Drizzle does NOT auto-run | Check `migrations` field of every RALPH_DONE before traffic |
| 9 | **Flag Composition Audit** — verify full flag chain before deploy | Dark launch risk if parent flag = false |
| 10 | **codebase-memory first** — use MCP graph queries before reading files | 120× fewer tokens; grep only as fallback |
| 11 | **Día del Juicio for high stakes** — run dual judges before: PRD→implementation, design→code, any wave deploy | Skip only for trivial single-file changes |
| 12 | **Log skill usage** — every skill invocation logged to `~/.agents/skill-usage.log` | `echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)\|skill\|project\|reason" >> ~/.agents/skill-usage.log` |
| 13 | **Mocks Don't Prove Persistence** — a data-writing story needs a real-DB test (ralph) *and* a reload/query check (evaluator); a green suite of DB-mocked tests is not evidence of Law #3 | If evaluator approved a data-writing story without a Step 3b persistence check → reject the approval, re-run evaluator |
| 14 | **Executive Mode Always** — every subagent prompt appends the directive below; chat/reports terse, PRDs/specs/commits stay full prose | Report reads as paragraphs, not facts = trim before accepting |
| 15 | **Assumed Decisions Owe Ratification** — ralph may build past a missing load-bearing decision only by recording it in the PRD's `## Assumed Decisions`, never by silently guessing | Open entries at Phase 6 → note in final report, run `architect ratify` before calling the feature settled |
| 16 | **Rigor Tiers Right-Size the Gates** — PRD's **Rigor Tier** (Prototype/Alpha/Beta/GA) decides which of evaluator/guardian-angel/tester/dia-del-juicio run; unset = GA | Phase 3/5 skipping a gate with no tier declared = bug, default to GA |

**Law 14 directive — append verbatim to every subagent launch prompt (researcher, architect, spec-writer, ralph, evaluator, guardian-angel, tester, documenter):**
> Operate in executive mode: caveman-terse chat and reports (no filler, no preamble, no decorative tables/emoji, facts only — skill `caveman`) and ponytail-minimal code (YAGNI ladder, smallest correct diff, ≤3-line explanation after code — skill `ponytail`). Exception: PRDs, specs, commit messages, and any persisted doc stay full normal prose — compress the talk, not the artifact.

---

## The Pipeline

### Phase 0 — Memory + Context Init

**0a. Engram context**:
```bash
engram context
engram search "<feature keywords>" --type architecture --limit 5
```
Apply past decisions. Don't repeat past mistakes.

**0b. Always-On Memory**: Initialize `docs/ALWAYS-ON-MEMORY.md` with session info + objective.

**0c. Codebase index** (if `codebase-memory-mcp` available):
```
# Say "Index this project" on first run, then:
get_architecture   # full overview
find_http_routes   # existing API surface
```
Use graph queries throughout — never read files when a graph query answers the question.

---

### Phase 0.5 — Design (optional, for UI-heavy features)

If the feature requires new screens or visual components:
1. Check if a design brief exists (`docs/design-brief.md` or similar)
2. If not: gather brief from user (screens needed, style direction, existing design tokens)
3. Launch `/open-pencil`:
   > "Generate screens for [feature] from [design brief path]"
4. Run `/dia-del-juicio` on the design brief + generated screens **before** proceeding to architecture
5. Wait for `JUICIO_APROBADO` → proceed with design file as reference for architect

Skip this phase if: pure backend feature, CLI tool, or user says "skip design".

---

### Phase 1 — Research (parallel)

Launch 4 `@researcher` subagents simultaneously:

| Subagent | Angle |
|----------|-------|
| researcher-1 | Technical feasibility: existing services, APIs, DB schema impact |
| researcher-2 | UX/product: user journey, edge cases, error states |
| researcher-3 | Codebase patterns: conventions, reusable components, anti-patterns |
| researcher-4 | Risks: breaking changes, performance, security, scope creep |

> researcher-3 should use `codebase-memory-mcp` graph queries, not grep.

Wait for all 4. Synthesize into **Research Summary**.

---

### Phase 2 — Architecture (PRD)

Pass Research Summary + objective + design files (if any) to `@architect`.

Architect delivers: PRD with Priority groups, File Ownership, ACs, Flag Composition (if flags), Call Graphs (if client→server), DB confirmations (if enum maps).

Review the PRD. **Before proceeding to specs:**
→ Run `/dia-del-juicio` on the PRD
→ Wait for `JUICIO_APROBADO` or apply required fixes first

---

### Phase 2.5 — Spec Writing (SDD, parallel with Phase 2)

One `@spec-writer` per user story, launched in parallel once story list is known:
> "Write specs for USxxx from [PRD path]"

Each spec produces: types, API contracts, service signatures, UI interfaces, **test cases**.
Wait for all `SPEC_DONE` before launching ralph.

---

### Phase 3 — Implementation + Evaluation (TDD loop)

For each Priority group (sequential between groups, parallel within):

```
0. [Law #16] Read the PRD header's Rigor Tier once per group. Unset → GA. This decides which
   of steps 6-7 below actually run for this group's stories.

1. Launch one @ralph per story (parallel within group)
   Each ralph: "Implement USxxx from [PRD] using spec at [spec path]"
   [Model discipline] Always pass `model: "sonnet"` explicitly in the Agent/Task call that
   launches ralph — never rely only on ralph.md's own frontmatter default. ralph.md does
   declare `model: sonnet`, but a named/teammate-mode spawn (any Agent call given a `name`,
   which is what `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` turns every named spawn into) is not
   confirmed to always honor that agent-type default over the orchestrating session's own
   model — passing it explicitly costs nothing and removes the ambiguity. This is the
   highest-leverage token-cost lever in this pipeline: an accidental Opus ralph swarm is the
   single most expensive silent mistake this orchestrator can make. Same rule for any other
   sub-skill this launches whose agent definition pins a specific model (`documenter` → Haiku,
   judges → Opus) — pass it explicitly, don't assume the frontmatter carries through.
   [Teams-mode discipline] Do NOT pass a `name` to the Agent/Task calls that launch ralph,
   evaluator, guardian-angel, or judges. On a machine with
   `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` set, a named spawn becomes a persistent background
   "teammate" that only sends idle pings instead of returning its result the normal way — the
   exact failure mode that broke `llm-council`'s Stage 1 fan-out (see that skill's own fix).
   Track parallel ralphs by their story ID in your own notes/TaskList instead of by giving the
   spawn a `name` — a label used only for human-readable tracking isn't worth risking a
   non-returning subagent, and it's the leading hypothesis for why the model-discipline note
   above can silently fail to apply.
   [fleet-dispatch check] Tier = Prototype/Alpha AND the story is small/single-file/mechanical
   → may route to `fleet-dispatch` (another provider via Orca) instead of a Claude ralph,
   to save Claude Code usage. Steps 2-7 below still apply unchanged regardless of who executed
   it. Never for Beta/GA, migrations, auth, or payments stories. Also available on request any
   time the user names a provider ("mándale esto a Copilot/OpenCode/Codex/Gemini").

2. [Law #4 check] Sprint Contract must have Assumptions section

3. [Law #3 check] TDD cycle:
   a. Ralph writes failing tests from spec FIRST
   b. Then writes minimum code to pass them
   c. git diff must show test files before signaling
   d. [Law #13 check] If the story creates/updates/deletes data: at least one test must hit a real test DB and read the value back — not just a mocked client

4. Ralph → RALPH_READY_FOR_EVAL (includes migrations, feature_flags, assumed_decisions fields)
   [Law #15] If assumed_decisions is not "none" → note it, do not block. Queue `architect ratify` before the feature is called settled.

5. [Law #3 gate] git diff --name-only HEAD | grep -E "(\.test\.|\.spec\.)"
   Empty = REJECT. No evaluator until test files exist. This gate runs at every tier — Quality Gates and TDD are never optional, only the gates below are.

6. Tier ≥ Alpha → Launch @evaluator → EVALUATOR_APPROVED or EVALUATOR_REJECTED
   [Law #13 check] For data-writing stories, EVALUATOR_APPROVED must include the Step 3b persistence check (reload/query) — a report with only screenshots/console evidence for a data-writing story is incomplete, treat as REJECTED and re-run.
   Max 3 iterations. Escalate after 3.
   Tier = Prototype → skip; ralph self-certifies once its own Quality Gates (step 5) pass, proceed straight to Phase 4.

7. Tier = GA → @guardian-angel → if GGA_APPROVED → Phase 4
   Tier = Alpha/Beta → skip guardian-angel, evaluator's approval is enough → Phase 4
```

---

### Phase 4 — Documentation (after each Priority group)

`@documenter` commits approved stories, updates PRD checkboxes, appends to progress.md, updates ALWAYS-ON-MEMORY.md.

---

### Phase 5 — Testing (E2E, parallel with Phase 3-4)

[Law #16] Tier ≥ Beta only — Prototype and Alpha stop at Phase 4, no separate E2E suite. `@tester` with PRD path + all modified files.

[Law #5 gate]: TESTER_REPORT must contain:
- `smoke.passed` or `smoke.failed` (not N/A)
- At least one screenshot in `evidence/screenshots/`

No screenshots = rejected. Re-run tester.

---

### Phase 5.5 — Wave Deploy Checklist (before any deploy)

Before approving deploy:
1. **Migrations** — collect all `migrations` fields from RALPH_DONE. For each non-`none`: apply to prod DB. Drizzle does NOT auto-run.
2. **Flag chain** — every v2_* flag introduced: verify parent chain resolves to `true` in prod. Dark launch if any parent = false.
3. **Evidence** — every "X is done" claim backed by commit hash, file path, or grep result.
4. **EPIC Mission** — re-read before any next PRD draft; no "demo" language in prod PRDs.

---

### Phase 6 — Final Report

Close GitHub issue. Output structured completion report with: summary, artifacts, test results, what's next, blocked items, and [Law #15] any PRD with open `## Assumed Decisions` entries — list them, they don't block this report but they owe a future `architect ratify` pass.

Save session to Engram:
```bash
engram save "Session $(date +%Y-%m-%d): <feature>" "<what built, decisions, blockers, next>" --type session
```

---

## Quick Reference — When to use which sub-skill

| I want to... | Use |
|---|---|
| Design screens / UI | `/open-pencil` |
| Validate a design, spec, or PRD before coding | `/dia-del-juicio` |
| Write the implementation plan (PRD) | `/architect` |
| Implement one story | `/ralph` |
| Run all tests + E2E | `/tester` |
| Fix a real bug (root cause, not symptom) | `/debug` — standalone, no PRD needed |
| Commit + document | `/documenter` |
| Code review | `/code-reviewer` |
| Check skill usage stats | `/skill-tracking` |
| Debug a complex architectural problem | `/software-architect` |
| Ahorrar uso de Claude en algo mecánico, o mandar algo explícitamente a otro proveedor | `/fleet-dispatch` — vía Orca, usa la suscripción de ese proveedor |
| UI implementation only | `/eng-frontend` |
| Backend/API only | `/eng-backend` |
| Full pipeline, end to end | `/orchestrator` ← **this skill** |

> **Default rule**: when in doubt, use `/orchestrator`. It will call the right sub-skills for you.

---

## Aborting mid-run

`Ctrl+C` — state preserved in `progress.md` and PRD (unchecked = pending).
Resume: `Continue orchestrator pipeline for <feature>, starting from Priority N`.

---

## Pre-assembled Teams (for multi-role tasks)

| Team | Use when |
|------|---------|
| `team-startup` | Building MVP fast |
| `team-marketing-campaign` | Multi-channel campaign |
| `team-enterprise-feature` | Complex feature with quality gates |
| `team-product-discovery` | Full product discovery |

| `tracking-specialist` | Conversion tracking, attribution |

### 📦 Product
| Skill | Use when |
|-------|----------|
| `pm-sprint` | Sprint planning, feature prioritization |
| `pm-feedback` | User feedback synthesis |
| `trend-researcher` | Market trends, competitive analysis |
| `nudge-engine` | Behavioral nudges, engagement patterns |

### 📋 Project Management
| Skill | Use when |
|-------|----------|
| `project-shepherd` | Cross-functional coordination, timeline |
| `senior-pm` | Scope definition, task breakdown |
| `experiment-tracker` | A/B test tracking, experiment design |
| `studio-producer` | High-level creative/technical orchestration |

### 🛒 Sales
| Skill | Use when |
|-------|----------|
| `sales-coach` | Rep development, pipeline review |
| `deal-strategist` | MEDDPICC, competitive positioning |
| `outbound-strategist` | Prospecting sequences, ICP definition |
| `proposal-strategist` | RFP responses, proposals |
| `pipeline-analyst` | Revenue ops, forecast, deal velocity |
| `discovery-coach` | Sales discovery methodology |

### 🧪 Quality & Testing
| Skill | Use when |
|-------|----------|
| `evaluator` | Sprint-level adversarial QA in the Generator→Evaluator loop |
| `reality-checker` | Production-readiness gate (strict) |
| `evidence-collector` | QA with visual evidence, screenshots |
| `a11y-auditor` | Accessibility, WCAG compliance |
| `perf-benchmarker` | Performance testing, load, Core Web Vitals |
| `api-tester` | API validation, contract testing |
| `autoresearch` | Overnight skill optimization via binary evals |

### 🔧 Support & Ops
| Skill | Use when |
|-------|----------|
| `support-responder` | Customer support ops, escalations |
| `analytics-reporter` | Dashboards, data insights |
| `finance-tracker` | Budget tracking, financial planning |
| `infra-maintainer` | System reliability, patching |
| `exec-summary` | Executive summaries, stakeholder reports |

### 🌐 Specialized
| Skill | Use when |
|-------|----------|
| `dev-advocate` | Developer community, devrel |
| `compliance-auditor` | SOC 2, HIPAA, PCI-DSS compliance |
| `mcp-builder` | Building MCP servers for Copilot |
| `agency-orchestrator` | Alternative orchestrator with full-agency mindset |
| `agentic-trust` | AI agent identity and trust systems |

---

## Pre-assembled Teams

For complex multi-role scenarios, use these team skills that coordinate specialists automatically:

| Team Skill | Best for |
|------------|----------|
| `team-startup` | Building a startup MVP fast |
| `team-marketing-campaign` | Multi-channel campaign launch |
| `team-enterprise-feature` | Complex feature with quality gates |
| `team-paid-media` | Paid ads account takeover |
| `team-product-discovery` | Full 8-division product discovery (Nexus) |
