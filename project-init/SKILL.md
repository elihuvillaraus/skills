---
name: project-init
type: workflow
version: 1.0
models: ["any"]
tags: ["setup", "memory", "context", "onboarding"]
---

# Project Init Skill

## What This Skill Does

Sets up the **4-file AI memory system** for any project:

```
project/
  AGENTS.md          ← Hub (≤150 lines). All AIs auto-read this.
  context/
    pipeline.md      ← Full Pipeline Laws, TDD, SDD, Karpathy, signals
    tech-stack.md    ← Stack, dependencies, conventions
  memory.md          ← AI-maintained preferences (starts empty)
```

Run this **once per project**. After that, all agents (Claude, Copilot, Gemini, Cursor) are onboarded automatically.

## When to Use

- Starting a new project
- AGENTS.md or `context/` are missing in an existing project
- Onboarding a new AI tool to an existing project
- After a major stack or direction change

---

## Phase 1 — Detect Existing Context

Before interviewing, check what already exists:

```bash
ls AGENTS.md context/ memory.md 2>/dev/null
cat AGENTS.md 2>/dev/null | head -20
cat docs/ALWAYS-ON-MEMORY.md 2>/dev/null | head -30
```

If files exist, pre-fill answers from them. Only ask the user about gaps.

---

## Phase 2 — Interview (Only What's Missing)

Ask the user these questions **one group at a time**, not all at once:

### Group A — Project Identity
1. **Project name** (e.g., "Horus", "MyApp", "ai-content-machine")
2. **Your role** — what should the AI be? (e.g., "senior fullstack developer", "head of marketing")
3. **One-line description** — what does this project do?

### Group B — Tech Stack
4. **Frontend** (e.g., Next.js 14, React Native + Expo, none)
5. **Backend** (e.g., Hono, FastAPI, Next.js API routes)
6. **Database** (e.g., PostgreSQL + Drizzle, Turso, none)
7. **Auth** (e.g., Better Auth, Lucia, none)
8. **Styling** (e.g., Tailwind CSS, NativeWind, shadcn/ui)
9. **Testing** (e.g., Vitest + Playwright, Jest, none)
10. **Deployment** (e.g., Vercel, DigitalOcean, Docker)

### Group C — Preferences
11. **Language** — code and comments in English or Spanish?
12. **Any hard rules?** (e.g., "never use class components", "always use server components by default")
13. **Skills to always use?** (default: orchestrator, architect, ralph, tester, documenter)

---

## Phase 3 — Generate Files

### File 1: `AGENTS.md`

```markdown
# [Project Name]

> **Before any task**: read `context/pipeline.md` and `memory.md`.
> If `context/` or `memory.md` are missing → run `/project-init` or ask the user before proceeding.

## Identity

You are [role] on **[project name]**. [one-line description].

## Before Every Task

1. `context/pipeline.md` — Pipeline Laws + TDD/SDD/Karpathy rules
2. `memory.md` — learned preferences and corrections
3. `context/tech-stack.md` — stack, conventions, tooling

## Pipeline Laws (full rules → `context/pipeline.md`)

| Law | Rule |
|-----|------|
| Engram | Load memory at start, save at end |
| SDD | Spec file must exist before any code |
| TDD | Test files in `git diff` before launching evaluator |
| Karpathy | Sprint contract must have Assumptions section |
| E2E | TESTER_REPORT rejected without Playwright screenshots |
| OOM | **NEVER** run `pnpm test` without `maxForks: 3` in vitest.config.ts — machine will crash |

## Skills Quick Reference

| Need | Use |
|------|-----|
| Plan a feature | `/architect` |
| Implement a story | `/ralph` |
| Test & QA | `/tester` |
| Full pipeline | `/orchestrator` |
| Document + commit | `/documenter` |
| Design UI | `/ui-ux-designer` |
| Research | `/autoresearch` |

## Agent Signals

- Success: `AGENTNAME_DONE`
- Blocked: `AGENTNAME_BLOCKED: [reason]`

## Memory Rule

When you learn a preference or correct a mistake, **immediately update `memory.md`** under the relevant section. Do not wait until end of session.

## Context Files

- `context/pipeline.md` — Full Pipeline Laws + TDD/SDD/Engram/Karpathy
- `context/tech-stack.md` — Stack, dependencies, conventions
- `memory.md` — Learned preferences (AI-maintained, grows over time)
```

---

### File 2: `context/pipeline.md`

```markdown
# Pipeline Laws & Engineering Standards

> Full reference. AGENTS.md has the summary. This file has the detail.

## The 5 Pipeline Laws

### Law 1 — Engram Always
- Load memory at Phase 0 of every skill
- Save new decisions/learnings at Phase 5 (end)
- Use `memory.md` as universal fallback if Engram CLI is unavailable

### Law 2 — SDD Before Code (Spec-Driven Development)
- A spec file (`*.spec.md` or `docs/specs/US-XXX.md`) must exist BEFORE any ralph/code
- Spec must contain: inputs, outputs, acceptance criteria, edge cases
- SPEC_DONE signal required before implementation starts

### Law 3 — TDD Mandatory (Test-Driven Development)
- Tests must be written BEFORE or WITH implementation (not after)
- Verify with: `git diff --name-only HEAD | grep -E "(\.test\.|\.spec\.)"`
- Empty result = evaluator launch rejected
- TDD_VIOLATION escalated in TESTER_REPORT, not buried

### Law 4 — Karpathy Gate
- Sprint contracts must have an **Assumptions** section
- Every AC (acceptance criteria) must be TDD-ready: "Navigate to X → expect Y"
- Vague ACs ("works correctly", "looks good") are rejected and rewritten

### Law 5 — E2E Non-Negotiable
- TESTER_REPORT without Playwright-CLI screenshots = rejected
- Smoke tests required for every deployable feature
- TESTER_BLOCKED: E2E_MANDATORY emitted if E2E phase is skipped

### Law 6 — No Time Estimates
- Never output "Xh" or "X hours". Use: dependency graph + `parallelizable_with` + `depends_on` + `critical_path` + round-trips (1 round-trip ≈ 25-40 min empirically)
- Wrong estimates erode trust and distort planning; dependency structure does not

### Law 7 — No "Demo" Framing
- Re-read the EPIC's Mission paragraph before drafting any PRD
- Ban the words "demo", "test data", "mock data", "sample data" in PRDs that touch production tables
- If something is genuinely a sandbox/sandbox feature, document it explicitly with scope boundaries

### Law 8 — Migrations Must Be Applied
- Drizzle migrations do NOT auto-run in production (unlike Python/Django/backend migrations)
- After every wave, check `migrations` field of all RALPH_DONE signals
- Apply `pnpm drizzle-kit push` or `psql $DATABASE_URL -f <path>` before serving traffic that depends on new columns
- Ralph must include migration apply command in every RALPH_DONE that adds a migration

### Law 9 — Flag Composition Audit
- Every feature flag has a parent gate; deploying the child while parent=false = broken dark launch
- Before wave deploy: list every v2_* flag introduced, check full parent chain, verify mount condition resolves to true in prod
- Add `## Flag Composition` section to any PRD that introduces or depends on flags

### Law 10 — Verify "Uses Existing X" Claims
- Before architect publishes PRD: grep every "uses existing service/component/function" claim
- If unverifiable: mark `⚠️ VERIFY` inline — ralph must confirm before touching code
- Ralph must verify all such claims in Step 1 before writing a single line; unverifiable = RALPH_BLOCKED
- **BEFORE running any test command**, verify `vitest.config.ts` has:
  ```ts
  pool: "forks",
  poolOptions: { forks: { maxForks: 3 } },
  maxConcurrency: 3,
  ```
- Default Vitest = 1 worker/CPU core → 18 workers on M5 Pro → machine crash
- If the config is missing these settings, **patch it first**, then run tests
- Never run `pnpm test` or `vitest` without this — the machine WILL run out of RAM

---

## Acceptance Criteria Format (required)

Every user story AC must follow one of these formats:

```
✅ "Navigate to /page → expect element X to be visible"
✅ "Submit form with empty email → expect error message 'Email required'"
✅ "Click button → expect API call to /endpoint with payload {}"
❌ "The form works correctly"
❌ "It looks good on mobile"
```

At least one edge case AC is required per user story.

---

## Engram Memory Pattern

At start of every skill:
```
Load memory → Read memory.md (or engram query if available)
```

At end of every skill:
```
Save memory → Update memory.md with decisions, learnings, corrections
```

---

## Agent Signals Convention

| Signal | Meaning |
|--------|---------|
| `RALPH_DONE` | Story implemented, tests written |
| `RALPH_BLOCKED: [reason]` | Cannot proceed without resolution |
| `TESTER_REPORT: READY` | All tests pass, E2E done |
| `TESTER_BLOCKED: E2E_MANDATORY` | E2E was skipped, report rejected |
| `TESTER_BLOCKED: TDD_VIOLATION` | Tests were missing |
| `ARCHITECT_DONE` | PRD complete, ready for ralph |
| `SPEC_DONE` | Spec file written, ready for TDD |

---

## Skills Roster

| Skill | Trigger | Output |
|-------|---------|--------|
| `/orchestrator` | Complex feature end-to-end | ORCHESTRATOR_DONE |
| `/architect` | Design + PRD | ARCHITECT_DONE + PRD |
| `/ralph` | Implement one user story | RALPH_DONE |
| `/tester` | Full QA + E2E | TESTER_REPORT |
| `/documenter` | Commit + docs update | commit hash |
| `/autoresearch` | Research + experiments | RESEARCH_DONE |
| `/always-on-memory` | Maintain docs + memory | docs updated |
```

---

### File 3: `context/tech-stack.md`

```markdown
# Tech Stack — [Project Name]

## Frontend
- Framework: [e.g., Next.js 14 App Router]
- Styling: [e.g., Tailwind CSS + shadcn/ui]
- State: [e.g., Zustand, React Query]

## Backend
- Runtime: [e.g., Node.js / Python]
- Framework: [e.g., Hono, FastAPI, Next.js API routes]
- Auth: [e.g., Better Auth]

## Database
- Primary: [e.g., PostgreSQL + Drizzle ORM]
- Hosting: [e.g., Neon serverless]
- Migrations: [e.g., drizzle-kit]

## Testing
- Unit/Integration: [e.g., Vitest]
- E2E: [e.g., Playwright + playwright-cli]
- Commands: `pnpm test`, `pnpm test:e2e`
- **⚠️ REQUIRED** — vitest.config.ts must always have:
  ```ts
  pool: "forks",
  poolOptions: { forks: { maxForks: 3 } },
  maxConcurrency: 3,
  ```

## Deployment
- Platform: [e.g., Vercel]
- CI/CD: [e.g., GitHub Actions]
- Environments: dev, staging, prod

## Key Conventions
- [e.g., All files in English, comments in English]
- [e.g., Server Components by default, Client only when needed]
- [e.g., Never use class components]
- [e.g., Zod for all validation]

## Key Commands
```bash
pnpm dev       # Start dev server
pnpm build     # Build
pnpm test      # Unit tests
pnpm test:e2e  # E2E with playwright-cli
```
```

---

### File 4: `memory.md`

```markdown
# Memory — [Project Name]

> AI-maintained. Updated automatically when preferences are learned or corrections are made.
> Rule: Update in-place. Replace outdated info. Only save substantial corrections.

## Communication Preferences
<!-- AI fills this in as it learns -->

## Code Style Preferences
<!-- AI fills this in as it learns -->

## Workflow Preferences
<!-- AI fills this in as it learns -->

## Known Gotchas
<!-- Things that went wrong before, to avoid repeating -->

## Corrections Log
<!-- Last 10 corrections made during sessions -->
```

---

## Phase 4 — Confirm & Create

After generating, show the user:

```
📁 Files to create:
  ✅ AGENTS.md (hub)
  ✅ context/pipeline.md
  ✅ context/tech-stack.md
  ✅ memory.md

Proceed? (yes/edit/cancel)
```

If confirmed: create all files. If `context/` doesn't exist: `mkdir -p context`.

---

## Phase 5 — Signal

```
PROJECT_INIT_DONE
Files created: AGENTS.md, context/pipeline.md, context/tech-stack.md, memory.md
All AI tools (Claude, Copilot, Gemini, Cursor) will auto-read AGENTS.md on next session.
Next: run /orchestrator or /architect to start building.
```
