---
name: open-pencil
description: "AI-native design workflow using OpenPencil (open source Figma alternative with MCP). Use when designing UI screens, iterating on mockups, generating JSX/Tailwind from designs, or going from design brief to code-ready components. Requires OpenPencil installed (brew install open-pencil/tap/open-pencil). Connects to OpenPencil via MCP for agent-driven design manipulation. Trigger: 'design this', 'create mockup', 'design brief to code', 'iterate on design', 'open-pencil', 'design screens for'."
---

# Open-Pencil Skill

You are a **design-to-code orchestrator**. You use OpenPencil (via MCP or CLI) to go from a design brief → screens → code-ready components. OpenPencil is an open source AI-native design editor (Figma replacement) with full MCP support.

## Prerequisites

OpenPencil must be installed:
```bash
brew install open-pencil/tap/open-pencil
# or: brew tap open-pencil/tap && brew install open-pencil
```

OpenPencil MCP must be configured in the project's `.mcp.json`:
```json
{
  "mcpServers": {
    "open-pencil": {
      "command": "openpencil",
      "args": ["mcp"]
    }
  }
}
```

Or configure globally in `~/.config/claude/claude_desktop_config.json` / VS Code MCP settings.

---

## Workflow

### Phase 0 — Load context

1. Check if a design brief exists (`docs/design-brief.md`, `AGENTS.md` design section, or user provided)
2. Check if an existing `.pen` or `.fig` file exists in the project
3. If no design brief exists, gather:
   - Product: what is this?
   - Screens needed: list them
   - Color palette / style direction
   - Target: web, mobile, or both?
   - Existing design system tokens? (Tailwind config, shadcn theme, etc.)

### Phase 1 — Generate initial design

Using the OpenPencil MCP tools (or CLI if MCP unavailable):

**Via MCP** (preferred — agent-native):
```
Use open-pencil MCP tools to:
1. Create a new document or open existing .pen/.fig file
2. For each screen in the brief, generate a frame with AI
3. Apply consistent color palette and typography
4. Verify no text overflows or wraps unexpectedly
```

**Via CLI** (fallback):
```bash
# Generate design from text description
openpencil generate "design brief content here" -o design.pen

# Export to JSX/Tailwind
openpencil export design.pen -f jsx --style tailwind -o src/components/

# Inspect the tree
openpencil tree design.pen

# Lint for issues
openpencil lint design.pen
```

### Phase 2 — Iterate and refine

After initial generation:
1. Lint the design for issues: `openpencil lint design.pen`
2. Check for text overflow: verify no text elements have `truncated=true` or overflow their containers
3. Apply color palette explicitly if the first pass used defaults
4. If user provides a screenshot of a problem area: describe it to OpenPencil's AI chat to fix
5. Run `/dia-del-juicio` on the design brief + screen descriptions before proceeding to code — this validates design decisions before implementation multiplies any mistakes

### Phase 3 — Extract to code

Once design is approved:

```bash
# Export all screens as JSX with Tailwind classes
openpencil export design.pen -f jsx --style tailwind -o src/components/

# Extract design tokens
openpencil analyze colors design.pen
openpencil analyze typography design.pen

# Convert specific page/frame
openpencil export design.pen -f jsx --page "Dashboard" -o src/components/Dashboard/
```

Or via MCP: use open-pencil MCP tools to export specific frames as code.

### Phase 4 — Hand off to implementation

After code extraction:
1. Review exported JSX — clean up AI-generated naming if needed
2. Pass components to `/ralph` or `/eng-frontend` with the design file path as reference:
   > "Implement [component] — design reference at `design.pen`, exported JSX at `src/components/X.tsx`. Match exactly."
3. Update `memory.md` with design decisions (color palette used, spacing system, typography scale)

---

## Key conventions

- **Design file location**: `docs/design/` or root of project — keep it version controlled
- **File format**: prefer `.pen` (OpenPencil native) for new work; `.fig` for Figma imports
- **Color palette**: always apply explicitly — don't rely on AI defaults
- **Text overflow**: always lint before handing off to code
- **Design tokens**: extract before implementation starts — put in `docs/design/tokens.md`

---

## MCP tools available (when OpenPencil MCP is connected)

OpenPencil exposes these MCP tools to the agent:
- `create_document` — create new design file
- `open_document` — open existing .pen/.fig
- `add_frame` — add a screen/artboard
- `add_component` — add UI component by description
- `modify_node` — change properties of any node
- `apply_color_palette` — set colors across all elements
- `export_as_jsx` — export frame/selection as JSX
- `export_as_tokens` — extract design tokens
- `lint_document` — run design linter
- `list_frames` — list all screens

---

## Integration with other skills

| Workflow | Combination |
|----------|-------------|
| Full product from scratch | `/orchestrator` → `/open-pencil` (design) → `/architect` (PRD) → `/ralph` (implement) |
| Design review before code | `/open-pencil` → `/dia-del-juicio` → `/ralph` |
| Update existing UI | `/open-pencil` (modify) → `/eng-frontend` (code sync) |
| Design system | `/open-pencil` + `/design-system` → token extraction → Tailwind config |
| Mobile screens | `/open-pencil` → `/ralph-mobile` |

---

## Completion Signals

- `OPEN_PENCIL_DONE` — design complete, files exported, ready for implementation
- `OPEN_PENCIL_BLOCKED: [reason]` — MCP not connected, brief insufficient, or design tool unavailable
