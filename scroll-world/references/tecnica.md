# Técnica (reimplementada desde lo que describen el video y el código público; sin copiar)

## 1. Una sola cámara de perspectiva hace toda la página
- Hoja inicial: cámara muy alta, mirando hacia abajo, con **FOV de 2°** → la perspectiva desaparece y el modelo parece un dibujo.
- Al bajar, el lente se abre y la distancia se acorta **a la vez**. Interpola el FOV y el tamaño del encuadre en escala **logarítmica** (`exp(lerp(log a, log b, t))`) para que el tamaño aparente cambie de forma pareja y no haya "salto".
- Parametriza todo con `s` de 0 a 1 (progreso del scroll) en pistas de llaves `[s, valor, easing]`; para caminar usa una curva monótona que no se detenga en seco.
- Distancia = encuadre / (2·tan(fov/2)). Ajusta `near`/`far` según la altura (desde lejos todo es una losa delgada) para no perder precisión de profundidad.

## 2. El dibujo es el modelo
- `renderer.localClippingEnabled = true` y un `THREE.Plane` horizontal a ~1.2 m: lo que queda bajo el plano se ve, lo demás no. **El scroll sube el plano:** así crecen los muros.
- Líneas: `LineSegments2` (grosor en píxeles, no en mundo) con el mismo plano de recorte; el relleno de muros cortados es tinta sólida.
- Papel: un plano enorme del color del fondo, sin tone mapping ni niebla.

## 3. Escena a escena: línea → material
- Cada escena tiene un **frente de barrido** (vector de dirección + uniform) que decide en el shader qué parte ya es material real y cuál sigue en línea; las líneas de esa escena se recortan con un plano que avanza con el mismo frente.
- Progreso de cada escena = función del avance de la cámara hacia su umbral; el barrido empieza al cruzar la puerta.

## 4. Luz y realismo barato
- Sol direccional bajo (tarde), sombras de 4096 estáticas (`shadowMap.autoUpdate=false`, se recalculan al necesitar), hemisferio suave, luces puntuales pequeñas que falsean rebotes y una fría por donde entra el cielo.
- Sombras de contacto como planos con textura bajo cada mueble; texturas PBR CC0 (albedo, normal, rugosidad/AO) a 1k; HDRI solo para el cielo/reflejos.
- Tone mapping ACES; sin fog hasta que la cámara aterriza, luego niebla corta para ocultar el fondo.

## 5. Modo captura y alternativa
- `?capture` desactiva suavizado e intro: el recorrido se reproduce determinista, cuadro a cuadro, para video y para el juez.
- Puerta de capacidad: si no hay WebGL 2 o el equipo es débil, still + clip del recorrido. Presupuesto de referencia: ≈39 MB de texturas laptop, ≈13 MB móvil; usa tex 1k y comprime.
- Móvil: encuadre propio (la hoja es vertical, titular arriba y cajetín abajo), FOV de caminata más abierto (~76°), menos texturas.

## 6. Instrumento que cuenta la historia
HUD con `LENS 2.0° · HEIGHT 1 719 M · CUT +1.20 M` que cambia con el scroll, riel de escenas (01 SHEET, 02 LIFT, 03 FORECOURT, 04 HALL), cajetín de plano con escala y fecha, rótulo por escena con medidas. En cada vertical, traduce esto al instrumento propio (cámara con ISO/mm, GPS y hora, cuenta regresiva, etc.).
