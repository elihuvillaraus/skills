# Checkpoint — skills catalog maintenance + second-brain/agentic-os build session
Updated: 2026-09-25 21:10 · Status: IN_PROGRESS

## Done this session
- Replaced `architecture-diagram`/`process-flow-diagram` with `diagram-design` (per user choice via AskUserQuestion).
- Reviewed `taste-skill` vs `output-skill`/`redesign-skill`/`soft-skill` and merged/installed.
- Installed ClickHouse's official `clickhouse-best-practices` skill (resolved to real repo `ClickHouse/agent-skills`), then `clickhouse-architecture-advisor` (self-hosted ClickHouse used by Apollo/Atenea/Spatial CDPs).
- Added explicit "voiceover sets the pace, never the reverse" documentation to `hyperframes-helper`.
- Reviewed and installed `archify` (`tt-a1i/archify`) vs `diagram-design`, verified via `doctor`.
- Delivered skill-usage stats (most/least used) from `~/.agents/skill-usage.log`.
- Applied Opus 5.5 prompting-guide findings to `orchestrator/SKILL.md` (Phase 3 + Pipeline Laws) — commit `540a54f` (already on `main`, pre-dates this checkpoint window).
- Built and fully debugged `~/second-brain` (port 5210) — workspace force-graph visualizer, NOT git-tracked (local tool only):
  - Fixed a scan hang (`scan.js` walked the entire home dir) with an `ALLOWED_TOP_LEVEL` allowlist.
  - Fixed skills being misclassified as a Memory-layer "department" instead of the Skills layer — `addFoldedDir()` was hardcoding `.claude/skills/` instead of reusing `layerOf()`.
  - Fixed a phantom "CLAUDE.md" node (file doesn't exist on this machine) by introducing `ROUTER_DOC`, dynamically resolved from the user's real always-loaded index (`.claude/projects/-Users-elihuvillaraus/memory/MEMORY.md`). Two hardcodes existed (`'CLAUDE.md'` and a separate uppercase `'CLAUDE.MD'` in `index.html` found only via visual re-check) — both fixed across `scan.js`, `_core.js`, `index.html`.
  - Fixed a server crash ("nada está conectado") caused by `/api/open` using a Windows-only `spawn('cmd', ...)` with no error handler on macOS — added platform detection, try/catch, `child.on('error', ...)`, plus global `uncaughtException`/`unhandledRejection` handlers.
  - Rebranded fully to MarketINC Dev Studio & Agency (violet/cyan palette, real asset files from `ai-content-machine/marcus`, dropped all RoboNuggets branding/links).
  - Decluttered `Docs/SaaS` from 114 raw folders into one `project:` node per department — rebuilt `config/departments.json` to 15 real independent products (not merged) after user corrected my first "5 departments" proposal.
- Built and installed `~/agentic-os` (port 50000) — action-oriented dashboard, NOT git-tracked (local tool only): real headless-Claude-Code skill-deck runner (`claude -p "/{skill}" --model {model} --effort {effort}`, verified working, deliberately NOT using `--permission-mode bypassPermissions`), artifacts ring, rebranded to MarketINC. Calendar/Email/Stats/Routines widgets intentionally left unwired (need user's own OAuth/scheduler data — not a bug).
- Reviewed `github.com/affaan-m/ECC` (real Anthropic hackathon winner). Verified one of its env-var recommendations against official docs and applied it: added `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "50"` to `~/.claude/settings.json` (confirmed present on disk). Did NOT add `MAX_THINKING_TOKENS` or `CLAUDE_CODE_SUBAGENT_MODEL` — neither exists in official Claude Code docs as such (real subagent-model mechanism is `ANTHROPIC_DEFAULT_HAIKU_MODEL`/`_OPUS_MODEL`/`_SONNET_MODEL`).
- **Permanent hard rule established**: user requires neutral/Mexican Spanish (tú-forms) always, never Argentine voseo. Saved to `~/.claude/projects/-Users-elihuvillaraus/memory/feedback_spanish_register.md`, indexed in `MEMORY.md`. Checked entire skills catalog for voseo sourcing — found none, was pure model drift.

## In progress
- What: ECC findings were verified and one settings.json change applied, but the findings were never delivered to the user in prose (interrupted by a context-compaction event mid-turn).
- Where: `~/.claude/settings.json` env block (see Key context for exact diff already applied).
- Why paused: conversation was compacted before the explanatory message could be sent.

## Next steps (ordered)
1. Tell the user, in Mexican Spanish (tú-forms): `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50` is added and verified real; the other two ECC-suggested env vars are not real Claude Code settings, so they were skipped.
2. Ask the user which (if any) ECC pieces to cherry-pick — this is a genuine multi-option choice, nothing should be installed without sign-off:
   - `skills/skill-stocktake/`
   - `skills/cost-aware-llm-pipeline/`
   - `skills/security-scan/` (has an external npm dep on `ecc-agentshield` — flag that explicitly)
   - the instincts/continuous-learning-v2 hook system (flagged as high-integration-cost, worth a dedicated follow-up only if wanted)
3. If the user picks any cherry-pick target: vendor it through the normal pattern (clone/verify license → `~/.agents/skills/<name>` → symlink into `~/.claude/skills` + `~/.copilot/skills` → mirror into `~/Docs/SaaS/skills-repo` → commit with the current session's attribution trailer → push).

## Learnings / gotchas
- `~/second-brain` and `~/agentic-os` are deliberately local-only, not git repos, not mirrored into skills-repo — they are personal dashboards, not catalog skills. Don't try to commit/push them as if they were.
- When fixing hardcoded strings across a codebase, grep alone is not enough — this session had a hardcode (`'CLAUDE.MD'`, different case) that only surfaced via a visual browser re-check after the first fix looked complete. Re-verify visually, don't just trust the grep count.
- "Department" in the second-brain config is a visual color-grouping label only, not an org chart — the user's products (Sellia, Atenea, Zeus, Chatia, Walloy, Mercurio, Marcus, Pitonisa/Apollo, Argus, Spatial, Gaia, Speechlytics, Controlai) are all independent SaaS/PaaS products, never merge them into fewer buckets without asking.
- Argentine voseo drift is an easy pattern to slip back into mid-correction (it recurred once immediately after the user's own correction this session) — actively check every Spanish sentence for -ás/-és/-ís endings and "vos" before sending, not just the first one after a correction.
- Claude Code's default (non-bypassed) permission mode works fine in headless `-p` mode as long as the invoking environment's `settings.json` already allowlists the tool calls the skill needs — confirmed empirically via a real `/skill-tracking` test run, no need to reach for `--permission-mode bypassPermissions`.

## Blockers
None.

## Key context
- Branch: `main` · Commit: `540a54f` (last skills-repo commit; this checkpoint file itself is currently untracked/uncommitted).
- `~/.claude/settings.json` `env` block currently on disk:
  ```json
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "0",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "50"
  }
  ```
- Related files: `~/second-brain/` (scan.js, server.js, public/_core.js, public/index.html, config/departments.json, config/workspace.json), `~/agentic-os/` (os-config.json, dashboard.html, server.js), `~/.claude/projects/-Users-elihuvillaraus/memory/feedback_spanish_register.md`, `~/.claude/projects/-Users-elihuvillaraus/memory/MEMORY.md`.
- Related tasks: none (TaskList unused this session).
