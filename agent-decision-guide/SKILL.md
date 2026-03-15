---
name: agent-decision-guide
description: "Guía definitiva sobre cuándo usar un SKILL vs un AGENTE en GitHub Copilot CLI. Consultar antes de diseñar cualquier automatización, subagente, o flujo multi-agente. Trigger: 'qué uso skill o agente', 'cuándo usar agente', 'skill vs agent', 'cómo estructura mis agentes', 'when to use agent', 'agent architecture'."
---

# Skill vs Agent — Guía de Decisión para GitHub Copilot CLI

## TL;DR — Regla rápida

| Si necesitas... | Usa |
|---|---|
| Que YO (Copilot) **sepa** algo o **se comporte** diferente | **SKILL** |
| Que alguien **haga** trabajo de forma autónoma en paralelo | **AGENTE** |

---

## La arquitectura real del Copilot CLI

```
┌─────────────────────────────────────────────────────┐
│              USUARIO                                │
│                 ↓ mensaje                           │
│   ┌─────────────────────────────────┐              │
│   │    COPILOT CLI (Main Agent)     │ ← tú eres yo │
│   │  Context: Skills cargados aquí  │              │
│   │  Herramientas: bash, git, file  │              │
│   └──────────────┬──────────────────┘              │
│                  │ lanza via task tool              │
│        ┌─────────┼─────────┐                       │
│        ↓         ↓         ↓                       │
│   [ralph]   [tester]  [documenter]                 │
│   subagente  subagente  subagente                  │
│   SEPARADO   SEPARADO   SEPARADO                   │
│   (su propio contexto, herramientas, ejecución)    │
└─────────────────────────────────────────────────────┘
```

**Skills** = se cargan EN el contexto del agente principal. Yo los leo y adopto su conocimiento/comportamiento.

**Agentes (subagents)** = procesos separados, lanzados via `task` tool, con su propio contexto y herramientas. Trabajan de forma autónoma.

---

## SKILLS — ¿Cuándo usar?

Un skill es conocimiento o comportamiento inyectado al agente principal (yo).

### ✅ Usa un SKILL cuando:

1. **Es conocimiento de dominio** que quieres que yo aplique inline
   - Patrones de React, mejores prácticas de API, reglas de SEO
   - El skill me hace más inteligente sobre ese tema

2. **Es un modo de comportamiento** que debo adoptar
   - Plan mode, review mode, strict TDD mode
   - Cambia CÓMO pienso y actúo

3. **Es conocimiento de empresa/proyecto** persistente
   - Guía de estilo, decisiones de arquitectura, stack tecnológico
   - Lo que normalmente va en CLAUDE.md o AGENTS.md

4. **La tarea requiere contexto de la conversación actual**
   - Historial de lo que estamos haciendo juntos
   - Necesita mi contexto acumulado

5. **Es una guía de proceso** (SOP) que YO ejecuto
   - "Cómo hacer code review paso a paso"
   - "Cómo escribir un PRD"

### Ejemplos de buenos SKILLS:
```
seo-specialist    → conocimiento de SEO que aplico cuando lo necesitas
brand-guardian    → conocimiento de identidad de marca para respetar
content-creator   → cómo crear contenido efectivo
always-on-memory  → cómo mantener memoria entre sesiones
architect         → cómo diseñar una arquitectura de feature
```

---

## AGENTES — ¿Cuándo usar?

Un agente es un worker autónomo lanzado en su propio contexto separado.

### ✅ Usa un AGENTE cuando:

1. **Puede trabajar en PARALELO** con otros agentes
   - Múltiples user stories implementadas al mismo tiempo
   - Review de seguridad mientras se implementa la feature

2. **La tarea es DELEGABLE** — bien definida, con inputs y outputs claros
   - "Implementa US003 del PRD"
   - "Haz code review de estos archivos"
   - "Escribe los tests para este componente"

3. **Necesita su PROPIO CONTEXTO** limpio sin interferir con el mío
   - Trabajo largo que llenaría mi ventana de contexto
   - Tareas que no necesitan historial de conversación

4. **Emite SEÑALES** al terminar para coordinación
   - `RALPH_DONE`, `TESTER_DONE`, `DOCUMENTER_DONE`
   - El orchestrator espera estas señales para continuar

5. **Es un ESPECIALISTA** que ejecuta, no que aconseja
   - Escribe código, crea archivos, corre tests, hace commits
   - NOT: "¿qué opinas sobre este código?"

### Ejemplos de buenos AGENTES:
```
ralph         → implementa user stories autónomamente
tester        → corre tests, escribe specs, reporta cobertura
documenter    → hace commits, actualiza PRD checkboxes
architect     → genera PRD completo y GitHub issue
ui-ux-designer → diseña e implementa UI completa
```

---

## La confusión: agency-agents como skills

Los roles de `msitarzewski/agency-agents` (eng-frontend, security-eng, etc.) fueron convertidos a **skills**, pero conceptualmente son agentes.

### ¿Cuál es la realidad?

En el Copilot CLI, un skill PUEDE comportarse como agente cuando se lanza via `task` tool:

```
# Modo SKILL (el conocimiento de eng-frontend me informa a mí):
"Con el skill eng-frontend activo, revisa este componente"

# Modo AGENTE (eng-frontend ejecuta autónomamente en su propio contexto):
task(agent_type="general-purpose", prompt="Usando el skill eng-frontend, implementa el componente Login con React + Tailwind. Cuando termines señala ENG_FRONTEND_DONE")
```

### El formato importa:

| Aspecto | Skill puro | Skill usado como agente |
|---|---|---|
| **Formato** | Conocimiento/guía | Tiene task intake + signals |
| **Invocación** | Auto-detectado por contexto | Lanzado explícitamente via task tool |
| **Output** | Informational | Archivos creados + señal DONE |
| **Paralelo** | No (comparte mi contexto) | Sí (su propio proceso) |

---

## Framework de decisión — Árbol rápido

```
¿Es conocimiento o comportamiento que yo (Copilot) debo tener?
  → SKILL

¿Es trabajo que alguien debe HACER de forma autónoma?
  ↓
  ¿Puede ir en paralelo con otras tareas?
    → SÍ → AGENTE definitivamente
    → NO → Podría ser SKILL con sección de ejecución

  ¿Emite señal cuando termina?
    → SÍ → AGENTE
    → NO → Probablemente SKILL

  ¿Necesita contexto de conversación actual?
    → SÍ → SKILL (lanzarlo como agente perdería el contexto)
    → NO → AGENTE es mejor opción
```

---

## Tabla de clasificación del roster actual

### Deben funcionar principalmente como AGENTES (lanzar via task tool):

| Skill | Tipo correcto | Señal |
|---|---|---|
| `ralph` | Agente implementador | `RALPH_DONE` / `RALPH_BLOCKED` |
| `tester` | Agente de QA | `TESTER_DONE` / `TESTER_BLOCKED` |
| `documenter` | Agente documentador | Commits + updates |
| `architect` | Agente planificador | PRD creado |
| `eng-frontend` | Agente coder (frontend) | `ENG_FRONTEND_DONE` |
| `eng-backend` | Agente coder (backend) | `ENG_BACKEND_DONE` |
| `eng-senior` | Agente coder (senior) | `ENG_SENIOR_DONE` |
| `security-eng` | Agente de security review | `SECURITY_ENG_DONE` |
| `devops` | Agente de infraestructura | `DEVOPS_DONE` |
| `sre` | Agente de reliability | `SRE_DONE` |
| `ui-designer` | Agente de diseño UI | `UI_DESIGNER_DONE` |
| `ux-architect` | Agente de UX | `UX_ARCHITECT_DONE` |
| `mobile-builder` | Agente mobile | `MOBILE_BUILDER_DONE` |
| `rapid-proto` | Agente prototipado | `RAPID_PROTO_DONE` |
| `software-architect` | Agente arquitectura | `SOFTWARE_ARCHITECT_DONE` |
| `db-optimizer` | Agente DB | `DB_OPTIMIZER_DONE` |
| `code-reviewer` | Agente de review | `CODE_REVIEWER_DONE` |
| `reality-checker` | Agente de validación | `REALITY_CHECKER_DONE` |

### Deben funcionar principalmente como SKILLS (conocimiento inline):

| Skill | Razón |
|---|---|
| `brand-guardian` | Conocimiento de marca para aplicar en cada respuesta |
| `growth-hacker` | Framework mental, no ejecutor de código |
| `seo-specialist` | Conocimiento de SEO a aplicar inline |
| `content-creator` | Guía de creación de contenido |
| `analytics-reporter` | Métricas e interpretación |
| `always-on-memory` | Gestión de memoria/contexto |
| `multi-ai-memory` | Sincronización de contexto multi-AI |
| `orchestrator` | Meta-skill que coordina otros |
| `team-*` | Orchestrators de equipos |

---

## Cómo LANZAR un skill como agente

Para lanzar `eng-frontend` como agente autónomo:

```
task(
  agent_type="general-purpose",
  description="Frontend implementation",
  mode="background",
  prompt="""
  Eres un Frontend Developer senior (skill eng-frontend).
  
  TASK: Implementa [descripción específica del componente/feature]
  
  CONTEXTO:
  - Repo: [path del proyecto]
  - Stack: [React + TypeScript + Tailwind]
  - Design: [referencia al diseño]
  - Archivos relacionados: [lista]
  
  CUANDO TERMINES:
  - Asegúrate que todo compila sin errores
  - Escribe "ENG_FRONTEND_DONE" como última línea
  - Si encuentras un blocker, escribe "ENG_FRONTEND_BLOCKED: [razón]"
  """
)
```

---

## Multi-AI: el mismo skill para todos

GitHub Copilot CLI lee estas fuentes de contexto en TODOS los proyectos:

```
AGENTS.md           ← Universal (Claude + Gemini + Copilot lo leen)
CLAUDE.md           ← Claude Code específico
GEMINI.md           ← Gemini CLI específico
.github/copilot-instructions.md ← Copilot específico
~/.copilot/copilot-instructions.md ← Global Copilot
```

**Regla de oro**: Pon en `AGENTS.md` lo que quieres que TODOS los AI sepan.
Usa los archivos específicos solo para instrucciones que son exclusivas de ese tool.

Usa el skill `multi-ai-memory` para gestionar estos archivos automáticamente.
