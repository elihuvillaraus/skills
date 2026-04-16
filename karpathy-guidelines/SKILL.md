---
name: karpathy-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations on LLM pitfalls. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, and define verifiable success criteria. Universal — applies to all agents and all AI tools. Triggers on "karpathy", "think before coding", "don't assume", "simplify", "surgical changes", "success criteria".
license: MIT
source: https://github.com/forrestchang/andrej-karpathy-skills
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

> "The models make wrong assumptions on your behalf and just run along with them without checking. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."

> "LLMs are exceptionally good at looping until they meet specific goals... Don't tell it what to do, give it success criteria and watch it go."

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks (obvious one-liners, typo fixes), use judgment. For non-trivial work — anything that could cause regressions or require rework — apply these fully.

---

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple valid interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

**Banned behaviors:**
- Picking a silent interpretation of an ambiguous request and running with it
- Hiding confusion behind "I'll figure it out as I go"
- Implementing before surfacing a tradeoff that would change the decision

---

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

**The test:** Would a senior engineer say this is overcomplicated? If yes, simplify.

**Banned patterns:**
- Generic base classes for a problem with 1 concrete case
- Config objects with 15 fields when 3 are ever used
- "For future flexibility" arguments that add complexity now
- Wrapper functions that do nothing but call another function

---

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, **mention it — don't delete it**.

When your changes create orphans:
- Remove imports/variables/functions that **YOUR** changes made unused.
- Don't remove pre-existing dead code unless explicitly asked.

**The test:** Every changed line should trace directly to the user's request. If you can't explain why a line changed, undo it.

---

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform imperative tasks into verifiable goals:

| Instead of... | Transform to... |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |
| "Improve performance" | "Benchmark current time, implement change, verify X% improvement" |

For multi-step tasks, state a brief plan with explicit verification:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let the agent loop independently. Weak criteria ("make it work") require constant clarification and usually produce wrong results.

---

## How to Know It's Working

These guidelines are working when you see:
- **Fewer unnecessary changes in diffs** — Only requested changes appear
- **Fewer rewrites due to overcomplication** — Code is simple the first time
- **Clarifying questions come before implementation** — Not after mistakes
- **Clean, minimal PRs** — No drive-by refactoring, no "improvements"

---

## AGENTS.md / CLAUDE.md Snippet

Add this to any project's `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md` to make all AI tools follow these rules on that project:

```markdown
## Coding Behavior Guidelines (Karpathy)

1. **Think Before Coding** — State assumptions explicitly. If multiple interpretations exist, ask. Push back when a simpler approach exists.
2. **Simplicity First** — Minimum code that solves the problem. No speculative features, no single-use abstractions.
3. **Surgical Changes** — Touch only what you must. Match existing style. Mention unrelated dead code, don't delete it.
4. **Goal-Driven Execution** — Transform tasks into verifiable goals. Loop until success criteria are met.
```

---

## Pipeline Integration

These rules are already embedded in key pipeline agents — this skill makes them explicit and invocable on demand:

| Agent | Where Karpathy rules appear |
|---|---|
| `ralph` | Sprint Contract (Think Before Coding), TDD (Goal-Driven), output enforcement |
| `guardian-angel` | Simplicity First check, Surgical Changes diff review |
| `spec-writer` | Think Before Coding — defines what exists before ralph codes |
| `code-reviewer` | All 4 principles in the review checklist |

Use `/karpathy-guidelines` when:
- Onboarding a new project (add AGENTS.md snippet)
- A PR has unexpected drive-by changes
- A implementation came back overengineered
- You want to re-center an agent that's going in circles

---

## Copilot CLI Operations

### Signal
- Invoked as a reminder/overlay: `KARPATHY_DONE: [principle applied]`
- No blocking signal — this is a behavioral overlay, not a pipeline step
