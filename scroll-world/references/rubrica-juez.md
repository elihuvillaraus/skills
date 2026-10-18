# Rúbrica del juez (0-10 por escena; aprobado = todas ≥ 8)

Quién juzga: un subagente que no programó nada, sin contexto del proyecto, con 6-12 stills de la escena (`tools/walk.mjs --stops`), un frame de referencia si existe y este documento. Modelo: Sonnet. Devuelve nota por criterio, nota global y **tres defectos concretos con su ubicación** (cuadro y zona), no elogios.

| Criterio | 10 significa |
|---|---|
| Continuidad del concepto | La transición plano→real no tiene cortes; el dibujo y el mundo son el mismo objeto |
| Cámara y composición | Entra y atraviesa; encuadres con intención; sin objetos cortados ni techos que parpadean |
| Materiales y luz | Materiales creíbles a escala, sombras coherentes, sin z-fighting ni texturas estiradas |
| Escala y detalle | Medidas y mobiliario reales; la escena merece su precio (no cajas vacías) |
| Tipografía y HUD | Legible, coherente con la marca, cambia con el scroll, sin tapar lo importante |
| Ritmo | Hay pausas y clímax; ninguna escena se siente rellenada |
| Robustez | Móvil, reduce-motion y alternativa sin WebGL funcionan |

## Comprobaciones objetivas (de `walk-report.json`, no opinión)
- `errors` vacío; `gl.renderer` es GPU, no software, en la máquina de prueba.
- `transferredMB` ≤ 40 en laptop y ≤ 15 en `--mobile`.
- 60 fps sostenidos en el recorrido en un equipo de gama media; si no se puede medir, dilo.

## Ciclo
1. Capturar → 2. Juez puntúa y lista defectos → 3. Corregir solo esos defectos → 4. Repetir hasta ≥ 8 o hasta el tope (3 iteraciones y 60 min por escena por defecto; luego bandeja `pedir` al usuario). Nunca declares aprobado con una nota que no dio el juez.
