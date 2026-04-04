---
name: memory
description: "Persistent memory layer for the pipeline. Uses Engram to save, search, and restore context across sessions. Use for: saving architecture decisions, loading project context at session start, searching past patterns before coding, recording experiment learnings. Triggered by: 'save to memory', 'search memory', 'load project context', 'remember this', 'what did we decide about'."
---

# Memory

Role: **Persistent Memory Layer** (Engram wrapper).

You manage cross-session, cross-agent memory using Engram's SQLite + FTS5 backend.
Every agent in the pipeline calls you. You outlive individual sessions.

---

## Setup (one-time per machine)

```bash
# Verify engram is installed
engram --version

# If not installed:
brew install gentleman-programming/tap/engram

# Configure Copilot CLI MCP (add to ~/.vscode/mcp.json or user profile):
# {
#   "mcp": {
#     "engram": {
#       "type": "stdio",
#       "command": "engram",
#       "args": ["mcp", "--tools=agent"]
#     }
#   }
# }
```

---

## Operations

### Save a memory
```bash
engram save "<title>" "<content>" \
  --type <TYPE> \
  --project <project-name>

# TYPE values:
# architecture  → tech decisions, ADRs, system design
# learning      → experiment results, what worked/failed
# decision      → approved/rejected stories, evaluation outcomes
# bugfix        → bugs found and how they were resolved
# context       → general project context, conventions
# session       → end-of-session summary
```

**Examples:**
```bash
# Architect saves a PRD decision
engram save "Auth strategy: Better Auth + JWT" \
  "Decided to use Better Auth v2 with JWT (not sessions) for mobile compat. Ruled out Lucia — unmaintained." \
  --type architecture --project myapp

# Ralph saves a pattern learned
engram save "Drizzle migration pattern" \
  "Always run db:push before testing. Schema changes need explicit column type — never infer." \
  --type learning --project myapp

# Evaluator saves a rejection
engram save "US003 REJECTED: missing error state" \
  "Ralph did not handle 401 response on /api/auth/login. No toast shown to user. Must add error boundary." \
  --type decision --project myapp

# AutoResearch saves experiment
engram save "autoresearch-ralph-exp-007: +12% eval pass rate" \
  "Adding explicit 'out of scope' section to Sprint Contract increased evaluator pass rate from 71% to 83%. Variant saved as ralph-v2." \
  --type learning --project skills
```

### Search memories
```bash
engram search "<query>" \
  --type <TYPE> \
  --project <project-name> \
  --limit 5

# Examples:
engram search "auth middleware" --project myapp
engram search "evaluation rejection" --type decision --limit 10
engram search "drizzle schema" --type learning
```

### Load context at session start (Phase 0)
```bash
# Show recent context for current project (auto-detects from git remote)
engram context

# Explicit project name
engram context myapp
```

### Session summary (end of session)
```bash
engram save "Session $(date +%Y-%m-%d): <what was accomplished>" \
  "<summary of decisions, blockers, next steps>" \
  --type session --project <project-name>
```

### Sync across machines
```bash
# Before switching machines: export to git-tracked .engram/ folder
engram sync

# On new machine: import from .engram/ folder
engram sync --import

# Check sync status
engram sync --status
```

---

## Pipeline Integration Points

### Orchestrator (Phase 0)
```bash
# Load project context before starting pipeline
engram context
# Returns recent architecture decisions, open learnings, last session summary
```

### Architect (after PRD created)
```bash
engram save "PRD: <feature-name>" \
  "<summary of priority groups, key decisions, constraints>" \
  --type architecture --project <project>
```

### Ralph (before coding each story)
```bash
# Search for similar patterns before writing code
engram search "<story title or domain>" --type learning --limit 3
engram search "<technical domain>" --type architecture --limit 3
```

### Evaluator (after each verdict)
```bash
# On APPROVED:
engram save "APPROVED: <story-id> <story-title>" \
  "Passed all criteria. Key: <what made it pass>" \
  --type decision

# On REJECTED:
engram save "REJECTED: <story-id> — <reason>" \
  "Failed: <specific criterion>. Fix needed: <description>" \
  --type decision
```

### Documenter (after each commit)
```bash
engram save "commit: <story-id> <story-title>" \
  "Files changed: <list>. Notable: <any architectural learnings>" \
  --type bugfix
```

### AutoResearch (after each experiment)
```bash
engram save "autoresearch-<skill>-exp-<N>: <result>" \
  "Hypothesis: <what was tested>. Result: <pass rate before/after>. Kept: <yes/no>. Reason: <why>" \
  --type learning --project skills
```

---

## Completion Signals

- Success: `MEMORY_SAVED: <title>`
- Search complete: `MEMORY_SEARCH_DONE: <N> results`
- Context loaded: `MEMORY_CONTEXT_LOADED`
- `MEMORY_BLOCKED: engram not installed` → run `brew install gentleman-programming/tap/engram`
