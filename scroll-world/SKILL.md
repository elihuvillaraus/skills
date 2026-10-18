---
name: scroll-world
description: Crea experiencias web guiadas por scroll donde un artefacto plano que el cliente ya conoce (un plano, una postal, un menú, un wireframe, un póster) se vuelve un mundo 3D real que el visitante recorre, sin cortes, con three.js, GSAP ScrollTrigger y Lenis, sin build. Incluye el método (fórmula plano→real, propuesta antes de código, checkpoints, bucle de juez con otro modelo), la técnica de cámara y recorte, un catálogo de verticales y una herramienta para recorrer el sitio, capturar stills y grabar el video del recorrido. Usar cuando pidan una landing 3D/scroll cinematográfica, "tipo Casa Serra / Lintel / Turun", un recorrido virtual, una experiencia inmersiva de marca o el video de ese recorrido para reels y anuncios, en cualquier vertical.
argument-hint: "[vertical o marca] [artefacto plano] [escenas a recorrer]"
---

# scroll-world

Idea de Sam Aing (Casa Serra, Casa Larga, Turun, hechas con Claude Code y Opus 5.5). Sus repos no traen licencia: **no se copia código, se reimplementa**. Lo que sí es público y usable es el método y su prompt de arranque. Detalle de la técnica en `references/tecnica.md`, verticales en `references/verticales.md`, rúbrica del juez en `references/rubrica-juez.md`.

## La fórmula

**[artefacto plano que el cliente del vertical ya conoce] → [el mundo real que representa], recorrido de principio a fin por el scroll, sobre un solo modelo.**

Lo que lo hace funcionar, y no un efecto más:
1. **El artefacto plano no es una imagen: es el mismo modelo 3D** visto con un recorte y un lente larguísimo. El dibujo y el edificio son una sola cosa, por eso la transición no tiene corte.
2. **La cámara entra y atraviesa**, escena tras escena, a la altura de los ojos. No orbita el objeto desde fuera.
3. **Cada escena sigue siendo línea hasta que la cámara llega**; entonces los materiales reales la barren. Siempre hay una promesa pendiente más adelante.
4. **Los detalles del instrumento cuentan la historia** (HUD con lente, altura, corte; cajetín de plano; escala). Son baratos y venden el concepto.

## Cuándo sí y cuándo no

- **Sí:** marca o proyecto cuyo cliente decide con emoción y compara mal (inmobiliaria, turismo, hotel, arquitectura, producto de alto ticket, evento, portafolio) y una pieza capaz de hacerse viral en video.
- **No:** sitios transaccionales, SEO de catálogo, públicos con equipos débiles como único canal. Pesa (≈39 MB de texturas en laptop, ≈13 MB en móvil) y exige WebGL 2. Siempre con alternativa: `still` + clip del recorrido cuando no corra.
- Dos sitios en uno si hace falta: la experiencia como campaña y un sitio normal para SEO y conversión.

## Proceso (cada paso termina con algo que el usuario puede ver)

0. **Puerta `ambicion`** (modo completo): objetivo detrás del objetivo (¿ventas, reservas, un reel viral?), juez externo (estos pasos 4 y la rúbrica), modelo y costo. La meta no es "una página 3D" sino lo que esa página debe lograr.
1. **Brief:** vertical, artefacto plano, 5 escenas (qué hay en cada una), nivel de ambición ("casa de millones, muebles reales, luz de tarde"), marca y voz (`voice-md`, `brand-strategist`). Material real del cliente (medidas, fotos, textos) antes que inventado.
2. **Propuesta sin una línea de código:** layout con medidas que se puedan imaginar y trayectoria de cámara parada por parada, en **2 o 3 direcciones**; el usuario elige (bandeja `pedir` si no está presente). La última parte del prompt original importa tanto como la idea: sin ella sale una página terminada que no reconoces.
3. **Checkpoints, uno a la vez.** CP1: hoja plana, muros que suben, entrada a la primera escena. Grábalo y muéstralo antes de seguir: `node tools/walk.mjs <url> out --stops 12 --video`.
4. **Bucle del juez:** puntúa cada escena de 0 a 10 con la rúbrica y itera hasta 8 o más. **El juez no es quien programa:** un subagente distinto, sin el contexto del proyecto, con las capturas. Sin juez, el modelo da por terminado en 5-10 minutos un arreglo superficial; con juez trabaja más de una hora en una sola escena. Fija tope de tiempo e iteraciones.
5. **Resto de escenas**, una por checkpoint, con el mismo bucle.
6. **Cierre técnico:** alternativa sin WebGL (still + clip), móvil con encuadre propio (vertical, lente más abierto), presupuesto de peso, accesibilidad (reduce-motion, contenido real en HTML para SEO y lectores), `walk-report.json` sin errores.
7. **Entrega:** sitio, `walk.mp4` del recorrido, prompt reutilizable para el siguiente vertical y ficha de qué dijo el juez. Para reels y anuncios derivados: `animate`, `hyperframes-helper` (cortes, subtítulos) y `marcus-audio` (voz y música).

## Honestidad sobre costo y calidad

Un solo prompt de arranque, en sesión limpia, dio en unos 60 minutos un primer checkpoint muy bueno (lo comprobamos recorriendo Casa Larga). La versión viral de Casa Serra tomó unos 70 prompts, dos semanas y cuatro versiones completas. Promete el primero al cliente, presupuesta el segundo.

## Modelos y esfuerzo (sin medir, a validar con un caso real)

Dirección, propuesta, cámara y primera escena: Opus. Escenas repetitivas una vez fijada la arquitectura: Sonnet con `model` explícito. Juez visual: Sonnet con capturas, nunca el mismo hilo que programó. Haiku solo para tareas de lectura (inventario de texturas, pesos).

## Herramienta

`tools/walk.mjs <url> <outDir> [--stops 12] [--video] [--fps 30] [--seconds 40] [--capture] [--mobile]` recorre la página con scroll real, informa GPU/software, errores y MB transferidos, y deja los stills para el juez. `--capture` añade `?capture` a la URL: convención del patrón para quitar suavizado e intro y grabar cuadro a cuadro; la experiencia debe respetarla.

## Reglas

- Texturas CC0 (Poly Haven) y librerías por CDN con versión fija; sin build.
- Geometría en código antes que modelos externos; si el vertical necesita objetos orgánicos (producto, joya), usa GLB propios o fotos con licencia, y di cuál.
- Cifras, medidas, nombres y lugares: del cliente o marcados `{{por confirmar}}`. No inventes pruebas.
- Marcas ajenas: no usar en la pieza. Casos de clientes de socios: no nombrarlos.
