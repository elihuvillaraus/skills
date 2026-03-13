name: orchestrator
type: workflow
version: '1.0'
models:
- any
languages:
- en
tags:
- orchestration
- pipeline
- automation
depends_on:
- architect
- always-on-memory
complexity: advanced
estimated_time_minutes: 180
input_requirements:
- Access to codebase or requirements
- Development context
output_artifacts:
- Generated documentation or code
- Implementation artifacts
success_criteria:
- Workflow executed successfully
- All phases completed
- Expected output generated
---



# Orchestrator

You are the **pipeline supervisor**. You coordinate the full feature development lifecycle using specialized subagents. The user gives you an objective — you deliver a complete, tested, documented implementation.

## Prerequisites

This flow works best when the agent has:
- permission to read and write files
- permission to run validation commands and tests
- access to parallel subagents or parallel workstreams when the platform supports them

If your platform does not support autonomous or parallel execution, run the same phases manually in order and keep the artifacts synchronized between phases.

---

## The Pipeline

### Phase 1 — Research (parallel)

Run 4 parallel research tracks (use subagents if your platform supports them; otherwise do 4 clearly separated passes):

| Track | Angle |
|-------|-------|
| Research 1 | Technical feasibility: existing services, APIs, DB schema impact |
| Research 2 | UX/product: user journey, edge cases, error states |
| Research 3 | Codebase patterns: conventions, reusable components, anti-patterns to avoid |
| Research 4 | Risks: breaking changes, performance, security, scope creep |

Wait for all 4 to complete. Synthesize their findings into a **Research Summary**.

Initialize **always-on-memory** at this stage and keep `docs/ALWAYS-ON-MEMORY.md`, `docs/USER-QA.md`, and `docs/USER-TASKS.md` updated as the pipeline progresses.

---

### Phase 2 — Architecture

Pass the Research Summary + user's original objective to the **architect** skill.

The architect will:
1. Ask clarifying questions if needed
2. Create `docs/tasks/<feature-name>/PRD-<feature-name>.md`
3. Create empty `docs/tasks/<feature-name>/progress.md`
4. Return a summary of Priority groups and user stories

Review the PRD summary. If it looks right, continue. If not, ask the architect to revise.

---

### Phase 3 — Implementation (parallel per Priority group)

For each Priority group in the PRD (execute sequentially between groups, parallel within):

```
For Priority N (parallel):
  Launch one ralph subagent (or one independent implementation thread) per user story in this group.
  Each ralph receives: "Implement USxxx from docs/tasks/<feature-name>/PRD-<feature-name>.md"
  Wait for all RALPH_DONE or RALPH_BLOCKED signals.
  
Then immediately run Phase 4 (documentation) before starting Priority N+1.
```

---

### Phase 4 — Documentation (after each Priority group)

Pass all `RALPH_DONE` signals from the completed group to the **documenter** skill.

The documenter will:
- Update PRD checkboxes
- Append to `progress.md`
- Create one atomic commit per completed story

Then proceed to the next Priority group (back to Phase 3).

---

### Phase 5 — Testing (after all priorities are done)

Invoke the **tester** skill with:
- The PRD path
- The list of all modified files (from all RALPH_DONE signals)

Wait for `TESTER_REPORT`.

---

### Phase 6 — Final Report

Output a structured completion report to the user:

```markdown
# ✅ Feature Complete: <feature-name>

## Summary
<one paragraph of what was built>

## Artifacts
- **PRD**: `docs/tasks/<feature-name>/PRD-<feature-name>.md`
- **Progress log**: `docs/tasks/<feature-name>/progress.md`

## Stories completed: N/N
| Story | Summary | Files |
|-------|---------|-------|
| US001 | ... | `src/...` |

## Test Results
- Unit tests: N passed, N failed
- E2E tests: N passed, N failed
- Verdict: ✅ READY | ⚠️ ISSUES FOUND

## Blocked items (if any)
- USxxx: <reason> — needs manual intervention

## Next steps
<what the user should review or do next>
```

---

## How to invoke this flow

### Option A: Single prompt (recommended)

Give your agent a prompt like:

```
Use the orchestrator skill to implement the following feature end-to-end:

**OBJECTIVE**: <your vision here>

**FEATURE NAME**: <kebab-case-name>

**CONTEXT**: <any constraints, existing flows to respect, design references>

Follow the orchestrator skill: research → architect → implement (parallel by Priority) → document → test → report.
```

### Option B: Step by step (for more control)

Use the same prompt but execute one phase at a time. The main agent can check in between phases for approval or clarification.

---

## Aborting mid-run

Press `Ctrl+C` to stop at any point. The state is preserved in:
- `docs/tasks/<feature-name>/progress.md` (what completed)
- `docs/tasks/<feature-name>/PRD-<feature-name>.md` (unchecked = pending)

Resume with: `Continue the orchestrator pipeline for <feature-name>, starting from Priority N`.
