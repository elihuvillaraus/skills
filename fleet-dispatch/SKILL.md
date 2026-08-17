---
name: fleet-dispatch
description: Hand a piece of work to a DIFFERENT AI provider's CLI (Copilot, Codex, OpenCode, Gemini, Cursor, etc.) via Orca, using that provider's own subscription instead of burning Claude Code usage. Fires two ways — automatic (the orchestrator routes mechanical/low-risk work here without asking: documenter-type steps, Rigor Tier Prototype/Alpha stories, single-file trivial fixes) and explicit (the user names a provider: "mándale esto a Copilot", "usa OpenCode para esto", "no gastes Claude en esto", "manda esto a Codex/Gemini"). Never fires for planning, judges, architect, dia-del-juicio, or anything touching auth/payments/migrations — those stay on Claude regardless of tier. Requires the `orca` CLI installed and the repo to be Orca-managed. Triggers on "/fleet-dispatch", a named-provider request, or the orchestrator's own Phase 3 routing check.
---

# Fleet Dispatch

The user pays for five things (Claude Code, GitHub Copilot, OpenCode, Gemini, ChatGPT/Codex) and was manually bridging between them — planning in one, re-explaining context in another — which cost more time than it saved and turned the user into the orchestrator instead of the AI. This skill fixes that by making **Claude Code itself** the one that hands work to another provider's CLI, through Orca's own scriptable orchestration layer, and reads the result back. The user stops being the bridge.

## Before anything: pull the live guide, never hardcode `orca` flags

Orca ships its own version-matched skill guides through its CLI. **This skill's own author confirmed a real drift**: Orca's public docs page and the actual installed CLI's `--help` output disagreed on `orchestration` flags during authoring. Do not trust any command written below as gospel — they illustrate the *shape* of the mechanism, not a copy-paste script. Every time this skill runs:

```bash
orca skills get orca-cli
orca skills get orchestration
```

Read those, then use whatever the current guide says. If `orca skills get` itself fails or the `orca` command isn't found, stop and tell the user — don't invent a workaround.

## When this fires

**Automatic — orchestrator routes here without asking:**
- A Phase 4 `documenter`-style step (commit + doc update, already low-stakes).
- A Rigor Tier **Prototype** or **Alpha** story that's a small, single-file, mechanical change (per orchestrator Phase 3 step 1).
- Trivial fixes: typos, formatting, a one-line change, dependency bumps with no logic change.

**Explicit — the user names a provider or says something equivalent to "don't spend Claude on this":**
- "mándale esto a Copilot / OpenCode / Codex / Gemini"
- "usa otro proveedor para esto"
- "no ocupes Claude para esto"

**Never automatic — these always stay on Claude regardless of Rigor Tier:**
- Planning/architecture: `architect`, `dia-del-juicio` judges, `software-architect`.
- Anything touching auth, payments, or a migration.
- Rigor Tier **Beta** or **GA** stories.
- Anything the user hasn't asked to move and doesn't meet the automatic criteria above — when in doubt, keep it on Claude. This skill exists to save tokens on the *safe* work, not to gamble on the load-bearing work.

## Workflow

1. **Verify preconditions.** `which orca` — if missing, tell the user and stop (don't fall back to raw `git worktree` or another mechanism; that's a different, unverified path). Confirm the current repo is Orca-managed (`orca worktree current` or `orca repo show`, per the live guide) — if it isn't, tell the user this needs the repo registered with Orca first.

2. **Pull the live guides** (above) — do this every run, not just once; Orca updates.

3. **Pick the target provider.** If the user named one, use it. If automatic, default to whichever provider the user actually has active capacity on (ask if genuinely ambiguous — this skill has no way to query remaining Claude/Copilot/etc. quota itself; Orca's usage/rate-limit view is desktop-app-only, not exposed via this CLI as of authoring). Known agent ids observed on this machine's guide: `claude`, `codex`, `omp`, `pi`, `grok`, `opencode`, `gemini`, `cursor`, `droid` — GitHub Copilot is supported by Orca generally (per its README's agent list) even though it wasn't named in the fetched guide text; confirm the exact id via the live guide or `orca worktree create --help` before using an id you haven't seen confirmed.

4. **Dispatch.** Shape (verify against the live guide, don't trust this verbatim):
   ```bash
   orca worktree create --name <short-task-name> --agent <provider-id> --prompt "<the actual task, with enough context to stand alone — the other provider has none of this conversation>" --json
   ```
   The prompt must be self-contained: the receiving provider has zero memory of this session. Include the file paths, the acceptance criteria, and anything a fresh agent would need — the same discipline as briefing a fresh subagent per this catalog's own norms.

5. **Wait, then read the result** using the live guide's current `terminal wait` / `orchestration check` commands — don't poll in a tight loop; use the guide's blocking/wait primitive.

6. **The output still goes through the same quality gates its Rigor Tier calls for.** Dispatching to another provider changes *who executed the story*, not *what verifies it* — a dispatched Prototype/Alpha story still follows orchestrator Phase 3 steps 5-7 exactly as if `ralph` had written it (TDD gate always; evaluator/guardian-angel per tier). Never treat another provider's self-report as sufficient on its own.

7. **Report back** to whoever called this skill (the orchestrator, or the user directly): which provider ran it, the worktree/branch it produced, and the result — success, needs review, or blocked.

## Completion signal

```json
{
  "signal": "FLEET_DISPATCH_DONE",
  "provider": "copilot",
  "worktree": "...",
  "task": "US004 — rename button label",
  "outcome": "succeeded | needs_review | failed",
  "notes": "..."
}
```
Or `FLEET_DISPATCH_BLOCKED` with a reason (orca not installed, repo not Orca-managed, provider unavailable, dispatch failed) — never silently fall back to running the work in Claude without saying so; that would defeat the reason this exists.

## Notes

- This is a cost/throughput tool, not a quality gate — it doesn't replace `evaluator`, `guardian-angel`, or `tester`, and it isn't a Pipeline Law (it's conditional and opt-in by design, unlike the always-active laws in `orchestrator`).
- Don't auto-merge a dispatched worktree's output without the same review the user already applies to Claude's own work.
- If a provider's output is bad, that's signal to stop routing that category to that provider — not a reason to silently abandon the mechanism entirely.
- See also `orchestrator`'s Phase 3 step 1 and Quick Reference table for where this plugs into the main pipeline.
