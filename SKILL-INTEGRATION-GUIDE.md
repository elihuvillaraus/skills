# Skill Integration Guide

How to use elihuvillaraus/skills with any AI model.

## Quick Links

- **Repository**: https://github.com/elihuvillaraus/skills
- **Registry**: [registry.yaml](./registry.yaml)
- **Format Spec**: See model-agnostic standard below

## Using Skills by Platform

### Claude / OpenCode

Skills auto-load from `~/.agents/skills/`

```bash
# Add skills to your local path
mkdir -p ~/.agents/skills
cd ~/.agents/skills
git clone https://github.com/elihuvillaraus/skills.git .

# Use directly
skill load architect
/orchestrator go
/tester run tests
```

**Advantage**: Auto-loads, no copying needed

### ChatGPT / OpenAI

1. Get the raw skill URL:
```
https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md
```

2. Paste into your chat:
```
Use this skill:
[PASTE CONTENT]

Now, plan this feature: [your feature]
```

Or reference via URL:
```
I want you to use this skill: https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md

Now plan this feature...
```

**Advantage**: Works in web chat, simple copy/paste

### Google Gemini

1. Download skill file locally
2. Upload in Gemini interface

Or use API:
```python
import anthropic

with open('skills/architect/SKILL.md', 'r') as f:
    skill_content = f.read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="gemini-2.0-flash",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": skill_content},
            {"type": "text", "text": "Use this skill to plan a feature"}
        ]
    }]
)
```

**Advantage**: Can upload files directly

### Local Models (Llama, Mistral, etc.)

Include skill in system prompt:

```bash
# Option 1: Via ollama
SKILL=$(cat architect/SKILL.md)
ollama run mistral "
$SKILL

Now plan this feature: [your feature]
"

# Option 2: Via Python
import ollama

with open('architect/SKILL.md', 'r') as f:
    skill = f.read()

response = ollama.generate(
    model='mistral',
    prompt='Plan a feature',
    system=skill
)
```

**Advantage**: Full control, works offline

### API Usage (Any Platform)

Include skill in request:

```bash
curl https://api.openai.com/v1/messages \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "system": "SKILL CONTENT HERE",
    "messages": [
      {"role": "user", "content": "Use this skill to plan a feature"}
    ]
  }'
```

**Advantage**: Works with any API provider

## Skill Format (Model-Agnostic)

All skills follow this structure:

### 1. YAML Frontmatter
```yaml
---
name: architect
type: workflow
version: 1.0
models: ["any"]
languages: ["en"]
tags: ["architecture", "planning"]
depends_on: []
complexity: advanced
estimated_time_minutes: 60
input_requirements: []
output_artifacts: []
success_criteria: []
---
```

**Key**: `models: ["any"]` means it works with every LLM

### 2. Clear Phases

```markdown
## Phase 1 — Understand
[What happens in this phase]

### Step 1a: Action
- **Input**: What you start with
- **Output**: What you get
```

### 3. Conditional Branches

Skills gracefully adapt to tool access:

```markdown
### Phase 2 — Analyze

**If you can run bash**:
```bash
grep -r "pattern" src/
```

**If you can't run bash**:
1. Ask user for: `find src -name "*.ts"`
2. Analyze output
3. Recommend changes
```

### 4. Explicit Output

```markdown
## Output Format

Return this JSON:
{
  "status": "success",
  "prd": "docs/tasks/feature/PRD.md",
  "decisions": [...]
}
```

This ensures:
- ✅ All models return consistent format
- ✅ Results can be parsed/automated
- ✅ No surprise outputs

## Model Capability Levels

Not all models have the same tools. Skills adapt:

| Model | Level | Can Do |
|-------|-------|--------|
| Claude | 3 | Bash + Files + APIs |
| GPT-4 | 2 | Bash via output + APIs |
| Gemini | 2 | APIs + Web search |
| Llama | 1 | Text only |

Each skill works at all levels.

## Using Skills Across Teams

### Scenario: Distributed Team

```
Alice (Claude on Mac)
Bob (ChatGPT web)
Charlie (Gemini iOS)
Diana (Llama on Linux)
    ↓
All load: orchestrator skill
    ↓
All execute same workflow
    ↓
All create identical artifacts
    ↓
Perfect collaboration
```

### How It Works

1. **Same skill file** used by everyone
2. **Conditionally adapts** to each model's capabilities
3. **Same output format** from all models
4. **Perfect sync** across team

## Sharing Skills

### Option 1: GitHub URL
```
"Use this skill: https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md"
```

**Best for**: Cross-team sharing, always up-to-date

### Option 2: Copy/Paste
```
[Copy architect/SKILL.md content]
[Paste into chat]
```

**Best for**: Quick one-off usage

### Option 3: Git Submodule
```bash
git submodule add https://github.com/elihuvillaraus/skills.git docs/skills
```

**Best for**: Projects that depend on skills

### Option 4: Local Clone
```bash
git clone https://github.com/elihuvillaraus/skills.git ~/.agents/skills
```

**Best for**: Claude/OpenCode users

## Troubleshooting

### "Model doesn't understand the skill"

→ Your model may not have enough instruction-following capability

**Solution**: Use simpler skills or break into smaller steps

### "Different output from different models"

→ Shouldn't happen if skill is truly model-agnostic

**Solution**: Check that skill follows conditional branching pattern

### "Skill doesn't have tool access I need"

→ Skill has branches for different capabilities

**Solution**: Check the skill for "If you can X" sections

### "Can't find raw URL for GitHub"

→ Navigate to file in GitHub, click "Raw" button

```
GitHub web: https://github.com/elihuvillaraus/skills/blob/main/architect/SKILL.md
Raw URL: https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md
```

## Best Practices

### 1. Always Check Skill Version
```yaml
version: 1.0  ← Use latest version
```

### 2. Use Raw GitHub URLs for Sharing
```
✅ https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md
❌ https://github.com/elihuvillaraus/skills/blob/main/architect/SKILL.md
```

### 3. Test with Multiple Models
Before using a skill in production:
- ✅ Test with Claude
- ✅ Test with GPT
- ✅ Test with Gemini
- ✅ Test with local model

### 4. Explicit About Model Capability
Instead of:
> "Run this test"

Better:
> "If you can execute bash, run this test. If not, provide these steps for manual execution"

### 5. Share the Registry
When sharing skills with team:
```
Here's the skills repository: https://github.com/elihuvillaraus/skills
See registry.yaml for all available skills
```

## FAQ

**Q: Do I need to install anything?**
A: No. Skills are pure Markdown. Copy/paste or use URL.

**Q: Can I modify a skill?**
A: Yes! Create your own version or submit PR for improvements.

**Q: What if a skill breaks?**
A: All skills are version 1.0 (stable). Report issue on GitHub.

**Q: Can I combine multiple skills?**
A: Yes! Many skills have dependencies listed in frontmatter.

**Q: How often are skills updated?**
A: Check GitHub commits for update frequency.

**Q: Can I use these skills commercially?**
A: Yes, they're open source.

## Examples

### Using Architect Skill with Claude
```bash
skill load architect
/architect plan payment processing system
```

### Using Architect Skill with GPT
```
[Paste https://raw.githubusercontent.com/elihuvillaraus/skills/main/architect/SKILL.md]

Use this skill to plan a payment processing system
```

### Using Orchestrator with Gemini
```
[Upload orchestrator/SKILL.md]

I want to build a marketplace. Use this skill to run the full pipeline.
```

### Using with Local Model
```bash
cat orchestrator/SKILL.md >> system_prompt.txt
ollama run mistral --system "$(cat system_prompt.txt)" "Build a marketplace"
```

## Support

- 📖 **Docs**: See README.md
- 🐛 **Issues**: GitHub issues
- 💡 **Ideas**: GitHub discussions
- 📧 **Questions**: Open GitHub issue

---

**Last Updated**: March 11, 2026
