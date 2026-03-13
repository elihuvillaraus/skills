name: always-on-memory
type: workflow
version: '1.0'
models:
- any
languages:
- en
tags:
- memory
- documentation
- decisions
- qa
- handoff
depends_on: []
complexity: moderate
estimated_time_minutes: 15
input_requirements:
- Access to requirements, PRD, or active implementation context
- Ability to write files or return markdown for the user to save
output_artifacts:
- docs/ALWAYS-ON-MEMORY.md
- docs/USER-QA.md
- docs/USER-TASKS.md
success_criteria:
- Decisions are captured continuously as work progresses
- Manual QA scenarios are documented for the user
- User-owned follow-up actions are separated from agent work
---



# Always On Memory

Role: **Persistent project memory system**.
You maintain structured documentation throughout planning and execution so important context is never lost between architect, orchestrator, ralph, tester, and the user.

## Purpose

Create and continuously maintain three durable documents:

1. `docs/ALWAYS-ON-MEMORY.md` — architecture decisions, assumptions, constraints, learnings, and open questions
2. `docs/USER-QA.md` — manual QA scenarios the user should run
3. `docs/USER-TASKS.md` — actions only the user can perform (secrets, dashboards, production setup, approvals, external config)

These files are the long-lived memory of the project. They must stay current while work is happening, not only at the end.

## Process

### Phase 1 — Initialize memory

If the files do not exist, create them immediately.

Use these starter sections:

#### `docs/ALWAYS-ON-MEMORY.md`
- Overview
- Decisions
- Constraints
- Known risks
- Open questions
- Learnings

#### `docs/USER-QA.md`
- Environment / setup notes
- Test scenarios
- Expected outcomes
- Known limitations

#### `docs/USER-TASKS.md`
- Required credentials or secrets
- Dashboard / vendor configuration
- Deployment or rollout tasks
- Post-launch checks

### Phase 2 — Capture decisions in real time

As soon as a meaningful decision is made, record it in `docs/ALWAYS-ON-MEMORY.md`.

Capture items such as:
- chosen architecture or library direction
- scope boundaries and explicit non-goals
- migration or rollout constraints
- discovered edge cases
- conventions the implementation should follow
- important tradeoffs and why they were made

Do not wait until the end to write these down.

### Phase 3 — Track user-owned work separately

Whenever you find work that the agent cannot complete directly, add it to `docs/USER-TASKS.md`.

Examples:
- add API keys or secrets
- configure third-party dashboards
- enable production webhooks
- perform manual approvals
- provision external resources

Only include tasks that genuinely require the user or an external human owner.

### Phase 4 — Maintain QA handoff

Whenever implementation introduces behavior that should be manually validated, add it to `docs/USER-QA.md`.

Each QA item should include:
- scenario name
- setup or preconditions
- exact user actions
- expected result
- notes on platform / environment if relevant

Prefer actionable, reproducible steps over vague suggestions.

### Phase 5 — Keep memory synchronized

On every major phase transition (research → architecture → implementation → testing → handoff), review all three files and update them.

Ensure:
- resolved questions are marked as resolved
- stale assumptions are corrected
- QA steps reflect actual implementation
- user tasks only contain outstanding actions

## Decision Rules

Use this split consistently:

- `ALWAYS-ON-MEMORY.md` → stable context the team should remember
- `USER-QA.md` → manual validation steps
- `USER-TASKS.md` → tasks the user must do personally

Do **not** put agent-executable implementation work into `USER-TASKS.md`.
Do **not** put transient brainstorming into memory unless it affected a real decision.

## If tools are available

- Create or update the three files directly
- Preserve existing content that is still valid
- Append new entries with clear headings and timestamps when useful
- Keep the documents readable and concise

## If tools are not available

Return three Markdown blocks labeled:
- `ALWAYS-ON-MEMORY.md`
- `USER-QA.md`
- `USER-TASKS.md`

so the user can save them manually.

## Output

Confirm with a summary like:

```text
🧠 Always-on memory synchronized
- Updated: docs/ALWAYS-ON-MEMORY.md
- Updated: docs/USER-QA.md
- Updated: docs/USER-TASKS.md
```
