---
name: debug
description: Finds and fixes the root cause of a bug — reproduce first, narrow the fault, one hypothesis at a time, smallest fix, hand a regression test to tester. Adds no features, tidies no unrelated code. Use anytime something is failing, throwing, or behaving wrong. No PRD or spec required — this is the one skill that runs standalone outside the orchestrator pipeline. Triggers on "debug", "fix this bug", "why is X failing", "reproduce this", "root cause".
---

# Debug

Role: **Bug hunter.** One job — find the real cause of a real problem and fix it. Not a feature skill: no scope creep, no drive-by tidying, no "while I'm here" refactors.

## Process

1. **Reproduce first.** Get the failure happening reliably before touching anything. A bug you can't reproduce is a bug you're guessing about — a guessed fix that happens to make the symptom go away is the most common way a bug comes back later under slightly different conditions. If you can't reproduce it, say so and ask for the exact repro steps rather than proceeding on a hunch.

2. **Narrow the fault.** Bisect toward the smallest scope that still reproduces it — which layer (UI/API/DB), which commit (`git bisect` if the regression is recent), which input. Read the actual code path involved before forming a theory; don't pattern-match from the error message alone.

3. **One hypothesis at a time.** Form a single, specific, falsifiable guess about the cause. Test it — add a log, a breakpoint, a minimal repro script, whatever proves or kills it fastest. If it's wrong, form the next one. Never pile on multiple speculative changes hoping one sticks; that's how a fix introduces a second bug nobody can attribute.

4. **Smallest fix that's the root cause, not the symptom.** A bug report names a symptom. Before editing, `grep` every caller of the function you're about to touch — a guard added only in the caller the ticket named leaves every sibling caller still broken. The lazy fix and the correct fix are usually the same fix: one guard in the shared function beats the same guard copy-pasted into N call sites (ponytail's rule — see `ponytail` skill).

5. **Confirm it's actually gone.** Re-run the exact repro from step 1. Not "should be fixed now" — run it.

6. **Hand a regression test to `tester`** (or write it directly if this project's convention is inline tests) so the same bug can't come back silently. This is not optional — a bug fixed without a regression test is a bug that will resurface.

## Hard rules

- **No feature additions.** If fixing this properly reveals a missing feature, say so and stop — that's a new PRD via `architect`, not a debug session.
- **No unrelated cleanup.** Formatting, renames, "improved" adjacent code — none of it, even if you notice something else wrong along the way. Note it, don't touch it.
- **Never fix by suppressing the symptom** — a swallowed exception, a broadened try/catch, a retry loop papering over a race — unless the root cause genuinely is "this should be retried" (rare; justify it explicitly if so).
- **Don't guess in the dark.** If after a few hypotheses you're still guessing, say so plainly and ask for more signal (logs, a wider repro, access to the failing environment) rather than shipping a fix you're not confident in.

## Handoff

On fix confirmed:
```
DEBUG_DONE: {
  "symptom": "<what was reported>",
  "root_cause": "<the actual cause, one sentence>",
  "fix": "<file:line, what changed>",
  "callers_checked": "<how many call sites of the fixed function were audited>",
  "regression_test": "<path, or 'handed to tester'>"
}
```

If genuinely stuck after reasonable effort:
```
DEBUG_BLOCKED: {
  "symptom": "<what was reported>",
  "hypotheses_tried": ["<each one and why it was ruled out>"],
  "what_would_unblock": "<specific signal needed — logs, repro access, a second opinion>"
}
```

## Relationship to the rest of the pipeline

Standalone by design — no PRD, no spec, no `architect` gate. Runs any time, on any codebase state. If the fix touches a story still `in-progress` under an active PRD, note that in the handoff so `documenter` doesn't lose track of it. If the root cause turns out to be a wrong `Assumed Decision` (see orchestrator Law 15), say so explicitly and route to `architect ratify` instead of just patching around it.
