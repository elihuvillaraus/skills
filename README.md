# elihuvillaraus/skills

**Model-Agnostic Skills Repository** — Reusable AI workflows that work with any LLM platform.

🚀 **Works with**: Claude | GPT | Gemini | Llama | Any AI Model

## What's Inside

A collection of **production-grade skills** for building products end-to-end:

| Skill | Type | Purpose | Complexity |
|-------|------|---------|-----------|
| **architect** | workflow | Design parallelizable features with PRDs | Advanced |
| **orchestrator** | workflow | Run full pipeline: plan → build → test → ship | Advanced |
| **ralph** | workflow | Autonomous implementation of user stories | Advanced |
| **ralph-mobile** | workflow | Mobile implementation (Expo/React Native) | Advanced |
| **tester** | workflow | E2E validation with real systems | Advanced |
| **tester-mobile** | workflow | Mobile E2E testing with Maestro | Advanced |
| **documenter** | workflow | Update progress, commit, document | Moderate |
| **visionary** | workflow | Strategic vision → bounded domains | Advanced |
| **user-journey** | workflow | Map complete user flows end-to-end | Moderate |

## Quick Start

### For Claude/OpenCode Users
```bash
# Skills auto-load
skill load architect
/orchestrator go
/tester run tests
```

### For GPT Users
```
1. Copy raw skill: https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md
2. Paste into ChatGPT
3. Request: "Use this skill to plan a feature"
```

### For Gemini Users
```
1. Upload skill file
2. Ask: "Use this skill to plan a feature"
```

### For Local Model Users
```bash
cat architect/SKILL.md | include-in-prompt
# Then ask: "Use this skill to..."
```

## Installation

### Clone the Repository
```bash
git clone https://github.com/elihuvillaraus/skills.git
cd skills
```

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
├── SKILL-STANDARD.md        ← Format specification
├── SKILL-INTEGRATION-GUIDE.md ← How to use
│
├── architect/
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
orchestrator loads architect + ralph + tester
    ↓
architect: Plans feature (PRD + decisions)
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
- **[SKILL-STANDARD.md](./SKILL-STANDARD.md)** — Format & how to create skills *(in root .agents folder)*
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

- **Total Skills**: 9
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
