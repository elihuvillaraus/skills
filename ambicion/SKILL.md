---
name: ambicion
description: Puerta de ambición antes de ejecutar una tarea no trivial. Pregunta cuál es el objetivo detrás del objetivo (Altitud), cómo lo haría el mejor experto con sus herramientas y datos crudos (Profundidad) y qué otros campos aportarían, haciendo su trabajo y no actuándolo (Alcance); fija una meta dura, un juez externo y el modelo y esfuerzo adecuados, y reescribe el pedido a ese nivel. Basada en el artículo de Felix Rieseberg "How to be more ambitious" y la skill be-ambitious de RoboNuggets (MIT), adaptada a nuestro stack. Usar con /ambicion, "sé más ambicioso", "sube el nivel", "cuál es el objetivo detrás", "cómo lo haría un experto", "revisa si vamos por el mejor enfoque", y como Fase 0.1 del orquestador en toda tarea no trivial.
argument-hint: "[tarea o pedido a mejorar]"
license: MIT
metadata:
  fuente: https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/
  derivada-de: https://github.com/robonuggets/be-ambitious (MIT)
---

# Ambición (puerta previa a ejecutar)

Mejor, no más grande. Cada tipo sube algo: el resultado (Altitud), el estándar (Profundidad) o el número de miradas (Alcance). Si una sugerencia agranda el trabajo sin mejorarlo, descártala. La ambición sube el estándar, no los permisos: lo irreversible, lo que cuesta dinero o lo que reemplaza lo pedido se confirma antes (bandeja `pedir`).

## Cuándo corre y cuándo no

- **Corre** (modo completo): objetivo que sirve a un resultado de negocio, entrega a clientes, decisiones de arquitectura, algo que se repetirá, o cualquier tarea que el orquestador clasifique como no trivial.
- **Modo corto** (3 líneas): tareas medianas. Solo objetivo detrás del objetivo, juez externo y modelo.
- **No corre**: ediciones puntuales, preguntas, lecturas, correcciones de una línea. Si dudas, modo corto.

## Los tres tipos (elige uno o dos, casi nunca los tres)

| Tipo | Úsalo cuando | Sáltalo cuando |
|---|---|---|
| Altitud | La tarea sirve a un resultado. Señal: habría reuniones para discutirla | Trabajo creativo sin resultado más allá de sí mismo |
| Profundidad | Debe quedar realmente bien | Desechable |
| Alcance | Debe llegar a personas, o el campo obvio ya no da ideas | Arreglo puntual con una sola respuesta |

**Altitud.** Pregunta: ¿qué quieres que pase después? ¿cuál es el objetivo detrás del objetivo? Escalera de tres peldaños, cada uno más alto: (1) entender en vez de rellenar, (2) llegar a decisiones con a favor y en contra, (3) reemplazar el ritual (diseñar algo mejor, demostrarlo con nuestra propia historia y correrlo en paralelo). Los flujos duraderos suelen pedir preparación antes: acceso a datos, mapa versión→código, máquinas para reproducir. Nómbrala como parte del plan. Techo: si un peldaño no tiene juez externo, baja uno.

**Profundidad.** Baja un nivel: del entregable a los datos, herramientas y el problema real.
- Las herramientas del experto, no su vocabulario: donde saldría una tabla markdown, un científico de datos usa base de datos y un modelo estadístico. Cambiar de jerga sin cambiar de método es teatro.
- Meta irrazonable tratada como razonable: si piden 5 s, apunta a 200 ms; si el modelo dice "imposible", "es muy resoluble, sigue".
- Desafía lo que se cree: parte de datos crudos y trata de reproducir la creencia ("creemos que la baja es de onboarding; reprodúcelo").
- Conocimiento nuevo: ya dentro de los datos, busca el punto ciego y comprueba que predice sobre datos no vistos.
- Prompt de Felix, textual, para cualquier tarea: *"I want a deeper version of this task, not a bigger one. Before rewriting it: (1) say what a top professional in this field would do here that I'm not asking for; (2) name the rawest material they would start from instead of what has already been digested for me; (3) name the specific methods and tools they would use; (4) say what, other than you or me, would show the result is right. Then rewrite my prompt to ask for exactly that."*

**Alcance.** Mira el trabajo desde más campos de los que antes era rentable.
- Cambia sustantivos por verbos: "una presentación" es "lograr que gente ocupada crea una historia de causa y efecto y decida con incertidumbre en 30 minutos". Los verbos revelan qué campos ayudan.
- Arma el equipo: cinco expertos de campos distintos, dos de ellos para encontrar qué está mal (red team: vendedor en corto, contador forense). Cada uno hace su trabajo con sus métodos; no actúa un personaje.
- Cuesta tokens: equipo completo solo en lo más importante. Un subagente por campo, con su método y sus herramientas.

## Juez externo (regla que no se negocia)

Nunca juzgues tu propio trabajo ni dejes que el modelo lo juzgue: los modelos coinciden con quien los lee. Define antes de empezar qué, distinto de ti y del usuario, demuestra que está bien, y elige el más duro disponible:

| Qué se hizo | Juez |
|---|---|
| Código / app | tests que fallan antes y pasan después, skill `evaluator` y `tester` (Playwright en la app real) |
| Rendimiento | medición repetida (Lighthouse u otra) y presupuesto que falle si se rompe |
| Decisión, arquitectura, precio, entrega de alto riesgo | `dia-del-juicio` (dos jueces ciegos) o `llm-council` |
| Contenido / marca | `brand-guardian`, `reality-checker`; cifras verificadas contra el dato fuente |
| Algo que el usuario debe aprobar o hacer | `mcp__bandeja__pedir` con `verifica` si hay comando de solo lectura |

Informa contra el juez con honestidad: una meta dura fallada con números reales es un buen resultado; una fingida no lo es.

## Equipo (Alcance) con lo que ya tenemos

Campo → skill o agente: analista de datos `analytics-reporter`; investigación de tendencias `trend-researcher`; usuario `ux-researcher`; diseño `ui-designer` / `ux-architect`; marca y voz `brand-strategist`, `voice-md`; estrategia comercial `deal-strategist`, `proposal-strategist`; riesgo `security-eng`, `compliance-auditor`; red team `reality-checker`, `dia-del-juicio`. Si el campo no está en esta lista, descríbelo como verbo y un método, y lanza un subagente.

## Modelo, esfuerzo y costo (parte de la puerta)

Cada puerta responde también "¿vamos con el modelo correcto?" según la tabla del orquestador (`~/.claude/AGENTS.md`, "Modelos y orquestación"): haiku para volumen y lecturas, sonnet para lo que se entrega (ralph, evaluator, researcher), opus para síntesis y jueces. Un equipo de Alcance son subagentes: pasa `model` explícito. Esfuerzo `medium` por defecto; súbelo solo donde esté medido. Para trabajo masivo y repetible, mira `claude -p` con Haiku 5.5 contra los créditos de API en vez de gastar la sesión interactiva.

## Acceso (no lo finjas)

Todo esto exige una computadora donde instalar software y los datos reales (MCP u otros medios). Si falta algo, nombra exactamente qué falta y qué desbloquearía. Nunca inventes una fuente, herramienta o resultado para tapar el hueco.

## Salida (proporcional a la tarea; una línea de pedido = pocas líneas de plan)

1. **Objetivo detrás del objetivo**, una línea.
2. **Tipos que aplican** (y los saltados), una línea cada uno con el porqué.
3. **Plan** por tipo: escalera de Altitud; las cuatro respuestas y la meta dura de Profundidad; verbos y equipo (campo, qué hace, método) de Alcance.
4. **Juez externo y criterio de aprobado.**
5. **Modelo/esfuerzo** y costo estimado si hay subagentes.
6. **Qué necesita**: datos, herramientas y acceso, marcado como presente o faltante.
7. **Pedido reescrito** en un solo bloque copiable, como lo escribiría el usuario, terminando con el juez y qué cuenta como aprobado.
8. **Siguiente:** el peldaño más alto que se pueda terminar y comprobar con el acceso actual. Tarea para hacer → nómbralo y empieza. Pedido para mejorar → detente tras el pedido reescrito. Si ni el primer peldaño tiene acceso, pídelo y detente. Pregunta antes si el peldaño reemplaza lo pedido, gasta dinero o no se puede deshacer.

## Ejemplo corto

`/ambicion arregla el crash del login`
- Objetivo: la gente siempre puede entrar.
- Tipos: Altitud y Profundidad; Alcance saltado (un crash tiene una respuesta).
- Altitud: (1) arreglar este crash con una prueba que falla y luego pasa; (2) buscar todos los crashes de esta clase en los reportes y arreglar la causa; (3) mantener el login sin crashes: traer reportes, mapear versión a commit, reproducir en cada plataforma, verificar sin que lo pidan.
- Profundidad: partir de los volcados crudos, reproducir antes de arreglar; meta: cero crashes de login en el próximo release, no "menos".
- Juez: la prueba pasa a verde y la tasa de crashes del build llega a cero en la herramienta de reportes.

## Por qué funciona

Autoeficacia: quien cree poder, logra más, y se puede provocar. Dantzig resolvió dos problemas abiertos de estadística en 1939 porque creyó que eran tarea. Bannister rompió la milla en 4 min y otro lo repitió 46 días después. Con el modelo igual: di que lo difícil es posible, da permiso de fallar frente a un juez honesto, y recuerda el porqué; sin propósito solo vas más rápido sin rumbo.
