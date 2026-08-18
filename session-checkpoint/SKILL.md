---
name: session-checkpoint
description: Save progress, decisions, learnings, and next steps to persistent memory before a context compact (manual /compact or auto-compact) or at any natural session boundary — using ONE fixed template and a clear decision tree for where to write it, instead of improvising a different format every time. Trigger on "prepare for compact", "save your progress", "checkpoint this session", "guarda el progreso", "prepara memoria persistente antes del compact", "deja todo listo para continuar", "antes de compactar", "save your learnings and next steps so we can continue later" — or run it proactively right before you invoke /compact yourself. Named `session-checkpoint` (not `checkpoint`) because Claude Code has its own built-in `/checkpoint` CLI command that the Skill tool cannot invoke — that name collision is reserved, don't rename this back to it.
---

# Session Checkpoint

One fixed ritual for "write down where we are so the next session — yours after a compact, or another agent entirely — can pick this up cold." The problem this solves: every agent was asked for this the same way and each produced a differently-shaped note (different sections, different files, different level of detail). This skill fixes the shape. It does not fix where memory lives for a given project — it routes to whatever this project already uses (Engram, the 4-file always-on-memory system, or a plain fallback file) and writes the same template into it every time.

## Why a file, not just a good /compact summary

Context compaction (manual or auto) summarizes the **conversation** — and any summary is lossy paraphrase, including the built-in one. A file on disk is not subject to that summarization at all; it survives verbatim. That is the entire reason this skill writes to disk instead of trusting the next compaction to remember the right details. Corollary: put in the file anything you would NOT trust an LLM summary to preserve faithfully — exact values, the exact next command to run, the exact reason something is blocked — not vibes.

## When to run this

- The user asks, in any phrasing close to the triggers above.
- Proactively, right before you run `/compact` yourself.
- At a natural stopping point even without an explicit compact: end of a working session, handing off to another agent/subagent, or a Priority group finishing in an orchestrator run.
- Never wait to be told twice in the same project — once you've located where this project checkpoints (see below), keep it current without being asked again.

## Hard Rules

1. **One template, always.** Use the exact structure in "The template" below. Do not invent sections, rename them, or reorder them per-session — the whole point is that it reads the same every time.
2. **Overwrite the current-state sections; never let this file grow into a log.** This is a snapshot of "where are we right now," not a diary. Superseded info is noise, not history. (Durable history has its own home — see the decision tree.)
3. **Concrete over vague.** "Next steps" are ordered, actionable, and literal: a command to run, a file to open, a check to make — never "continue working on the feature."
4. **Point at git and TaskList instead of duplicating them.** State the branch/commit and reference open task IDs; don't restate a diff or a task list in prose.
5. **Keep it short.** It must be cheap to re-read on resume. If a section would run long, link to the file/PR/doc instead of pasting it in.
6. **Read before you overwrite.** If a checkpoint file already exists, read it first — carry forward anything still true (open blockers, standing next steps) and drop what's done.

## Where to save — decision tree

Don't invent a new file if this project already has somewhere better. Check in this order and use every tier that applies (they serve different purposes, not alternatives to pick one from):

1. **Engram installed** (`which engram`) → this is the durable, cross-session, searchable layer. Always save here if available, regardless of the other tiers:
   ```bash
   engram save "Checkpoint $(date +%Y-%m-%d): <one-line state>" \
     "<the template body below>" \
     --type session --project <project-name>
   ```
   See the `memory` skill for the full Engram operations reference.

2. **Project has the 4-file always-on-memory system** (`AGENTS.md` + `docs/ALWAYS-ON-MEMORY.md` — check with `ls AGENTS.md docs/ALWAYS-ON-MEMORY.md`) → write the template into `docs/ALWAYS-ON-MEMORY.md` under that file's existing section structure (its "Learnings", "Blockers & Solutions", "Next Steps & Recommendations" map directly onto this skill's template — don't duplicate the file, fold into it). If a durable preference or correction also emerged this session, update `memory.md` too — that file is for standing preferences, not session state; see `always-on-memory` and `project-init`.

3. **Neither exists** (a plain repo, a one-off task, no pipeline scaffolding) → write a single `CHECKPOINT.md`:
   - Same directory as `AGENTS.md`/`CLAUDE.md` if one exists.
   - Otherwise the repo root.
   - Otherwise (not even a git repo — a throwaway or general chat) → say plainly there is nowhere durable to persist to, and print the template in the chat instead of inventing a random path.

4. **TaskList tool is in use** (open tasks from `TaskList`) → reference their IDs/status in "Next steps" instead of re-describing them.

Do all applicable tiers, not just the first match — Engram makes this searchable later ("what were we doing on skills-repo last Tuesday"); the project file is what a human or agent literally opens first.

## The template

```markdown
# Checkpoint — <project/task name>
Updated: <YYYY-MM-DD HH:MM> · Status: IN_PROGRESS | BLOCKED | DONE

## Done this session
- <concrete, verifiable — "added X to file:line", not "worked on X">

## In progress
- What: <exact current state of the unfinished thing>
- Where: <file:line / branch / commit>
- Why paused: <the actual reason, e.g. "waiting on API key" not "stopped here">

## Next steps (ordered, actionable)
1. <first literal action — a command, a file to open, a check to run>
2. ...

## Learnings / gotchas
- <anything a fresh agent would otherwise rediscover the hard way>

## Blockers
- <blocker> → needs: <what unblocks it, and from whom>

## Key context
- Branch: <name> · Commit: <short sha>
- Related files: <paths, not contents>
- Related tasks: <TaskList IDs if any>
```

Every heading is mandatory; write "None" rather than omitting a section — an agent scanning for "Blockers" and not finding the heading can't tell "no blockers" from "nobody checked."

## Workflow

1. **Locate.** Run the decision tree above. Note which tier(s) apply.
2. **Read what exists.** If a checkpoint already exists in the located tier(s), read it before writing — carry forward what's still true.
3. **Fill the template** from the actual session: what got done (verifiable, not summarized-feeling), the literal state of anything unfinished, ordered next actions, learnings worth not re-learning, blockers with what unblocks them, and the git/task pointers.
4. **Write it** to every applicable tier from step 1.
5. **Say where you put it** — one line: "Checkpoint saved to `docs/ALWAYS-ON-MEMORY.md` and Engram (project `skills`)." The user should never have to ask where to look after a compact.

## Companion automation (Claude Code only)

This skill covers the portable part — the format and the routing logic, usable from Claude Code, Copilot CLI, Gemini CLI, or Cursor. Claude Code specifically also has a `PreCompact` hook event (fires on both manual and auto compact) that can inject a reminder to run this skill without the user ever asking — the same mechanism already wired for `SessionStart` (matcher `compact`) in this machine's `~/.claude/settings.json`. That hook is not installed yet; ask the user before adding one (it's a settings.json change, not something this skill should do silently).
