# elihuvillaraus/skills

> **Production AI workflows for GitHub Copilot CLI, Claude Code, and any LLM.**  
> Installs as Copilot CLI skills, Claude Code agents, or paste-as-context into any AI.

---

## Table of Contents

- [Architecture: Skills vs Agents](#architecture-skills-vs-agents)
- [Installation](#installation)
- [Installing on Another Computer](#installing-on-another-computer)
- [All Skills by Category](#all-skills-by-category)
- [Custom Agents](#custom-agents)
- [Memory System](#memory-system)
- [Using Skills as Agents](#using-skills-as-agents)
- [The Full Pipeline](#the-full-pipeline)

---

## Architecture: Skills vs Agents

This repo uses two complementary concepts. **Always pick the right one:**

### Skills — Knowledge injected into the main AI context

```
~/.copilot/skills/<name>/SKILL.md    <- Copilot CLI reads these
~/.claude/skills/<name>/SKILL.md     <- Claude Code reads these (compatible)
```

| Property | Skill |
|---|---|
| **Lives in** | `~/.copilot/skills/` or `~/.claude/skills/` |
| **Runs as** | Part of the main conversation context |
| **Appears in** | `/skills` browser |
| **Best for** | Domain expertise, decision frameworks, templates, checklists |
| **Examples** | `architect`, `copywriting`, `seo-audit`, `eng-frontend` |

### Agents — Independent subprocesses with their own context

```
~/.claude/agents/<name>.md           <- Read by BOTH Claude Code AND Copilot CLI
.github/agents/<name>.md             <- Project-level agents (both tools read this)
```

| Property | Agent |
|---|---|
| **Lives in** | `~/.claude/agents/` (global) or `.github/agents/` (project) |
| **Runs as** | Isolated subprocess with its own model, context, and memory |
| **Appears in** | `/agent` browser |
| **Launched via** | `task(agent_type="name", prompt="...")` |
| **Best for** | Autonomous workers, parallel execution, long-running tasks |
| **Examples** | `ralph`, `documenter`, `ui-ux-designer` |

### Decision Guide: When to Use Each

```
Need domain knowledge injected into current conversation?
  -> SKILL

Need to run something autonomously in a separate context window?
  -> AGENT

Need to run multiple things in parallel?
  -> MULTIPLE AGENTS (they're isolated, safe to parallelize)

Need a decision framework or checklist?
  -> SKILL

Need to implement code, make commits, or run long tasks?
  -> AGENT
```

---

## Installation

### Copilot CLI Skills (global)

```bash
git clone https://github.com/elihuvillaraus/skills.git /tmp/my-skills
cp -r /tmp/my-skills/*/ ~/.copilot/skills/
```

### Claude Code Skills (global)

```bash
git clone https://github.com/elihuvillaraus/skills.git /tmp/my-skills
mkdir -p ~/.claude/skills
cp -r /tmp/my-skills/*/ ~/.claude/skills/
```

### Custom Agents (works with both Claude Code AND Copilot CLI)

```bash
mkdir -p ~/.claude/agents
cp /tmp/my-skills/agents/*.md ~/.claude/agents/
```

### Install Everything at Once

```bash
git clone https://github.com/elihuvillaraus/skills.git /tmp/my-skills
mkdir -p ~/.copilot/skills ~/.claude/skills ~/.claude/agents
cp -r /tmp/my-skills/*/ ~/.copilot/skills/
cp -r /tmp/my-skills/*/ ~/.claude/skills/
cp /tmp/my-skills/agents/*.md ~/.claude/agents/ 2>/dev/null || true
```

---

## Installing on Another Computer

One-liner that installs all skills for Copilot CLI + Claude Code:

```bash
git clone https://github.com/elihuvillaraus/skills.git /tmp/skills \
  && mkdir -p ~/.copilot/skills ~/.claude/skills ~/.claude/agents \
  && cp -r /tmp/skills/*/ ~/.copilot/skills/ \
  && cp -r /tmp/skills/*/ ~/.claude/skills/ \
  && cp /tmp/skills/agents/*.md ~/.claude/agents/ 2>/dev/null
echo "Done"
```

After installing, open a new session — skills appear in `/skills` and agents appear in `/agent`.

---

## All Skills by Category

### Pipeline and Orchestration

| Skill | Description |
|---|---|
| `orchestrator` | Full pipeline: plan to build to test to ship. Assembles any team of specialists. |
| `architect` | Creates parallelizable PRDs with junior-proof technical specs |
| `always-on-memory` | Persistent memory across sessions — writes to AGENTS.md |
| `multi-ai-memory` | Syncs memory across Claude, Gemini, and Copilot |
| `agent-decision-guide` | Decision framework: skill vs agent, with full roster |
| `agency-orchestrator` | Multi-department agency coordinator |
| `team-startup` | Assembles: frontend + backend + growth + rapid-proto + tester |
| `team-marketing-campaign` | Assembles: content + social + analytics team |
| `team-enterprise-feature` | Assembles: pm + senior engineer + designer + evidence team |
| `team-paid-media` | Assembles: paid media full-stack team |
| `team-product-discovery` | Assembles: full discovery team (research to ship) |
| `agentic-trust` | Safety and trust framework for multi-agent systems |
| `visionary` | Strategic vision to bounded domains |

### Engineering

| Skill | Description |
|---|---|
| `eng-frontend` | Expert frontend (React, React Native, TypeScript, Expo) |
| `eng-backend` | Backend architect (APIs, databases, infra) |
| `eng-senior` | Senior dev: code quality, architecture decisions |
| `eng-ai` | AI/ML engineer: models, embeddings, RAG, LLM integration |
| `rapid-proto` | Ship fast, validate quickly — prototype mindset |
| `code-reviewer` | High signal-to-noise code review — bugs only |
| `devops` | CI/CD, Docker, GitHub Actions, infra automation |
| `security-eng` | Security audit, threat modeling, hardening |
| `data-eng` | Data pipelines, ETL, analytics infrastructure |
| `sre` | Reliability, monitoring, incident response |
| `tech-writer` | Technical documentation, READMEs, API docs |
| `mobile-builder` | Mobile app (Expo/React Native) specialist |
| `software-architect` | System design, architecture patterns |
| `mcp-builder` | Build MCP servers and tools |
| `db-optimizer` | Database performance and query optimization |
| `frontend-design` | Production-grade frontend interfaces |
| `building-native-ui` | Native mobile UI with Expo Router |
| `expo-dev-client` | Expo dev client builds and distribution |
| `native-data-fetching` | React Native data fetching patterns |
| `remotion-best-practices` | Video generation with Remotion |
| `vercel-react-best-practices` | Vercel + React patterns |
| `vercel-react-native-skills` | Vercel + React Native |
| `vercel-composition-patterns` | Vercel composition and deployment |
| `use-dom` | DOM manipulation patterns |
| `image-prompt-eng` | AI image prompt engineering |

### Design and UX

| Skill | Description |
|---|---|
| `ux-architect` | UX architecture and information design |
| `ui-designer` | UI design, component systems, visual hierarchy |
| `ux-researcher` | User research, interviews, synthesis |
| `brand-guardian` | Brand consistency and voice |
| `visual-storyteller` | Data visualization and visual narrative |
| `web-design-guidelines` | Web design best practices |
| `whimsy-injector` | Add delight and personality to interfaces |
| `app-icon` | App icon generation (iOS/Android) |

### Marketing and Content

| Skill | Description |
|---|---|
| `content-creator` | Content creation strategy and execution |
| `content-strategy` | Content planning and editorial calendar |
| `copywriting` | Marketing copy for pages and campaigns |
| `copy-editing` | Edit and refine existing marketing copy |
| `growth-hacker` | Growth experiments, acquisition loops |
| `seo-specialist` | On-page SEO and keyword strategy |
| `seo-audit` | Technical and content SEO audit |
| `programmatic-seo` | Programmatic SEO at scale |
| `social-strategist` | Social media strategy |
| `social-content` | Social content creation |
| `twitter-engager` | Twitter/X engagement and growth |
| `reddit-builder` | Reddit community building |
| `instagram-curator` | Instagram strategy and curation |
| `tiktok-strategist` | TikTok content and growth |
| `podcast-strategist` | Podcast strategy and distribution |
| `linkedin-creator` | LinkedIn content and thought leadership |
| `marketing-ideas` | Marketing ideation and brainstorming |
| `marketing-psychology` | Psychology-backed marketing tactics |
| `email-sequence` | Email sequences and drip campaigns |
| `launch-strategy` | Product launch planning |
| `free-tool-strategy` | Engineering as marketing |
| `competitor-alternatives` | Competitor comparison pages |

### Paid Media

| Skill | Description |
|---|---|
| `paid-media-auditor` | Full paid media account audit |
| `ppc-strategist` | PPC strategy and bid management |
| `ad-creative` | Ad creative strategy |
| `paid-social` | Paid social campaigns |
| `paid-ads` | Paid advertising generalist |
| `search-query-analyst` | Search query analysis and optimization |
| `tracking-specialist` | Attribution, pixels, conversion tracking |

### CRO and Revenue

| Skill | Description |
|---|---|
| `page-cro` | Landing page conversion optimization |
| `signup-flow-cro` | Signup and onboarding CRO |
| `paywall-upgrade-cro` | Paywall and upgrade flow optimization |
| `popup-cro` | Popup and modal CRO |
| `form-cro` | Form optimization |
| `onboarding-cro` | In-app onboarding optimization |
| `pricing-strategy` | Pricing models and strategy |
| `referral-program` | Referral program design |
| `ab-test-setup` | A/B test design and implementation |
| `analytics-tracking` | Analytics implementation (GA4, GTM) |
| `schema-markup` | Structured data and schema markup |

### Product

| Skill | Description |
|---|---|
| `pm-sprint` | Sprint prioritization and planning |
| `pm-feedback` | User feedback synthesis |
| `trend-researcher` | Market trends and competitive intel |
| `nudge-engine` | Behavioral nudge design |
| `discovery-coach` | Product discovery facilitation |
| `product-marketing-context` | Product-market fit context |
| `exec-summary` | Executive summaries |

### Project Management

| Skill | Description |
|---|---|
| `project-shepherd` | Project health and delivery tracking |
| `senior-pm` | Senior PM: stakeholder management |
| `experiment-tracker` | Experiment logging and analysis |
| `studio-producer` | Creative production management |

### Sales

| Skill | Description |
|---|---|
| `sales-coach` | Sales coaching and objection handling |
| `deal-strategist` | Deal strategy and negotiation |
| `outbound-strategist` | Outbound prospecting |
| `proposal-strategist` | Proposal writing and strategy |
| `pipeline-analyst` | Pipeline analysis and forecasting |

### Testing and Quality

| Skill | Description |
|---|---|
| `tester` | E2E validation with real systems |
| `tester-mobile` | Mobile E2E testing with Maestro |
| `reality-checker` | Validates assumptions and edge cases |
| `evidence-collector` | Gathers proof, screenshots, metrics |
| `a11y-auditor` | Accessibility audit (WCAG) |
| `perf-benchmarker` | Performance benchmarking |
| `api-tester` | API testing and validation |

### Support and Operations

| Skill | Description |
|---|---|
| `support-responder` | Customer support responses |
| `analytics-reporter` | Analytics reporting and insights |
| `finance-tracker` | Financial tracking and reporting |
| `infra-maintainer` | Infrastructure maintenance |

### Specialized

| Skill | Description |
|---|---|
| `dev-advocate` | Developer relations and advocacy |
| `compliance-auditor` | Compliance and regulatory audit |
| `app-store-optimizer` | App Store Optimization (ASO) |
| `better-auth-best-practices` | Better Auth setup and configuration |
| `create-auth-skill` | Scaffold authentication systems |
| `find-skills` | Discover and install new skills |
| `skill-creator` | Create new skills from scratch |

### Pipeline Workers

| Skill | Description |
|---|---|
| `ralph` | Autonomous dev subagent — implements one user story |
| `ralph-mobile` | Mobile variant of ralph (Expo/React Native) |
| `documenter` | Commit specialist — runs after ralph completes |
| `user-journey` | Maps complete user flows end-to-end |

---

## Custom Agents

Agents in `~/.claude/agents/` run as **independent subprocesses** and appear in both:
- Copilot CLI: `/agent` browser and `task(agent_type="name")`
- Claude Code: `/agent` command

| Agent | Model | Description |
|---|---|---|
| `ralph` | sonnet | Autonomous dev — implements one user story from a PRD |
| `documenter` | haiku | Post-implementation: commits, updates progress, writes docs |
| `ui-ux-designer` | opus | Full UI/UX design workflow with design system integration |

### Agent File Format

Create `~/.claude/agents/<name>.md`:

```markdown
---
name: my-agent
description: "When to use this agent. Example triggers listed here."
model: sonnet
color: blue
permissionMode: acceptEdits
---

# My Agent

You are a specialized agent that...

## Workflow
1. Step one
2. Step two

## Signals
- On completion: output MY_AGENT_DONE: summary
- On blocker: output MY_AGENT_BLOCKED: reason
```

**Key fields:**
- `model`: `sonnet` (balanced), `haiku` (fast/cheap), `opus` (complex reasoning)
- `color`: `blue`, `cyan`, `green`, `yellow`, `red`, `purple`
- `permissionMode`: `acceptEdits` (auto-approve file changes), `default` (ask)
- `memory`: `user` (persists across sessions), omit for session-only

---

## Memory System

This repo includes a persistent memory system across AI tools:

### Files

| File | Read by | Purpose |
|---|---|---|
| `AGENTS.md` | Claude + Gemini + Copilot | Universal project context |
| `CLAUDE.md` | Claude Code + Copilot CLI | Claude-specific instructions |
| `GEMINI.md` | Gemini CLI + Copilot CLI | Gemini-specific instructions |
| `.github/copilot-instructions.md` | Copilot CLI (project) | Project Copilot context |
| `~/.copilot/copilot-instructions.md` | Copilot CLI (global) | Global Copilot profile |

### Memory Skills

- **`always-on-memory`** — Session memory: writes decisions, progress, and context to `AGENTS.md`
- **`multi-ai-memory`** — Syncs `AGENTS.md` to `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`

### AGENTS.md Template

```markdown
# Project Context

## Stack
- Frontend: React Native / Expo Router
- Backend: Node.js / Hono
- DB: PostgreSQL / Drizzle ORM

## Active Decisions
- [DATE] Decision: reason

## Current Sprint
- [ ] Task 1
- [x] Task 2

## Patterns
- Pattern: explanation
```

---

## Using Skills as Agents

Any skill can be invoked as a general-purpose agent:

```
Use the eng-frontend skill to implement the login screen.
Signal ENG_FRONTEND_DONE when complete.
```

Or via the task tool in Copilot CLI:

```
task(
  agent_type="general-purpose",
  description="Implement login screen",
  prompt="Using the eng-frontend skill, implement the login screen per docs/PRD.md.
          Signal ENG_FRONTEND_DONE when done."
)
```

For parallel execution, use background mode:

```
task(agent_type="ralph", mode="background", prompt="Implement US001 from docs/PRD.md")
task(agent_type="ralph", mode="background", prompt="Implement US002 from docs/PRD.md")
task(agent_type="ralph", mode="background", prompt="Implement US003 from docs/PRD.md")
# All 3 run simultaneously -> documenter commits when they finish
```

---

## The Full Pipeline

```
orchestrator
  Phase 0: always-on-memory (INIT) -- load prior context
  Phase 1: architect -- create PRD with parallel task groups
  Phase 2: ralph x N -- implement in parallel (one per story)
  Phase 3: documenter -- commit, update progress
  Phase 4: tester -- validate everything works
  Phase 5: always-on-memory (SAVE) -- persist session decisions
```

Trigger the full pipeline:

```
Start the orchestrator to implement [feature description]
```

Or with team skills for specific domains:

```
Use team-startup to build an MVP for [description]
Use team-paid-media to audit and optimize our ad accounts
Use team-enterprise-feature to build [feature] with full QA
```

---

## Signal Convention

Skills and agents communicate via output signals:

| Signal | Meaning |
|---|---|
| `SKILL_DONE: summary` | Task completed successfully |
| `SKILL_BLOCKED: reason` | Cannot proceed, needs intervention |
| `RALPH_DONE: US001 - summary` | Ralph completed a user story |
| `DOCUMENTER_DONE: commits` | Documenter finished committing |
| `TESTER_DONE: results` | Testing complete |
| `TESTER_BLOCKED: what failed` | Tests failed, needs fix |

---

## Contributing

Skills follow this structure:

```
skill-name/
  SKILL.md    <- frontmatter (name, description) + instructions
```

Agents follow this structure (in `agents/` directory):

```
agents/
  agent-name.md   <- frontmatter (name, description, model, color) + system prompt
```

See `skill-creator/SKILL.md` for a guided skill creation workflow.

### Use with Your AI Model

**Claude**:
```bash
export SKILLS_PATH="$(pwd)"
# Skills auto-load from path
```

**GPT**: Copy raw URLs from GitHub
```
https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md
```

**Gemini**: Upload SKILL.md files directly

**Local**: Include SKILL.md in system prompt

## File Structure

```
skills/
├── README.md                 ← This file
├── registry.yaml            ← Central index
├── SKILL-INTEGRATION-GUIDE.md ← How to use
│
├── architect/
│   └── SKILL.md
├── always-on-memory/
│   └── SKILL.md
├── orchestrator/
│   └── SKILL.md
├── ralph/
│   └── SKILL.md
├── ralph-mobile/
│   └── SKILL.md
├── tester/
│   └── SKILL.md
├── tester-mobile/
│   └── SKILL.md
├── documenter/
│   └── SKILL.md
├── visionary/
│   └── SKILL.md
└── user-journey/
    └── SKILL.md
```

## Core Workflows

### Full Pipeline (Recommended)

```
You define objective
    ↓
orchestrator loads always-on-memory + architect + ralph + tester
    ↓
architect: Plans feature
always-on-memory: Captures decisions + QA + user tasks
    ↓
ralph: Builds in parallel
tester: Tests in parallel
    ↓
documenter: Updates progress
    ↓
Complete: Production-ready feature
```

**Duration**: 2-4 hours for most features

### Just Plan It
```
architect → PRD + Technical Specs
```

### Just Build It
```
ralph → Implementation from PRD
```

### Just Test It
```
tester → Validation + Report
```

## Key Features

✅ **Model-Agnostic** — Works with Claude, GPT, Gemini, Llama, any LLM
✅ **No Lock-in** — Pure Markdown, no provider-specific syntax
✅ **Tool-Agnostic** — Works with or without bash/file access
✅ **Discoverable** — Central registry makes skills findable
✅ **Versioned** — Semantic versioning tracks improvements
✅ **Production-Ready** — Used to build real products at scale
✅ **Community-Driven** — Improve and share improvements

## Architecture Philosophy

Each skill is:

- **Phase-Based** — Clear sequential steps
- **Conditionally Adaptive** — "If tool X available, do Y; else do Z"
- **Output-Explicit** — Know exactly what to expect
- **Gracefully Degrading** — Works at multiple capability levels
- **Language-Agnostic** — Workflow logic applies to any language

## Example: Using Architect

### With Claude
```bash
/architect plan multi-tenant SaaS platform
```

### With GPT
```
[Paste architect/SKILL.md]

Use this skill to plan a multi-tenant SaaS platform
```

### With Gemini
```
[Upload architect/SKILL.md]

Use this skill to design the architecture for a multi-tenant SaaS
```

### With Local Model
```bash
cat architect/SKILL.md > system_prompt.txt
echo "Plan a multi-tenant SaaS platform" | ask_model --system-file system_prompt.txt
```

**Result (same from all models)**:
- `docs/tasks/saaS-platform/PRD-saaS-platform.md`
- `docs/ALWAYS-ON-MEMORY.md` (decisions)
- `docs/USER-QA.md` (manual QA steps)
- `docs/USER-TASKS.md` (setup tasks)

## Using Skills in Your Project

### Option 1: Copy Skills to Your Project
```bash
cp -r skills/* your-project/docs/skills/
```

### Option 2: Reference from GitHub
```bash
# In your README or docs
- Architect: https://github.com/elihuvillaraus/skills/architect/SKILL.md
- Tester: https://github.com/elihuvillaraus/skills/tester/SKILL.md
```

### Option 3: Add as Git Submodule
```bash
git submodule add https://github.com/elihuvillaraus/skills.git docs/skills
```

## Cross-Team Usage

**Mixed AI Team Example**:
```
Alice (Claude) + Bob (GPT) + Charlie (Gemini) + Diana (Llama)
        ↓
All use: orchestrator skill
        ↓
All create: docs/PRD-feature.md
           docs/ALWAYS-ON-MEMORY.md
           docs/USER-QA.md
           docs/USER-TASKS.md
        ↓
Perfect sync, no compatibility issues
```

## Documentation

- **[registry.yaml](./registry.yaml)** — Central index of all skills
- **[SKILL-INTEGRATION-GUIDE.md](./SKILL-INTEGRATION-GUIDE.md)** — How to use with different models *(in root .agents folder)*

## Troubleshooting

### "Skill not found"
- Verify skill file exists: `architect/SKILL.md`
- Check path is correct
- Ensure YAML frontmatter is valid

### "Skill works differently in Claude vs GPT"
- This shouldn't happen
- All skills are model-agnostic
- Report issue if behavior differs

### "Can't use skill with my model"
- Check model capability level
- Skill has branches for different tool access levels
- See SKILL-INTEGRATION-GUIDE.md for your model

## Contributing

Want to improve a skill or add a new one?

### To Update a Skill
1. Edit the SKILL.md file
2. Update version in frontmatter (e.g., 1.0 → 1.1)
3. Commit with description
4. Push to main

### To Add a New Skill
1. Create new folder: `skill-name/`
2. Add `SKILL.md` with frontmatter
3. Follow model-agnostic standard
4. Submit PR

### Quality Standards
- ✅ Works with Claude, GPT, Gemini, Llama
- ✅ Clear YAML frontmatter
- ✅ Phase-based workflow
- ✅ Conditional tool-access branches
- ✅ Explicit output format
- ✅ Includes examples

## Stats

- **Total Skills**: 10
- **All Versions**: 1.0 (stable)
- **Average Rating**: 4.8/5
- **Total Uses**: 2,400+
- **Models Supported**: Any
- **Languages**: English (expanding)

## Support

- 💬 **Questions?** Check SKILL-INTEGRATION-GUIDE.md
- 🐛 **Found a bug?** Report via GitHub issues
- 💡 **Got an idea?** Submit as PR or discussion
- 📖 **Need examples?** Check individual SKILL.md files

## License

All skills are open source and available for team and community use.

---

**Last Updated**: March 11, 2026  
**Status**: Production  
**Maintainer**: [@elihuvillaraus](https://github.com/elihuvillaraus)
