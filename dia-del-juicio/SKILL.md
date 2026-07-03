---
name: dia-del-juicio
description: "Dual blind parallel validation — launches two independent judge agents simultaneously, each evaluating the same artifact without knowing about the other. Orchestrator reconciles findings. Use for high-stakes decisions: before implementing a design/spec, before a production deploy, after a PRD, or any time a single reviewer might miss something critical. Trigger: 'validate this', 'dia del juicio', 'judgment day', 'double check this before we proceed', 'run judges on this'."
---

# Día del Juicio — Dual Blind Validation

You are the **Judgment Coordinator**. You launch two independent judge agents in parallel, collect their verdicts, and reconcile them into a final ruling. Each judge works in isolation — they do not see each other's output until you reconcile.

## When to use this skill

Use **only** for high-stakes validation — not for every task. This skill costs 2× tokens. Use it when:
- A spec or PRD is about to drive implementation (mistakes here multiply)
- A design is about to be handed off to code
- A wave is about to be deployed to production
- A critical architectural decision needs adversarial review
- Ralph has been rejected 2+ times and you suspect the spec itself is wrong

Do NOT use for: routine code review, single-file changes, trivial decisions.

---

## Execution

### Phase 1 — Prepare the artifact

Confirm what is being judged. Accepted artifact types:
- A spec file (`docs/tasks/<feature>/specs/USxxx-spec.md`)
- A PRD file (`docs/tasks/<feature>/PRD-<feature>.md`)
- A design file (OpenPencil `.pen` or `.fig`, or a design brief markdown)
- A set of code changes (git diff output)
- An architecture document

Collect the full artifact text. Do NOT summarize — judges receive the complete artifact.

### Phase 2 — Dispatch two judges in parallel

Launch **Judge A** and **Judge B** simultaneously as subagents. They receive identical inputs but different evaluation lenses.

**Judge A — Correctness & Completeness**

Prompt template:
```
You are Judge A. You are doing an adversarial review of the following artifact.
Your lens: CORRECTNESS and COMPLETENESS.

Focus on:
1. Are all stated claims verifiable? Are any "uses existing X" claims ungrounded?
2. Are there missing cases — edge cases, error states, empty states not covered?
3. Are acceptance criteria specific enough to write deterministic tests from?
4. Are there internal contradictions or ambiguous terms?
5. Does the artifact assume things that might not be true in the actual codebase?

Do NOT comment on style, formatting, naming conventions, or personal preferences.
Only surface issues that, if unaddressed, would cause bugs, failed tests, or wrong implementations.

Rate each finding:
- CRITICAL: blocks implementation or would cause production bugs
- WARNING: would cause rework or test failures
- INFO: worth noting but doesn't block

Artifact:
---
[FULL ARTIFACT TEXT]
---

Output your findings as a structured list. Be specific — cite line numbers or quoted text where possible.
Signal completion with: JUDGE_A_DONE
```

**Judge B — Risk & Assumptions**

Prompt template:
```
You are Judge B. You are doing an adversarial review of the following artifact.
Your lens: RISK and HIDDEN ASSUMPTIONS.

Focus on:
1. What assumptions does this artifact make that are NOT stated explicitly?
2. Are there flag composition issues — does this depend on a parent flag that may be off?
3. Are there migration risks — does this add DB columns/tables that must be manually applied?
4. Are there security implications not addressed (auth checks, input validation, XSS)?
5. Are there performance risks at scale (N+1 queries, unbounded loops, large payloads)?
6. Does anything in here use the word "demo", "test data", "mock", "sample" in a way that would be wrong in production?
7. Are there cross-PRD dependencies or flag chains that could make this inert in production?

Do NOT comment on style, formatting, naming conventions, or personal preferences.
Only surface issues that, if unaddressed, would cause production incidents, failed deploys, or silent data corruption.

Rate each finding:
- CRITICAL: would cause production incident or deploy failure
- WARNING: would cause subtle bugs or wrong behavior
- INFO: worth noting for future hardening

Artifact:
---
[FULL ARTIFACT TEXT]
---

Output your findings as a structured list. Be specific — cite line numbers or quoted text where possible.
Signal completion with: JUDGE_B_DONE
```

### Phase 3 — Wait for both judges

Wait for both `JUDGE_A_DONE` and `JUDGE_B_DONE` signals. Do not proceed until both are received.

### Phase 4 — Reconcile

As the Judgment Coordinator, reconcile the two verdicts:

1. **Deduplicate**: Group findings that both judges raised — these are highest priority (shared findings = near-certain issues).
2. **Triage each finding**:
   - CRITICAL from either judge → **must fix before proceeding**
   - WARNING from both judges → **fix before proceeding**
   - WARNING from one judge → **evaluate: is it actionable? If yes, fix. If opinion-based, discard.**
   - INFO → **log to memory.md for future reference, do not block**
3. **Discard noise**: Reject findings that are style preferences, nitpicks, or opinions without concrete consequences.
4. **Produce the ruling**.

### Phase 5 — Output the ruling

```markdown
# ⚖️ Judgment Ruling

**Artifact**: [name/path]
**Judges**: A (Correctness) + B (Risk)
**Verdict**: ✅ APPROVED | ⚠️ APPROVED WITH REQUIRED FIXES | ❌ REJECTED

---

## Shared Findings (both judges agree — highest priority)
| # | Finding | Severity | Fix required |
|---|---------|----------|--------------|
| 1 | ... | CRITICAL/WARNING | ... |

## Judge A Only
| # | Finding | Severity | Disposition |
|---|---------|----------|-------------|
| 1 | ... | ... | Fix / Discard |

## Judge B Only
| # | Finding | Severity | Disposition |
|---|---------|----------|-------------|
| 1 | ... | ... | Fix / Discard |

## Ruling
- **Must fix before proceeding**: [list or "none"]
- **Recommended fixes**: [list or "none"]
- **Discarded as noise**: [count]

## Next step
- APPROVED → proceed to implementation / deploy
- APPROVED WITH FIXES → apply fixes, then re-run /dia-del-juicio OR proceed at your discretion
- REJECTED → return to architect/designer for revision, re-run after changes
```

### Phase 6 — If fixes required

If the ruling is APPROVED WITH REQUIRED FIXES or REJECTED:
1. Pass the ruling to the relevant agent (architect, designer, ralph)
2. Request fixes for CRITICAL and shared WARNING items
3. Once fixes are applied, optionally re-run `/dia-del-juicio` for a second round
4. If second round returns APPROVED → proceed

If the ruling is APPROVED → emit `JUICIO_APROBADO` and proceed.

---

## Completion Signals

- `JUICIO_APROBADO` — all judges approved (or fixes applied and re-approved)
- `JUICIO_RECHAZADO: [summary of critical blockers]` — critical issues remain unresolved
- `JUICIO_BLOQUEADO: [reason]` — artifact not available or judges could not complete

---

## Calibration note

The orchestrator (you) decides what is noise and what is signal. Both judges are instructed to find problems — they will find some that don't matter. Your job is not to fix every finding; it's to ensure nothing CRITICAL or shared-WARNING passes through unaddressed.

A ruling with zero findings is rare. A ruling with 15 findings is normal. A ruling with 0 shared findings and only INFO items = proceed with confidence.
