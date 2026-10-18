# Verticales: de qué artefacto plano partir

Elige el artefacto que **el cliente de ese vertical ya reconoce** y que sea una proyección real del objeto. Prioridad en la primera columna según facilidad de reutilizar la técnica (A = casi directo, B = requiere modelar objetos, C = idea a validar).

| | Vertical | Artefacto plano | Se vuelve | Recorrido | Cierre / CTA |
|---|---|---|---|---|---|
| A | Arquitectura, inmobiliaria, remodelación | plano de planta a escala | la casa habitable | puerta → sala → cocina → patio → recámara | agendar visita |
| A | Turismo y experiencias | postal fotográfica sobre la arena | el paisaje en 3D (Turun, Kelingking) | descenso por horarios, reserva por mañana | reservar fecha |
| A | Hotel, restaurante, eventos y bodas | menú, invitación o croquis de mesas | el salón con luz de la noche | llegada → salón → mesa → terraza | cotizar fecha |
| A | Museo, galería, cultura | cartel de la exposición | las salas | sala por sala con la obra | comprar boleto |
| A | Portafolio de estudio o creador | fachada abstracta plana | pabellón con sala por proyecto | una sala por caso | contacto |
| B | Automotriz y movilidad | blueprint técnico del vehículo | el auto a escala real, interior | exterior → cabina → motor | prueba de manejo |
| B | Joyería, relojería, producto de alto ticket | dibujo de patente o despiece | la pieza armándose | componente por componente | ver en tienda |
| B | Manufactura, logística, planta | plano CAD o mapa de rutas | la planta o almacén operando | flujo de materia, estación por estación | demo con datos del cliente |
| B | Moda y retail | patrón de costura | prenda y boutique | tela → corte → prenda → vitrina | comprar o reservar |
| B | Agro, vino, hospitalidad rural | plano catastral o mapa de parcelas | viñedo/campo en la estación | parcela → bodega → mesa | reservar cata |
| C | SaaS y fintech | wireframe del producto | el producto vivo, con datos reales | pantalla → flujo → resultado | probar gratis |
| C | Educación y capacitación | mapa o diagrama del temario | un mundo explorable | módulo = sala | inscribirse |
| C | Salud y bienestar | planta de la clínica o diagrama del proceso | la clínica y la experiencia del paciente | recepción → consulta → tratamiento | agendar cita |
| C | MarketINC / TRUTH / ChatIA (ideas a validar) | contrato o conversación impresa | el mismo documento revelando lo que oculta (fraude, decisión) | cláusula → señal → desenlace | solicitar demo |

## Cómo adaptar el starter prompt (en `[corchetes]`)
```
I want to build a scroll-driven landing page for [VERTICAL / MARCA].

The idea: the page opens on [ARTEFACTO PLANO], flat, printed, nothing looks 3D. When the visitor scrolls, [CÓMO SE LEVANTA]; the camera comes down to [PUNTO DE ENTRADA] and travels through [ESCENAS EN ORDEN] at eye height. Each scene stays a line drawing until the camera gets there, then the real materials sweep across it.

What I care about:
- The flat artifact is not a picture. It is the real 3D model, cut/flattened by [MECANISMO: corte a 1.2 m + lente largo]. The drawing and the world are the same thing.
- The camera travels deep into the space, scene after scene. It never orbits from outside.
- It should feel like [NIVEL DE AMBICIÓN: materiales, luz, escala].
- three.js, GSAP ScrollTrigger and Lenis, plain files, no build step. Free CC0 materials.

Before you write any code, propose the layout with sizes I can picture and the camera path stop by stop. Give me two or three directions to choose from and wait for my answer. Then build in checkpoints. First checkpoint only: the flat sheet, the lift, and the entry to the first scene. Record it and show me before you go further.
```
Fuente del prompt base: https://sam1983aing.github.io/casa-serra/prompt/ (publicado por su autor como punto de partida).
