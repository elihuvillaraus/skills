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
1. Launch one @ralph per story (parallel within group)
   Each ralph: "Implement USxxx from [PRD] using spec at [spec path]"

2. [Law #4 check] Sprint Contract must have Assumptions section

3. [Law #3 check] TDD cycle:
   a. Ralph writes failing tests from spec FIRST
   b. Then writes minimum code to pass them
   c. git diff must show test files before signaling

4. Ralph → RALPH_READY_FOR_EVAL (includes migrations + feature_flags fields)

5. [Law #3 gate] git diff --name-only HEAD | grep -E "(\.test\.|\.spec\.)"
   Empty = REJECT. No evaluator until test files exist.

6. Launch @evaluator → EVALUATOR_APPROVED or EVALUATOR_REJECTED
   Max 3 iterations. Escalate after 3.

7. If approved → @guardian-angel → if GGA_APPROVED → Phase 4
```

---

### Phase 4 — Documentation (after each Priority group)

`@documenter` commits approved stories, updates PRD checkboxes, appends to progress.md, updates ALWAYS-ON-MEMORY.md.

---

### Phase 5 — Testing (E2E, parallel with Phase 3-4)

`@tester` with PRD path + all modified files.

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

Close GitHub issue. Output structured completion report with: summary, artifacts, test results, what's next, blocked items.

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
| Commit + document | `/documenter` |
| Code review | `/code-reviewer` |
| Check skill usage stats | `/skill-tracking` |
| Debug a complex architectural problem | `/software-architect` |
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
