---
name: always-on-memory
description: "Persistent memory system for AI coding sessions. Maintains AGENTS.md (universal memory bank read by ALL AI tools: Claude, Gemini, Copilot), session state docs, and project context. Use at session start to load context, during sessions to record decisions/progress, and at session end to persist learnings. Trigger: 'save memory', 'load context', 'update memory bank', 'persist session', 'always on memory', 'init memory', 'sync memory'."
---

# Always-On Memory — Sistema de Memoria Persistente

Eres el gestor de memoria persistente. Tu objetivo es que el contexto NO SE PIERDA entre sesiones y que TODOS los AI tools (Claude Code, Gemini CLI, GitHub Copilot CLI) compartan la misma base de conocimiento.

## Filosofía

```
Sin memoria: cada sesión empieza desde cero
Con always-on-memory: cada sesión empieza donde dejaste
```

La clave es escribir a archivos estándar que TODOS los AI leen automáticamente:
- `AGENTS.md` — leído por Claude, Gemini, y Copilot CLI
- `CLAUDE.md` — instrucciones específicas para Claude Code
- `GEMINI.md` — instrucciones específicas para Gemini CLI
- `.github/copilot-instructions.md` — instrucciones para GitHub Copilot
- `~/.copilot/copilot-instructions.md` — global para Copilot CLI

---

## Comandos del sistema

### 🚀 INIT — Inicio de sesión

Al inicio de cualquier sesión en un proyecto:

```bash
# 1. Check si existe AGENTS.md
cat AGENTS.md 2>/dev/null || echo "No memory bank found — will create"

# 2. Leer y cargar contexto
cat AGENTS.md
cat .github/copilot-instructions.md 2>/dev/null
```

Luego reportar al usuario:
> "✅ Contexto cargado. Último trabajo: [última entrada de activeContext]. Stack: [stack]. Continuando..."

Si NO existe `AGENTS.md`, ejecutar SETUP.

---

### 📋 SETUP — Primera vez en un proyecto

Crear la estructura de memoria:

```bash
# Crear directorio docs si no existe
mkdir -p docs .github

# Template AGENTS.md
cat > AGENTS.md << 'EOF'
# Memory Bank — [Project Name]
> Universal AI Memory: Read by Claude Code, Gemini CLI, and GitHub Copilot CLI

## Project Overview
- **Name**: [project name]
- **Stack**: [tech stack]
- **Purpose**: [what this project does]
- **Repo**: [GitHub URL if applicable]

## Active Context
- **Current sprint/phase**: [phase]
- **Last worked on**: [feature/task]
- **Status**: [in progress / blocked / done]

## Architecture Decisions
<!-- Record important decisions with their rationale -->
- [date]: [decision] — Reason: [why]

## Established Patterns
<!-- Code patterns, conventions, rules for THIS project -->
- [pattern description]

## Key Files
<!-- The most important files to know about -->
- `[path]` — [what it does]

## Common Commands
```bash
# Development
[dev command]

# Build
[build command]

# Test
[test command]
```

## Known Issues / Blockers
<!-- Active problems being worked on -->
- [ ] [issue description]

## Completed Milestones
<!-- History of what was accomplished -->
- [date]: [what was done]
EOF

echo "✅ AGENTS.md created"
```

---

### 💾 SAVE — Guardar progreso (durante/fin de sesión)

Actualizar la sección **Active Context** de `AGENTS.md`:

```bash
# Update activeContext section
# Replace "Active Context" section with current state
```

Elementos a siempre actualizar:
1. **Last worked on**: ¿qué fue lo último?
2. **Status**: ¿en qué estado quedó?
3. **Architecture Decisions**: ¿se tomó alguna decisión importante?
4. **Established Patterns**: ¿se descubrió algún patrón?
5. **Known Issues**: ¿hay algo bloqueado?
6. **Completed Milestones**: ¿qué se terminó?

---

### 🔄 SYNC — Sincronizar a todos los AI tools

Después de actualizar `AGENTS.md`, sincronizar contexto relevante a:

**`.github/copilot-instructions.md`** (Copilot específico):
```markdown
# Copilot Instructions — [Project Name]
> Auto-synced from AGENTS.md by always-on-memory

## Stack
[stack from AGENTS.md]

## Key Patterns
[patterns from AGENTS.md]

## Current Focus
[activeContext from AGENTS.md]
```

**`CLAUDE.md`** (si el proyecto usa Claude Code):
```markdown
# CLAUDE.md
> Instrucciones para Claude Code en este proyecto

[Technical patterns relevant to code editing]
[Banned tools / preferences]
[Memory bank system files to check]
```

---

## Estructura de archivos de memoria

```
proyecto/
├── AGENTS.md                          ← Universal (todos leen)
├── CLAUDE.md                          ← Claude Code específico
├── GEMINI.md                          ← Gemini CLI específico
├── .github/
│   └── copilot-instructions.md        ← GitHub Copilot específico
└── docs/
    ├── ALWAYS-ON-MEMORY.md            ← Estado de sesión actual
    ├── USER-TASKS.md                  ← Tareas identificadas
    └── USER-QA.md                     ← Pasos de QA manual
```

---

## Integración con el Pipeline

### En el Orchestrator (Phase 0):
```
1. Llamar always-on-memory → INIT
2. Si primer vez → SETUP
3. Cargar contexto en memoria de la sesión
4. Proceder con el pipeline
```

### Durante implementación (Phase 3):
```
Cada RALPH_DONE → always-on-memory SAVE:
  - Registrar US completada
  - Actualizar progreso
  - Notar patterns nuevos descubiertos
```

### Al finalizar (Phase 6):
```
1. always-on-memory SAVE — estado final
2. always-on-memory SYNC — propagar a todos los AI
3. Commit AGENTS.md con el pipeline
```

---

## Formato de AGENTS.md para equipos multi-AI

El archivo `AGENTS.md` es la **única fuente de verdad** universal.

### Reglas de escritura:
1. **Siempre en inglés o idioma consistente** (para compatibilidad multi-AI)
2. **Secciones fijas** (los AI las buscan por nombre)
3. **Entries con fecha** en historial
4. **Evitar información sensible** (secrets, tokens, passwords)
5. **Máximo 500 líneas** — si crece más, crear AGENTS-[topic].md

### Secciones obligatorias:
- `## Project Overview` — qué es esto
- `## Active Context` — estado actual
- `## Architecture Decisions` — decisiones tomadas
- `## Established Patterns` — convenciones del proyecto
- `## Key Files` — mapa de archivos importantes

### Secciones opcionales:
- `## Known Issues` — bugs activos
- `## Completed Milestones` — historial
- `## Common Commands` — comandos útiles
- `## Team Notes` — notas del equipo

---

## Gestión de contexto global (~/.copilot/)

Para contexto que aplica a TODOS tus proyectos:

```bash
# Ver instrucciones globales
cat ~/.copilot/copilot-instructions.md

# Actualizar contexto global
# (skills roster, preferencias, estilo de trabajo)
```

El archivo `~/.copilot/copilot-instructions.md` es tu **perfil de desarrollador** —
cosas como tu stack preferido, el roster de skills disponibles, y reglas de trabajo
que aplican en cualquier proyecto.

---

## Señal de operación

Al finalizar cualquier operación always-on-memory:
- Éxito: `MEMORY_SYNCED` + resumen de cambios
- Error: `MEMORY_ERROR: [razón]`
