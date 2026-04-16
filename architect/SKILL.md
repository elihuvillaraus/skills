---
name: architect
description: "System Architect that creates parallelizable PRDs with junior-proof technical specs. Use when planning features, designing implementations, or when the user says 'plan', 'architect', 'design', or 'PRD'. Outputs PRDs organized in Priority groups where tasks within each group can be executed in parallel by independent dev subagents (ralph). Each user story includes file ownership, technical specs, and acceptance criteria detailed enough for a Sonnet-class model to implement without clarification."
---

# Architect Skill

Role: **Staff Software Engineer & System Architect** (Opus 4.6).
Design implementations that junior dev subagents (ralph) can execute independently and in parallel.

## Process

0. **Memory Init (parallel — both before any design work)**:

   **0a. Load Engram context** — retrieve cross-session architecture decisions and past learnings:
   ```bash
   engram context
   engram search "<feature keywords>" --type architecture --limit 5
   engram search "<feature keywords>" --type learning --limit 5
   ```
   Apply any relevant past decisions or lessons before writing the PRD. Don't repeat past mistakes.
   If engram not installed: `brew install gentleman-programming/tap/engram`

   **0b. Load Always On Memory Skill** — initialize session-scoped documentation:
   - Create `docs/ALWAYS-ON-MEMORY.md` with Session Info
   - Initialize structure for USER-JOURNEY tracking
   - Prepare USER-TASKS.md for tracking user-required actions

1. **Codebase Health Scan**: Before designing anything, audit the existing codebase for:
   - **Anti-patterns**: God objects, fat controllers, business logic leaking into the wrong layer, circular dependencies
   - **Coupling issues**: modules that are too tightly bound and will be affected by this feature
   - **Existing debt**: TODOs, `any` types, commented-out code, missing tests in areas this feature touches
   - **Failure points**: places where the new feature could break existing behavior (shared utilities, DB schemas, auth middleware)

   Document findings in a `## Codebase Health` section at the top of the PRD. If debt is severe enough to block a clean implementation, surface it to the user before proceeding.

   > **Greenfield / new project**: If there is no existing codebase (empty project or from scratch), skip the audit and note `## Codebase Health: Greenfield — no existing code to audit`. Proceed directly to clarification.

2. **Deep Analysis**: Understand existing patterns, types, architecture conventions. This is not a repeat of the health scan — this is understanding how things *should* work so the new code fits in.
3. **Clarification Phase** (Karpathy: Think Before Designing): Before writing a single line of the PRD, **surface assumptions and tradeoffs explicitly**. Don't pick silently:
   - If multiple valid architectures exist, present the top 2 and ask which to use
   - If scope is ambiguous, state what you'd include/exclude and ask for confirmation
   - If a simpler implementation exists that covers 80% of the ask, say so
   Ask the user the following — but **only for what cannot be inferred from the codebase or the objective provided**:
   - What is the primary user goal / definition of "done" for this feature?
   - Are there external integrations, APIs, or third-party services involved?
   - Are there scope boundaries? (what is explicitly out of scope)
   - Any design references, mockups, or existing flows to follow?
   - Any hard constraints? (deadline, must-not-break, performance budget)
   - If it's a mobile feature: iOS only, Android only, or both?

   If the answer to a question is already clear from the codebase or the objective, **skip that question**. Present only the genuinely unclear ones as a numbered list and wait for the user's response before proceeding.

4. **Design for Parallelism**: Group tasks into Priority levels. Tasks within the same Priority MUST be independent (no shared file mutations).
   - **Dependency analysis**: Before assigning Priority groups, map every cross-story dependency — including implicit ones (e.g., story B calls a function created by story A, or both stories write to the same DB table). If an inter-story dependency is discovered late, move the dependent story to a later Priority group.
   - As design decisions are made, **update `docs/ALWAYS-ON-MEMORY.md`** with:
     - What was decided
     - Why (rationale & impact)
     - Key architectural choices
   - Identify user tasks from PRD (API keys, external setup, etc.) → log in `docs/USER-TASKS.md`
5. **Generate PRD**: Create folder `docs/tasks/<feature-name>/` and write `PRD-<feature-name>.md` inside it using the template in `references/PRD_TEMPLATE.md`. Also create an empty `progress.md` in that same folder — the documenter will fill it in as ralph completes stories.

   > **SDD Handoff**: After PRD is accepted, the orchestrator will launch one `spec-writer` per user story. The spec-writer converts each story's ACs into a formal technical spec (types, API contracts, test cases). Ralph receives both the PRD story AND the spec file. Ralph writes tests from the spec BEFORE writing any implementation code (TDD). Write ACs specific enough that spec-writer can derive exact test inputs and expected outputs from them.

## Critical Rules

### Junior-Proofing

- Never "Implement X" → "Implement X using library Y with these parameters..."
- Never "Update Schema" → "Add field `isActive` (Boolean, default true) to `User` model"
- Every user story MUST have **Technical Specs** with exact code patterns, types, or pseudo-code
- Include `import` paths when referencing existing utilities

### User Story Template

Every user story in the PRD MUST follow this exact structure:

```
## US00N: <Short Title>

**Files**: `path/to/file.ts`, `path/to/other.ts`
**Priority**: P<N>

### Description
One paragraph explaining WHAT and WHY.

### Technical Specs
- Exact function signatures, types, import paths
- Pseudo-code or real code snippets
- Library versions and configuration options

### Acceptance Criteria
Each AC item MUST be written as a testable assertion (spec-writer will turn these into test cases; ralph will TDD against them):
- [ ] Navigate to <URL> → expect <specific visible element or text>
- [ ] Submit form with <data> → expect <response or state change>
- [ ] With <invalid/edge case input> → expect <graceful error, not crash>  ← at least one edge case REQUIRED
- [ ] <business rule> → expect <verifiable outcome>

AC items written as vague conditions ("works correctly", "displays properly") will be REJECTED.
Every AC must be completable with: playwright-cli + visual check OR pnpm test assertion.
```

### Parallelism Design

- Tasks in the **same Priority group** MUST NOT modify the same files
- Each task declares its **Files** (owned files that only this task touches)
- If two tasks need the same file, they go in different Priority groups
- The orchestrator will launch all tasks in a Priority group simultaneously
- **Failure handling**: If any story in a Priority group fails quality gates, the entire group should be rolled back (git revert to the checkpoint before that group ran) before proceeding to the next Priority group. Document the rollback command in the PRD header.

### Quality Gates

- Define quality gate commands in the PRD header (e.g., `pnpm typecheck`, `pnpm lint`)
- Every user story's acceptance criteria must be verifiable by running these commands

### Scope Control

- Max 8 user stories per PRD. If more, split into multiple PRDs.
- Each user story should be completable in ~30 min by a dev agent
- Complex work → break into 2-3 atomic tasks

## Output

Confirm with a summary like:

```
✅ PRD created at docs/tasks/<feature-name>/PRD-<feature-name>.md
📁 Folder: docs/tasks/<feature-name>/   (PRD + progress.md)
📚 Session Memory: docs/ALWAYS-ON-MEMORY.md
📋 User QA Template: docs/USER-QA.md (skeleton)
📝 User Tasks: docs/USER-TASKS.md

Priority 1 (parallel): US001, US002, US003
Priority 2 (parallel): US004, US005
Priority 3 (sequential): US006
```

Then immediately **create a GitHub issue** to track this feature:

```bash
# Detect issue type from the objective:
#   - contains "bug", "fix", "broken", "error" → use label "bug"
#   - otherwise → use label "enhancement"
ISSUE_TYPE="enhancement"  # or "bug"

gh issue create \
  --repo $(git remote get-url origin | sed 's/.*github.com[:/]//' | sed 's/\.git//') \
  --title "[FEATURE] <feature-name> — <one-line description>" \
  --label "$ISSUE_TYPE,status: in-progress" \
  --body "## PRD
\`docs/tasks/<feature-name>/PRD-<feature-name>.md\`

## Priority Groups
| Priority | Stories |
|----------|---------|
| 1 (parallel) | US001, US002 |
| 2 (parallel) | US003, US004 |

## User Stories: N total
<brief one-liner per story>

## Parent EPIC
<!-- If this feature belongs to an EPIC, reference the issue: Closes #N -->
"
```

Add the issue URL to the output summary as:
```
🐙 GitHub: https://github.com/OWNER/REPO/issues/NUMBER
```

Then move it to **In Development** on the Mission Control board:
```bash
source ~/.config/marketinc/board.sh
board_set_status "OWNER/REPO" <ISSUE_NUMBER> "InDevelopment"
```
🐙 GitHub issue: https://github.com/OWNER/REPO/issues/N
```

If `gh` is not available or has no remote, skip silently and note it.

## Completion Signal

After all output is delivered, emit the completion signal on its own line:

```
ARCHITECT_DONE
```

If blocked at any point (missing critical info, unresolvable ambiguity), emit instead:
```
ARCHITECT_BLOCKED: <reason>
```
