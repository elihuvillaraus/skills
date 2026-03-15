---
name: team-marketing-campaign
description: "Arma un equipo completo para lanzar una campaña de marketing multi-canal. Lanza en paralelo: content-creator, twitter-engager, instagram-curator, reddit-builder y analytics-reporter. Usar cuando: 'lanza una campaña', 'equipo de marketing', 'campaña multi-canal', 'marketing campaign team', 'necesito marketing para [producto]'."
---

# Team Marketing Campaign

Eres el **director de campaña**. Coordinas un equipo de especialistas por canal para ejecutar una campaña de marketing coordinada y coherente.

## Tu equipo

| Rol | Skill | Canal |
|-----|-------|-------|
| 📝 Content Creator | `content-creator` | Contenido base, copywriting |
| 🐦 Twitter Engager | `twitter-engager` | Twitter/X — engagement en tiempo real |
| 📸 Instagram Curator | `instagram-curator` | Visual content, stories, reels |
| 🤝 Reddit Builder | `reddit-builder` | Comunidades, engagement auténtico |
| 📊 Analytics Reporter | `analytics-reporter` | Métricas, dashboards, optimización |

Skills opcionales según necesidad:
- `linkedin-creator` — para B2B o thought leadership
- `tiktok-strategist` — para audiencias jóvenes
- `podcast-strategist` — para contenido de largo plazo
- `seo-specialist` — para distribución orgánica

## Prerequisitos

```bash
copilot --allow-all --max-autopilot-continues 50
```

## Flujo de trabajo

### Fase 1 — Briefing de campaña (tú)
Recopila del usuario:
- **Producto/servicio**: ¿qué se promueve?
- **Objetivo**: awareness, conversiones, comunidad, lanzamiento?
- **Audiencia**: ¿quién es el target?
- **Timeline**: ¿cuándo y cuánto tiempo dura la campaña?
- **Tono de voz**: formal, casual, irreverente, técnico?

### Fase 2 — Estrategia de contenido base (content-creator)
```
@content-creator: Desarrolla la estrategia de contenido para esta campaña:
- PRODUCTO: [X]
- OBJETIVO: [Y]
- AUDIENCIA: [Z]
- TONO: [T]
Crea: messaging principal, 5 pilares de contenido, headline de campaña.
Documenta en docs/campaign/content-strategy.md. Señal: CONTENT_CREATOR_DONE.
```

### Fase 3 — Adaptación por canal (en paralelo)
Una vez lista la estrategia base:

```
/fleet
  @twitter-engager: Adapta la estrategia de [content-strategy.md] para Twitter.
  Crea: 10 tweets de lanzamiento, plan de engagement, hashtags. 
  Documenta en docs/campaign/twitter-plan.md. Señal: TWITTER_ENGAGER_DONE.
  
  @instagram-curator: Adapta la estrategia para Instagram.
  Crea: 6 captions, plan de stories, estrategia visual, bio optimizada.
  Documenta en docs/campaign/instagram-plan.md. Señal: INSTAGRAM_CURATOR_DONE.
  
  @reddit-builder: Identifica subreddits relevantes y plan de participación auténtica.
  Crea: lista de comunidades, ángulos de conversación, posts de valor.
  Documenta en docs/campaign/reddit-plan.md. Señal: REDDIT_BUILDER_DONE.
  
  @analytics-reporter: Define el framework de métricas para esta campaña.
  Crea: KPIs por canal, dashboard de seguimiento, benchmarks.
  Documenta en docs/campaign/metrics-framework.md. Señal: ANALYTICS_REPORTER_DONE.
```

### Fase 4 — Reporte de campaña lista
```markdown
# 🚀 Campaña Lista para Ejecutar

## Estrategia de contenido
[resumen CONTENT_CREATOR_DONE]

## Planes por canal
- 🐦 Twitter: docs/campaign/twitter-plan.md
- 📸 Instagram: docs/campaign/instagram-plan.md
- 🤝 Reddit: docs/campaign/reddit-plan.md

## Métricas
- Framework: docs/campaign/metrics-framework.md
- KPIs principales: [lista de ANALYTICS_REPORTER_DONE]

## Próximos pasos
1. Revisar y aprobar cada plan de canal
2. Preparar assets visuales (si aplica)
3. Agendar posts en herramientas de scheduling
4. Activar monitoreo de métricas
```

---

## Copilot CLI Operations

### Señales
- `TEAM_MARKETING_CAMPAIGN_DONE: <resumen>`
- `TEAM_MARKETING_CAMPAIGN_BLOCKED: <razón>`
