---
name: skill-tracking
description: "Track which skills are actually being used across projects. Reads ~/.agents/skill-usage.log, aggregates usage stats, identifies unused skills, and surfaces optimization opportunities. Also enforces the logging convention. Trigger: 'which skills am I using', 'skill usage stats', 'what skills are active', 'skill analytics', 'prune unused skills'."
---

# Skill Tracking

Track which skills are being invoked, which are dead weight, and what patterns emerge.

## The Convention

Every agent that invokes a skill MUST log it. Add this to your `AGENTS.md` or `memory.md`:

```
## Skill Logging Convention
When invoking any skill (including this one), append one line to ~/.agents/skill-usage.log:
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|SKILL_NAME|PROJECT_NAME|REASON" >> ~/.agents/skill-usage.log

Example:
  echo "2026-07-03T15:30:00Z|architect|pitonisa|planning apollo v3 feature" >> ~/.agents/skill-usage.log
```

This convention must be included in `AGENTS.md` so all agents see it.

---

## Usage Analysis

When invoked, run these analyses:

### 1 — Read the log

```bash
# Show all entries
cat ~/.agents/skill-usage.log 2>/dev/null | head -100

# Count by skill (last 30 days)
cat ~/.agents/skill-usage.log 2>/dev/null | \
  awk -F'|' '{print $2}' | sort | uniq -c | sort -rn | head -20

# Count by project
cat ~/.agents/skill-usage.log 2>/dev/null | \
  awk -F'|' '{print $3}' | sort | uniq -c | sort -rn | head -10

# Usage by date (last 14 days)
cat ~/.agents/skill-usage.log 2>/dev/null | \
  awk -F'|' '{print substr($1,1,10)}' | sort | uniq -c | tail -14
```

### 2 — Find unused skills

```bash
# List all skills
ALL_SKILLS=$(ls ~/.agents/skills/ | grep -v SKILL-STANDARD | sort)

# List used skills (from log)
USED_SKILLS=$(cat ~/.agents/skill-usage.log 2>/dev/null | awk -F'|' '{print $2}' | sort -u)

# Find unused (skills that never appear in log)
comm -23 <(echo "$ALL_SKILLS") <(echo "$USED_SKILLS") | head -50
```

### 3 — Find stale skills (not used in 30+ days)

```bash
THIRTY_DAYS_AGO=$(date -u -v-30d +%Y-%m-%d 2>/dev/null || date -u -d '30 days ago' +%Y-%m-%d)
cat ~/.agents/skill-usage.log 2>/dev/null | \
  awk -F'|' -v cutoff="$THIRTY_DAYS_AGO" '$1 >= cutoff {print $2}' | sort -u
```

### 4 — Output report

```markdown
# Skill Usage Report — [date]

## Most Used (last 30 days)
| Skill | Uses | Projects |
|-------|------|---------|
| orchestrator | 12 | pitonisa, zeus, horus |
| architect | 10 | pitonisa, zeus |
...

## Never Used (candidates for archiving)
[list of skills with 0 log entries]

## Last Seen > 30 Days Ago (consider pruning)
[list]

## Top Projects by Skill Activity
[list]

## Recommendations
- Archive: [skills with 0 uses and no recent modification]
- Keep: [top 20 by usage]
- Review: [skills modified but never used]
```

---

## Bootstrapping the log

If `~/.agents/skill-usage.log` does not exist, create it and note that historical data is unavailable. Going forward, all skill invocations will be logged.

```bash
touch ~/.agents/skill-usage.log
echo "# skill-usage.log — format: ISO8601|skill_name|project|reason" > ~/.agents/skill-usage.log
```

---

## Adding the convention to AGENTS.md

When run in a project, append the logging convention to the project's `AGENTS.md`:

```bash
cat >> AGENTS.md << 'EOF'

## Skill Logging (required)
When invoking any skill, log it:
```bash
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)|SKILL_NAME|$(basename $PWD)|REASON" >> ~/.agents/skill-usage.log
```
EOF
```

---

## Completion Signal

- `SKILL_TRACKING_DONE` — report generated
- Log bootstrapped if it didn't exist
- Convention added to `AGENTS.md` if not already present
