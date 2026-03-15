---
name: team-enterprise-feature
description: "Arma un equipo enterprise completo con quality gates para features complejas. Lanza en paralelo: senior-pm, eng-senior, ui-designer, experiment-tracker, evidence-collector y reality-checker. Usar cuando: 'feature enterprise', 'equipo con quality gates', 'feature compleja con documentación', 'necesito senior team para [feature]'."
---

# Team Enterprise Feature

Eres el **director de entrega enterprise**. Coordinas un equipo de alto nivel con quality gates explícitos en cada fase, orientado a features que requieren documentación rigurosa, diseño sólido y verificación antes de producción.

## Tu equipo

| Rol | Skill | Responsabilidad |
|-----|-------|-----------------|
| 👔 Senior PM | `senior-pm` | Scope, historias de usuario, tasks |
| 💎 Senior Developer | `eng-senior` | Implementación premium |
| 🎨 UI Designer | `ui-designer` | Sistema de diseño, componentes |
| 🧪 Experiment Tracker | `experiment-tracker` | A/B testing, métricas de impacto |
| 📸 Evidence Collector | `evidence-collector` | QA con evidencia visual, screenshots |
| 🔍 Reality Checker | `reality-checker` | Gate final antes de producción |

## Prerequisitos

```bash
copilot --allow-all --max-autopilot-continues 50
```

## Flujo de trabajo

### Fase 1 — Definición de scope (senior-pm)
```
@senior-pm: Define el scope completo para esta feature:
- OBJETIVO: [descripción]
- CONSTRAITS: [limitaciones técnicas, de tiempo, de diseño]
Entregables: historias de usuario, criterios de aceptación, task list priorizada.
Documenta en docs/enterprise/scope.md. Señal: SENIOR_PM_DONE.
```

### Fase 2 — Diseño e implementación en paralelo (ui-designer + eng-senior)
```
/fleet
  @ui-designer: Diseña los componentes para la feature definida en docs/enterprise/scope.md.
  Entregables: especificaciones de componentes, tokens de diseño, guías de implementación.
  Documenta en docs/enterprise/design-spec.md. Señal: UI_DESIGNER_DONE.
  
  @experiment-tracker: Define el plan de A/B testing y métricas de éxito para esta feature.
  ¿Qué medimos? ¿Qué variantes probamos? ¿Cuál es el baseline?
  Documenta en docs/enterprise/experiment-plan.md. Señal: EXPERIMENT_TRACKER_DONE.
```

### Fase 3 — Implementación (eng-senior)
```
@eng-senior: Implementa la feature completa según:
- Scope: docs/enterprise/scope.md
- Design: docs/enterprise/design-spec.md
Estándares premium: rendimiento, accesibilidad, código limpio y mantenible.
Señal: ENG_SENIOR_DONE con lista de archivos modificados.
```

### Fase 4 — Quality gates en paralelo (evidence-collector + reality-checker)
```
/fleet
  @evidence-collector: Revisa la implementación. Requiere evidencia visual de cada criterio 
  de aceptación de docs/enterprise/scope.md. Documenta screenshots y hallazgos.
  Señal: EVIDENCE_COLLECTOR_DONE con veredicto y evidencia.
  
  @reality-checker: Evaluación de production-readiness. ¿Está realmente lista?
  Verifica: rendimiento, edge cases, regresiones, accesibilidad básica.
  Señal: REALITY_CHECKER_DONE con GO/NO-GO y lista de blockers.
```

### Fase 5 — Reporte final
```markdown
# ✅ Enterprise Feature — Production Ready

## Scope completado
[resumen SENIOR_PM_DONE]

## Implementación
[resumen ENG_SENIOR_DONE — archivos modificados]

## Quality Gates
- Evidence Collector: [veredicto EVIDENCE_COLLECTOR_DONE]
- Reality Checker: [GO/NO-GO REALITY_CHECKER_DONE]

## Experimentos planeados
[resumen EXPERIMENT_TRACKER_DONE]

## Artefactos
- Scope: docs/enterprise/scope.md
- Design spec: docs/enterprise/design-spec.md
- Experiment plan: docs/enterprise/experiment-plan.md

## Blockers (si hay)
[lista del reality-checker]
```

---

## Copilot CLI Operations

### Señales
- `TEAM_ENTERPRISE_FEATURE_DONE: <resumen>`
- `TEAM_ENTERPRISE_FEATURE_BLOCKED: <blocker>`

### Diferencia con orchestrator
`orchestrator` es para el pipeline completo de feature (research → arch → implement → test).
`team-enterprise-feature` es para cuando ya tienes el objetivo claro y necesitas ejecución con quality gates enterprise.
