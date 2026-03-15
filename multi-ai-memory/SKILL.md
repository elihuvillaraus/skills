---
name: multi-ai-memory
description: "Manages a unified memory bank that works across ALL AI coding tools: Claude Code, Gemini CLI, GitHub Copilot CLI, and Cursor/Windsurf. Creates and synchronizes AGENTS.md (universal), CLAUDE.md, GEMINI.md, and .github/copilot-instructions.md. Inspired by centminmod/my-claude-code-setup memory bank approach, extended for multi-tool use. Trigger: 'sync ai memory', 'update all ai context', 'multi ai memory', 'cross tool memory', 'sync claude gemini copilot', 'memory bank sync'."
---

# Multi-AI Memory — Sincronización Universal entre Herramientas

Gestionas un sistema de memoria unificado que funciona con TODOS los AI tools.

## El problema que resuelves

```
Sin multi-ai-memory:
  - Abres Claude Code → no sabe nada del proyecto
  - Abres Gemini CLI → empieza desde cero
  - Abres Copilot CLI → no tiene contexto

Con multi-ai-memory:
  - AGENTS.md = fuente universal de verdad
  - Cada tool lee su archivo específico
  - Todos tienen el mismo contexto del proyecto
```

---

## Arquitectura del sistema

```
AGENTS.md (universal — TODOS leen)
    ↓ sincroniza a:
    ├── CLAUDE.md (Claude Code lee esto)
    ├── GEMINI.md (Gemini CLI lee esto)
    ├── .github/copilot-instructions.md (GitHub Copilot)
    └── .agent/ARCHITECTURE.md (Cursor/Windsurf vía antigravity-kit)
```

Copilot CLI además lee (en orden de prioridad):
1. `AGENTS.md` — instrucciones universales del proyecto
2. `CLAUDE.md` — instrucciones de Claude (también las lee Copilot)
3. `GEMINI.md` — instrucciones de Gemini (también las lee Copilot)
4. `.github/copilot-instructions.md` — Copilot específico
5. `~/.copilot/copilot-instructions.md` — global personal

---

## Comando: INIT (primer setup)

Al inicializar un proyecto nuevo con multi-ai-memory:

### 1. Crear AGENTS.md (universal)
```markdown
# [Project Name] — AI Memory Bank
> Universal instructions for Claude Code, Gemini CLI, and GitHub Copilot CLI

## Project Overview
**Name**: [name]
**Stack**: [stack]
**Purpose**: [purpose]
**Repo**: [URL]

## Active Context
**Phase**: [current phase]
**Last session**: [date — what was done]
**Next**: [what to do next]
**Blockers**: [none / description]

## Architecture Decisions
- [date] [decision] — Rationale: [why]

## Code Patterns & Conventions
<!-- Patterns ALL agents must follow in this project -->
- [pattern]

## Key Files Map
- `src/[path]` — [description]

## Do NOT
<!-- Things all AI must avoid in this project -->
- [constraint]

## Session History
<!-- Append after each session -->
- [date]: [summary of what was accomplished]
```

### 2. Crear CLAUDE.md (Claude Code específico)
```markdown
# CLAUDE.md

## AI Guidance
- Read AGENTS.md first for project context
- [Claude-specific tool preferences]
- [Claude-specific behavioral rules]

## Memory Bank Files
- AGENTS.md — universal project context (PRIMARY)
- CLAUDE-decisions.md — architecture decisions (if exists)
- CLAUDE-patterns.md — code patterns (if exists)
- CLAUDE-activeContext.md — current session state (if exists)

## Tool Preferences
- Use ripgrep (rg) over grep
- Use fd over find
- [other preferences]
```

### 3. Crear GEMINI.md (Gemini CLI específico)
```markdown
# GEMINI.md

## AI Guidance
- Read AGENTS.md first for project context
- Ignore CLAUDE.md and CLAUDE-*.md files
- Strict scope adherence: only do what's asked

## Memory Bank Files
- AGENTS.md — universal project context (PRIMARY)
- GEMINI-activeContext.md — current Gemini session (if exists)

## Core Principles
1. Strict Instructions: adhere exactly to user requests
2. Scope Limitation: don't expand beyond the request
3. Clarification Protocol: ask if ambiguous
```

### 4. Crear .github/copilot-instructions.md (Copilot específico)
```markdown
# Copilot Instructions
> Auto-synced from AGENTS.md by multi-ai-memory skill

## Project Context
[brief summary from AGENTS.md]

## Stack
[from AGENTS.md]

## Key Patterns
[from AGENTS.md patterns section]

## Current Focus
[from AGENTS.md activeContext]

## Skills Available
Use these installed skills for specialized tasks:
[relevant skill list for this project]
```

---

## Comando: SYNC (sincronizar desde AGENTS.md)

Cuando `AGENTS.md` se actualiza, propagar cambios:

```bash
# 1. Leer AGENTS.md actual
# 2. Extraer secciones relevantes
# 3. Actualizar cada archivo de destino
# 4. Reportar qué cambió
```

### Qué sincronizar a cada tool:

| Sección de AGENTS.md | CLAUDE.md | GEMINI.md | copilot-instructions.md |
|---|---|---|---|
| Project Overview | ✅ | ✅ | ✅ |
| Active Context | ✅ | ✅ | ✅ |
| Architecture Decisions | ✅ referencia | ❌ | ❌ |
| Code Patterns | ✅ | ✅ | ✅ |
| Key Files | ✅ | ✅ | ✅ |
| Do NOT | ✅ | ✅ | ✅ |
| Session History | ❌ | ❌ | ❌ |

---

## Comando: UPDATE (agregar a la sesión)

Después de cada sesión de trabajo, ejecutar:

```bash
# Agregar a Session History en AGENTS.md:
# - [$(date +%Y-%m-%d)]: [resumen de lo que se hizo]

# Actualizar Active Context:
# - Phase: [updated phase]  
# - Last session: [$(date +%Y-%m-%d) — what was done]
# - Next: [what's next]
# - Blockers: [any blockers discovered]
```

---

## Comparación con centminmod/my-claude-code-setup

El approach de centminmod usa archivos separados por AI:
```
CLAUDE-activeContext.md
CLAUDE-patterns.md  
CLAUDE-decisions.md
CLAUDE-troubleshooting.md
```

**Nuestra extensión** agrega:
- `AGENTS.md` como fuente universal (todos los AI lo leen)
- Sincronización automática a GEMINI.md y copilot-instructions.md
- Integración con always-on-memory skill para automatizar el proceso
- Soporte para Cursor/Windsurf vía antigravity-kit (.agent/ARCHITECTURE.md)

---

## Gestión de memoria global personal

Para tu memoria de desarrollador (aplica en todos los proyectos):

**`~/.copilot/copilot-instructions.md`** — perfil global:
```markdown
# Copilot Global Instructions — elihuvillaraus

## Developer Profile
- Primary languages: TypeScript, Python
- Preferred frameworks: Next.js, FastAPI, React Native + Expo
- Styling: Tailwind CSS
- DB: PostgreSQL + Drizzle ORM, Neon

## Available Skills Roster
[lista de skills instalados por categoría]

## Work Style
- Always init always-on-memory at session start
- Use orchestrator for complex multi-agent tasks
- Prefer always-ask over assume

## Agent Signals Convention
Agents signal completion with: AGENTNAME_DONE / AGENTNAME_BLOCKED
```

---

## Compatibilidad con antigravity-kit

Si el proyecto usa Cursor/Windsurf con antigravity-kit:

```bash
# Sincronizar también a .agent/
mkdir -p .agent
# Copiar secciones técnicas relevantes a .agent/ARCHITECTURE.md
```

Los agentes de antigravity-kit (.agent/agents/) leen `.agent/ARCHITECTURE.md`
automáticamente — mantenerlo sincronizado con `AGENTS.md`.

---

## Señales de operación

- `MEMORY_SYNCED: [files updated]` — sincronización exitosa
- `MEMORY_INIT: [project name]` — inicialización completa  
- `MEMORY_UPDATED: [session date]` — sesión guardada
- `MEMORY_ERROR: [reason]` — error en sincronización
