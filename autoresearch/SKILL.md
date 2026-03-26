---
name: autoresearch
description: "Self-improving skill optimizer. Runs overnight experiments to improve any skill using binary evals and a Karpathy-style research loop. Generates variants of a skill, measures pass rate against deterministic test cases, commits improvements, discards failures. Use for: improving ralph, tester, architect, or any skill with measurable output. Triggered by: 'improve skill', 'autoresearch', 'optimize skill overnight', 'run experiments on'."
---

# AutoResearch

Role: **Self-Improving Skill Optimizer**.
You run automated experiments to improve skills using binary evaluation and git checkpointing.

Inspired by Karpathy's autoresearch pattern and Shopify's use of it to achieve 53% faster rendering via 93 autonomous commits.

## Core Loop

```
baseline → hypothesis → variant → eval → commit if better / reset if worse → repeat
```

---

## Phase 0 — Setup

### 0.1 — Identify skill target

The user specifies which skill to improve:
```
"Run autoresearch on tester"
"Improve the ralph skill overnight"
"Optimize architect for better PRD quality"
```

Read the target skill:
```bash
cat ~/.copilot/skills/<skill-name>/SKILL.md
```

### 0.2 — Define eval harness

Create `/tmp/autoresearch-<skill>-evals.md` with binary test cases:

```markdown
# Eval Harness for <skill>

## Test Cases (binary: PASS/FAIL)

### TC001: [Test description]
- Input: [what you'll provide to the skill]
- Expected: [specific, deterministic output]
- Assertion: [how to verify — grep for string, check file exists, count occurrences]

### TC002: ...
```

**Rules for good evals:**
- Binary ONLY — yes/no, present/absent, > threshold (not "looks good")
- Deterministic — same input always gives same answer
- Independent — each test case stands alone
- Measurable — can be checked programmatically

Example good assertions:
```bash
# ✅ Binary, measurable
grep -q "RALPH_DONE" output.txt && echo PASS || echo FAIL
[ $(grep -c "screenshot" output.txt) -ge 3 ] && echo PASS || echo FAIL
ls /tmp/eval-*.png | wc -l | grep -q "^[3-9]" && echo PASS || echo FAIL

# ❌ Not good
# "The output is clear" — subjective
# "The skill did a good job" — not deterministic
```

### 0.3 — Measure baseline

Run each test case against the current skill. Record:
```
Baseline pass rate: X/N (XX%)
Failing cases: TC003, TC007, TC012
```

---

## Phase 1 — Hypothesis Generation

Generate 3 hypotheses about why failing cases fail. Examples:
- "TC003 fails because the skill doesn't require screenshots in Phase 2"
- "TC007 fails because edge case testing is optional in the instructions"
- "TC012 fails because the completion signal format is ambiguous"

Pick the hypothesis most likely to improve pass rate without hurting passing cases.

---

## Phase 2 — Variant Creation (ONE change at a time)

Make EXACTLY ONE change to the skill. This is the most important rule — never change two things at once or you can't attribute improvement.

```bash
# Backup current version
cp ~/.copilot/skills/<skill>/SKILL.md /tmp/skill-backup.md

# Make the single targeted change
# (Edit the SKILL.md file)
```

Document what you changed:
```markdown
## Variant 1
- Hypothesis: "TC003 fails because..."
- Change: Added "REQUIRED: take screenshot before and after every interaction" to Phase 2
- Prediction: TC003 should now pass; TC001-TC002 unaffected
```

---

## Phase 3 — Evaluation

Run all test cases against the variant. Compare:

```
Variant 1 pass rate: X/N (XX%)
Baseline pass rate: X/N (XX%)
Delta: +X cases
```

---

## Phase 4 — Commit or Reset

**If improved** (pass rate went UP):
```bash
cd ~/.copilot/skills/<skill>
git add SKILL.md
git commit -m "autoresearch: improve <skill> (+X pass rate)

Change: [one sentence description]
Pass rate: X% → Y%
Test cases improved: TC003

Co-authored-by: AutoResearch <autoresearch@local>"
```

**If same or worse**:
```bash
cp /tmp/skill-backup.md ~/.copilot/skills/<skill>/SKILL.md
echo "Variant 1 discarded. Pass rate unchanged."
```

---

## Phase 5 — Repeat

Loop back to Phase 1 with the next hypothesis.

**Stopping criteria:**
- Pass rate reaches 100% (done)
- 3 consecutive variants with no improvement (likely at local maximum)
- User-specified iteration limit reached

---

## Running Overnight

Start a detached session:

```bash
copilot --allow-all --max-autopilot-continues 100
# Then Shift+Tab for autopilot, then:
# "Run autoresearch on tester for 20 iterations"
```

This runs ~12-15 experiments/hour. Overnight = 100+ experiments.

---

## Output Report

At completion:

```markdown
# AutoResearch Report: <skill>

## Summary
- Iterations: N
- Start pass rate: X%
- Final pass rate: Y%
- Improvement: +Z percentage points
- Commits made: N (improvements kept)
- Variants discarded: N

## Changes Made

### Commit 1: [description]
- Test cases fixed: TC003
- Pass rate delta: +5%

### Commit 2: [description]
- Test cases fixed: TC007
- Pass rate delta: +3%

## Remaining Failures
- TC012: [description of persistent failure — may need human input]

## Next Steps
- [Recommendation for further improvement]
```

---

## Applying to Product Code (not just skills)

AutoResearch works on any code with a measurable outcome:

**Example: Optimize a React component**
```markdown
Target: app/components/ProductCard.tsx
Metric: Lighthouse performance score for /products page
Baseline: 72/100
Test: npx lighthouse http://localhost:3000/products --output json | jq .categories.performance.score
Goal: >0.90
```

**Example: Improve a prompt in your app**
```markdown
Target: lib/prompts/summarize.ts
Metric: % of outputs that are < 3 sentences AND contain key topic
Baseline: 41%
Test: node scripts/eval-summarize.js
Goal: >80%
```

---

## Non-negotiable rules

1. **ONE change per variant** — never change two things at once
2. **Eval harness is LOCKED** — never modify test cases after establishing baseline (prevents gaming)
3. **Commit improvements immediately** — git is your checkpoint system
4. **Binary assertions only** — no subjective scoring
5. **Document every variant** — even discarded ones, in the report
