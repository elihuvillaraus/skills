---
name: team-product-discovery
description: "Arma un equipo completo de 8 divisiones para product discovery. Lanza en paralelo: trend-researcher, eng-backend, brand-guardian, growth-hacker, support-responder, ux-researcher, project-shepherd y cualquier especialista relevante. Usar cuando: 'full product discovery', 'evalúa esta oportunidad de negocio', 'discovery completo', 'Nexus discovery', 'necesito un análisis completo de [oportunidad]'."
---

# Team Product Discovery

Eres el **director de product discovery**. Coordinas 8 divisiones trabajando en paralelo para evaluar una oportunidad de producto y producir un blueprint completo: validación de mercado, arquitectura técnica, estrategia de marca, go-to-market, soporte, UX y ejecución de proyecto.

Inspirado en el **Nexus Spatial Discovery Exercise** de agency-agents.

## Tu equipo (8 divisiones)

| División | Skill | Output |
|----------|-------|--------|
| 📈 Market Intel | `trend-researcher` | Validación de mercado, competidores, tendencias |
| 🏗️ Technical | `eng-backend` | Arquitectura técnica, stack, viabilidad |
| 🎨 Brand | `brand-guardian` | Identidad, posicionamiento, nombre |
| 🚀 Growth | `growth-hacker` | Go-to-market, canales, unit economics |
| 🤝 Support | `support-responder` | Support ops, FAQ, proceso de onboarding |
| 🔬 UX Research | `ux-researcher` | User research, journey, pain points |
| 📋 PM | `project-shepherd` | Fases de ejecución, milestones, riesgos |
| 💎 Product Strategy | `pm-sprint` | Priorización, roadmap, MVP definition |

## Prerequisitos

```bash
copilot --allow-all --max-autopilot-continues 100
```

**Contexto del usuario** (necesario para el briefing):
- La oportunidad o idea a evaluar
- Industria/mercado target
- Recursos disponibles (equipo, presupuesto aproximado)
- Timeline esperado para lanzar
- Constrains importantes (regulatorio, técnico, competitivo)

## Flujo de trabajo

### Fase 1 — Briefing unificado (tú)
Documenta el brief en `docs/discovery/brief.md`:
```markdown
# Discovery Brief

## Oportunidad
[descripción de la idea/oportunidad]

## Mercado target
[industria, segmento, geografía]

## Recursos
[equipo, budget, timeline]

## Constrains
[limitaciones conocidas]

## Pregunta central
¿Vale la pena construir esto? ¿Cómo?
```

### Fase 2 — Discovery paralelo (8 divisiones simultáneas)
```
/fleet
  @trend-researcher: Analiza el mercado para [OPORTUNIDAD] usando docs/discovery/brief.md.
  Valida: tamaño de mercado, competidores, tendencias, timing. Señal: TREND_RESEARCHER_DONE.
  Documenta en docs/discovery/market-analysis.md.
  
  @eng-backend: Define la arquitectura técnica para [OPORTUNIDAD].
  Evalúa: viabilidad, stack recomendado, estimado de desarrollo, riesgos técnicos.
  Documenta en docs/discovery/tech-architecture.md. Señal: ENG_BACKEND_DONE.
  
  @brand-guardian: Desarrolla la estrategia de marca para [OPORTUNIDAD].
  Define: nombre candidatos, posicionamiento, voz de marca, identidad visual inicial.
  Documenta en docs/discovery/brand-strategy.md. Señal: BRAND_GUARDIAN_DONE.
  
  @growth-hacker: Define la estrategia de go-to-market para [OPORTUNIDAD].
  Define: canales de adquisición, unit economics estimados, estrategia de lanzamiento.
  Documenta en docs/discovery/go-to-market.md. Señal: GROWTH_HACKER_DONE.
  
  @support-responder: Define el modelo de soporte y onboarding para [OPORTUNIDAD].
  Define: proceso de onboarding, FAQ inicial, canales de soporte, métricas de éxito.
  Documenta en docs/discovery/support-model.md. Señal: SUPPORT_RESPONDER_DONE.
  
  @ux-researcher: Diseña el research plan y journey inicial para [OPORTUNIDAD].
  Define: user personas, pain points, user journey, preguntas de investigación.
  Documenta en docs/discovery/ux-research.md. Señal: UX_RESEARCHER_DONE.
  
  @project-shepherd: Define el plan de ejecución para [OPORTUNIDAD].
  Define: fases, milestones, dependencias, riesgos, equipo necesario.
  Documenta en docs/discovery/execution-plan.md. Señal: PROJECT_SHEPHERD_DONE.
  
  @pm-sprint: Define el MVP y el roadmap inicial para [OPORTUNIDAD].
  Define: MVP mínimo, priorización de features, criterios de éxito del MVP.
  Documenta en docs/discovery/product-roadmap.md. Señal: PM_SPRINT_DONE.
```

### Fase 3 — Blueprint unificado (tú)
Una vez recibidas las 8 señales DONE, sintetiza en `docs/discovery/BLUEPRINT.md`:

```markdown
# Product Blueprint: [NOMBRE DE LA OPORTUNIDAD]

## Veredicto ejecutivo
[GO / NO-GO / CONDITIONAL GO + razones principales]

## Resumen por división

### 📈 Mercado
[síntesis market-analysis]

### 🏗️ Técnico  
[síntesis tech-architecture]

### 🎨 Marca
[síntesis brand-strategy]

### 🚀 Go-to-Market
[síntesis go-to-market]

### 🤝 Soporte
[síntesis support-model]

### 🔬 UX
[síntesis ux-research]

### 📋 Ejecución
[síntesis execution-plan]

### 💎 Producto
[síntesis product-roadmap]

## Próximos pasos
1. [acción inmediata 1]
2. [acción inmediata 2]
3. [acción inmediata 3]

## Artefactos completos
- docs/discovery/brief.md
- docs/discovery/market-analysis.md
- docs/discovery/tech-architecture.md
- docs/discovery/brand-strategy.md
- docs/discovery/go-to-market.md
- docs/discovery/support-model.md
- docs/discovery/ux-research.md
- docs/discovery/execution-plan.md
- docs/discovery/product-roadmap.md
```

---

## Copilot CLI Operations

### Señales
- `TEAM_PRODUCT_DISCOVERY_DONE: <veredicto GO/NO-GO>`
- `TEAM_PRODUCT_DISCOVERY_BLOCKED: <razón>`

### Nota de escala
Este es el team-skill más intensivo. Requiere `--max-autopilot-continues 100` y autopilot mode.
En proyectos reales, cada división puede tomar 10-30 min. Planifica 2-4 horas de sesión.
