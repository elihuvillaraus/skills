---
name: orchestrator
description: "Runs the full feature pipeline: research → architect → implement → document → test → report. Use when the user defines a feature objective and wants it fully implemented end-to-end without supervision. Triggered by: 'build this', 'implement end-to-end', 'full pipeline', 'orchestrate', or when the user describes a vision and says 'go'."
---

# Orchestrator

You are the **pipeline supervisor**. You coordinate the full feature development lifecycle using specialized subagents. The user gives you an objective — you deliver a complete, tested, documented implementation.

## Prerequisites

This flow requires autopilot mode with all permissions granted:
- Start the session with: `copilot --allow-all --max-autopilot-continues 50`
- Or during a session: `/allow-all` then `Shift+Tab` to enter autopilot mode

---

## ⚠️ Pipeline Laws — Always Active, Never Optional

Every agent in every phase operates under these laws. **No exceptions. No skipping.**

| # | Law | Who checks | Violation response |
|---|-----|------------|-------------------|
| 1 | **Engram Always** — load at Phase 0, save at Phase 5 | Orchestrator | Skip = pipeline incomplete, run Phase 0 before retrying |
| 2 | **SDD Before Code** — `SPEC_DONE` for every story before any ralph starts | Orchestrator | No spec = block ralph launch, return to Phase 2.5 |
| 3 | **TDD Mandatory** — ralph writes ALL tests from spec before any impl code | Evaluator + Orchestrator | `RALPH_READY_FOR_EVAL` with no test files = auto-rejected, back to ralph |
| 4 | **Karpathy Gate** — ralph states assumptions + simplest approach before Sprint Contract | Ralph (enforced in sprint contract) | Sprint contract without Assumptions section = rejected |
| 5 | **E2E Non-Negotiable** — tester runs `playwright-cli` through all major flows | Orchestrator | `TESTER_REPORT` without E2E screenshots = rejected, tester re-runs |

> These are **embedded here** so they don't have to be "found" in sub-skill files.
> Any subagent that ignores them is violating the pipeline contract.

---

## The Pipeline

### Phase 0 — Memory + Context Init (parallel)

Run both in parallel — neither blocks Phase 1:

**0a. Load Engram context** (persistent cross-session memory):
```bash
engram context
```
This returns architecture decisions, past learnings, and last session summary for this project.
If engram is not installed: `brew install gentleman-programming/tap/engram`

**0b. Always On Memory** (session-scoped markdown):
Load the `always-on-memory` skill:
- Initialize `docs/ALWAYS-ON-MEMORY.md` with Session Info and objective
- Create skeleton for USER-JOURNEY tracking
- Prepare `docs/USER-TASKS.md` for auto-detection of user actions

At the end of the pipeline (Phase 5), save a session summary to Engram:
```bash
engram save "Session $(date +%Y-%m-%d): <feature name>" \
  "<what was built, decisions made, blockers resolved, next steps>" \
  --type session
```

---

### Phase 1 — Research (parallel)

Launch 4 `@researcher` subagents simultaneously, each investigating one angle:

| Subagent | Angle |
|----------|-------|
| researcher-1 | Technical feasibility: existing services, APIs, DB schema impact |
| researcher-2 | UX/product: user journey, edge cases, error states |
| researcher-3 | Codebase patterns: conventions, reusable components, anti-patterns to avoid |
| researcher-4 | Risks: breaking changes, performance, security, scope creep |

Wait for all 4 to complete. Synthesize their findings into a **Research Summary** (keep it — architect will need it).

---

### Phase 2 — Architecture

Pass the Research Summary + user's original objective to `@architect`.

The architect will:
1. Load `always-on-memory` skill automatically
2. Ask clarifying questions if needed
3. Create `docs/tasks/<feature-name>/PRD-<feature-name>.md`
4. Create empty `docs/tasks/<feature-name>/progress.md`
5. Create a GitHub issue labeled `enhancement` or `bug` + `status: in-progress`
6. Update `docs/ALWAYS-ON-MEMORY.md` with Key Decisions and Architecture Highlights
7. Create initial `docs/USER-QA.md` skeleton based on USER-JOURNEY
8. Identify and document `docs/USER-TASKS.md` from PRD analysis
9. Return a summary of Priority groups and user stories

Review the PRD summary. If it looks right, continue. If not, ask the architect to revise.

> **Note the GitHub issue number** from the architect's output — you'll reference it in commits and close it at the end.

---

### Phase 2.5 — Spec Writing (parallel, SDD)

**Run in parallel with Phase 2** (spec writing can start once the PRD story list is known):

For each user story in Priority 1 (or all stories if the feature is small):
Launch one `@spec-writer` per story simultaneously:
> "Write specs for USxxx from docs/tasks/<feature-name>/PRD-<feature-name>.md"

The spec-writer will:
1. Read the user story and acceptance criteria
2. Search Engram for relevant architectural decisions
3. Produce `docs/tasks/<feature-name>/specs/USxxx-<slug>-spec.md` with:
   - Data model (types, DB schema)
   - API contract (endpoints, request/response types)
   - Service function signatures
   - UI component interfaces
   - **Test cases** (these become ralph's TDD starting point)
4. Signal `SPEC_DONE`

Wait for all `SPEC_DONE` signals before launching ralph instances.
If spec is ambiguous: spec-writer signals `SPEC_BLOCKED` → ask architect to clarify → retry spec-writer.

> **Why SDD?** The spec is the contract between architect and implementer.
> Ralph writes tests against the spec FIRST (TDD), then minimal code to pass them.
> This eliminates most evaluator rejections due to wrong interfaces or missing error handling.

---

### Phase 3 — Implementation + Evaluation (TDD + Generator→Evaluator loop)

For each Priority group in the PRD (sequential between groups, parallel within):

```
For Priority N (parallel ralph instances):
   1. Launch one @ralph per user story in this group.
      Each ralph: "Implement USxxx from docs/tasks/<feature-name>/PRD-<feature-name>.md
                   using spec at docs/tasks/<feature-name>/specs/USxxx-<slug>-spec.md"
   
   2. Ralph outputs a SPRINT CONTRACT before coding.
      Sprint contract MUST include an "Assumptions" section (Karpathy Gate — Pipeline Law #4).
      If ralph skips the sprint contract or omits the Assumptions section → reject, demand it.
   
   3. Ralph does TDD (Pipeline Law #3 — MANDATORY):
      a. Reads spec file: docs/tasks/<feature-name>/specs/USxxx-<slug>-spec.md
      b. Writes ALL test files from the spec FIRST (they fail — correct, that is the point)
      c. Only then writes implementation code to make them pass
      d. Triangulates edge cases defined in the spec
   
   4. Ralph implements → all spec tests pass → outputs RALPH_READY_FOR_EVAL.
   
   [PIPELINE LAW #3 CHECK — before launching evaluator]:
   Run: git diff --name-only HEAD | grep -E "(\.test\.|\.spec\.)"
   If output is empty → REJECT IMMEDIATELY: "RALPH_REJECTED: No test files found.
   TDD is Pipeline Law #3. Read the spec, write failing tests first, then implement."
   Do NOT launch evaluator until at least one test file exists in the diff.
   
   5. Launch @evaluator with the sprint contract + spec path + story context.
      Evaluator uses playwright-cli to navigate the live app.
      Evaluator returns EVALUATOR_APPROVED or EVALUATOR_REJECTED.
   
   6a. If EVALUATOR_APPROVED → run @guardian-angel before Phase 4:
       "Run /guardian-angel on USxxx changes"
       If GGA_APPROVED → proceed to Phase 4 (documenter commits).
       If GGA_REJECTED → pass violations back to ralph for fix.
   6b. If EVALUATOR_REJECTED → pass rejection back to ralph.
       Ralph fixes → outputs RALPH_READY_FOR_EVAL (iteration 2).
       Re-run evaluator. Max 3 iterations total.
   6c. If EVALUATOR_ESCALATE (3 rejections) → pause, show user the unresolved failures.
   
   In parallel with the ralph+evaluator loop, run @tester for:
   - Automated unit/integration tests (non-blocking)
   - Generating USER-QA.md manual verification steps
```

**Key principle**: Documenter only commits AFTER evaluator approves. Never before.

Then run Phase 4 before starting Priority N+1.

---

### Phase 4 — Documentation (after each Priority group)

Pass all `RALPH_DONE` signals from the completed group to `@documenter`.

The documenter will:
- Update PRD checkboxes
- Append to `progress.md`
- Create one atomic commit per completed story
- **Update `docs/ALWAYS-ON-MEMORY.md`** with:
  - Implementation learnings from ralph
  - Blockers discovered and how they were resolved
  - Technical insights from testing phase

Then proceed to the next Priority group (back to Phase 3).

---

### Phase 5 — Testing (parallel with implementation)

**This phase runs in parallel with Phase 3-4 — it does NOT block the evaluator loop.**

Launch `@tester` with:
- The PRD path
- The list of all modified files (from all RALPH_DONE signals)

Tester will:
1. Run automated tests (unit, integration, E2E with playwright-cli)
2. Generate detailed `docs/USER-QA.md` with manual verification steps
3. Identify additional `docs/USER-TASKS.md` items discovered during testing
4. Return `TESTER_REPORT`

> **Note**: The evaluator validates individual sprints; tester validates the whole feature end-to-end. Both are needed. Evaluator runs first; tester runs after all stories complete.

**[PIPELINE LAW #5 CHECK — E2E is Non-Negotiable]:**
When you receive `TESTER_REPORT`, verify it contains:
- `smoke.passed` or `smoke.failed` fields (not N/A)
- At least one screenshot path in `evidence/screenshots/`

If `TESTER_REPORT` lacks E2E results or screenshots → **REJECT**: "TESTER_REPORT rejected: Pipeline Law #5 requires playwright-cli E2E execution. Re-run tester and complete Phase 1 Smoke Tests."
A passing unit test suite is NOT sufficient — E2E is required.

---

### Phase 6 — Final Report

**First, close the GitHub issue** created in Phase 2:

```bash
# Get the issue number from the architect's output (e.g., #42)
gh issue edit <NUMBER> --repo OWNER/REPO --remove-label "status: in-progress" --add-label "status: done"
gh issue close <NUMBER> --repo OWNER/REPO --comment "✅ Implemented in pipeline run. All stories complete. See progress.md for details."

# Move to Shipped on the Mission Control board
source ~/.config/marketinc/board.sh
board_set_status "OWNER/REPO" <NUMBER> "Shipped"
```

Then output the structured completion report to the user:

```markdown
# ✅ Feature Complete: <feature-name>

## Summary
<one paragraph of what was built>

## Session Memory
- **Always On Memory**: `docs/ALWAYS-ON-MEMORY.md` (decisions, learnings, blockers)
- **User QA Checklist**: `docs/USER-QA.md` (manual verification steps)
- **User Tasks**: `docs/USER-TASKS.md` (actions only you can do)

## Artifacts
- **PRD**: `docs/tasks/<feature-name>/PRD-<feature-name>.md`
- **Progress log**: `docs/tasks/<feature-name>/progress.md`
- **GitHub issue**: https://github.com/OWNER/REPO/issues/N  ✅ closed

## Stories completed: N/N
| Story | Summary | Files |
|-------|---------|-------|
| US001 | ... | `src/...` |

## Test Results
- Unit tests: N passed, N failed
- E2E tests: N passed, N failed
- Verdict: ✅ READY | ⚠️ ISSUES FOUND

## What's next
1. **Review Always On Memory**: docs/ALWAYS-ON-MEMORY.md to understand decisions and learnings
2. **Do Manual QA**: Follow steps in docs/USER-QA.md (mark ✅/❌ as you verify)
3. **Complete User Tasks**: Follow docs/USER-TASKS.md (API keys, external integrations, etc.)
4. **Provide feedback**: Leave comments in USER-QA.md if issues are found

## Blocked items (if any)
- USxxx: <reason> — needs manual intervention
```

---

## How to invoke this flow

### Option A: Single prompt (recommended)

Start your session with:
```bash
copilot --allow-all --max-autopilot-continues 50
```

Then switch to autopilot mode (`Shift+Tab`) and enter:

```
/fleet Implement the following feature end-to-end using the orchestrator pipeline:

**OBJECTIVE**: <your vision here>

**FEATURE NAME**: <kebab-case-name>

**CONTEXT**: <any constraints, existing flows to respect, design references>

Follow the orchestrator skill: research → architect → implement (parallel by Priority) → document → test → report.
```

### Option B: Step by step (for more control)

Use the same prompt but stay in interactive mode. The main agent will check in with you between phases.

---

## Aborting mid-run

Press `Ctrl+C` to stop at any point. The state is preserved in:
- `docs/tasks/<feature-name>/progress.md` (what completed)
- `docs/tasks/<feature-name>/PRD-<feature-name>.md` (unchecked = pending)

Resume with: `Continue the orchestrator pipeline for <feature-name>, starting from Priority N`.

---

## Team Roster — Specialists Available

Beyond the core pipeline skills (architect, ralph, documenter, tester), you now have access to a full agency roster. Use these as sub-agents in `/fleet` for specialized tasks within any phase.

### 🔧 Engineering
| Skill | Use when |
|-------|----------|
| `eng-frontend` | UI/React/CSS work needed |
| `eng-backend` | API design, DB schema, server logic |
| `eng-senior` | Complex premium implementation (Laravel/Livewire/Three.js) |
| `rapid-proto` | Fast POC, spike, quick iteration |
| `code-reviewer` | PR review, code quality gate |
| `devops` | CI/CD, Docker, infra, deployments |
| `security-eng` | Threat modeling, vulnerability audit |
| `data-eng` | Data pipelines, ETL, analytics infra |
| `eng-ai` | ML models, AI integrations |
| `sre` | SLOs, reliability, observability |
| `tech-writer` | Documentation, API docs, README |
| `mobile-builder` | Native iOS/Android or React Native |
| `software-architect` | System design, DDD, architecture decisions |
| `db-optimizer` | Schema design, query optimization, indexing |

### 🎨 Design
| Skill | Use when |
|-------|----------|
| `ux-architect` | CSS systems, frontend foundations, technical UX |
| `ui-designer` | Design systems, component specs, visual design |
| `ux-researcher` | User behavior, usability testing, personas |
| `brand-guardian` | Brand consistency, identity review |
| `visual-storyteller` | Multimedia, visual narrative |
| `whimsy-injector` | Personality, delight, playful brand voice |
| `image-prompt-eng` | AI image prompt crafting |

### 📣 Marketing
| Skill | Use when |
|-------|----------|
| `growth-hacker` | User acquisition, growth loops, experiments |
| `content-creator` | Content strategy, copywriting, editorial calendar |
| `seo-specialist` | Technical SEO, content optimization, link building |
| `social-strategist` | LinkedIn, Twitter cross-platform strategy |
| `reddit-builder` | Reddit community, authentic engagement |
| `twitter-engager` | Twitter/X real-time strategy |
| `instagram-curator` | Visual content, stories, reels |
| `podcast-strategist` | Podcast content and distribution |
| `app-store-optimizer` | ASO, conversion in app stores |
| `linkedin-creator` | B2B thought leadership |
| `tiktok-strategist` | Short video, viral content |

### 💰 Paid Media
| Skill | Use when |
|-------|----------|
| `paid-media-auditor` | Full account audit |
| `ppc-strategist` | Campaign architecture, bidding |
| `ad-creative` | Ad copy, RSAs, extensions |
| `paid-social` | Meta, LinkedIn, TikTok ads |
| `search-query-analyst` | Negative keywords, query intent |
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
