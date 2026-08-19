# Estructura probada de una propuesta ejecutiva

Generalizada del documento real que le ganó al cliente (TRUTH → HITSS/Telmex,
`docs/sales/telmex/propuesta-zona-oriente.md` en speechlytics). No es la única
estructura válida, pero es la que ya funcionó — úsala como punto de partida y
recorta/agrega secciones según el trato real, no la sigas a ciegas.

## Convención del Markdown fuente

```markdown
## <Cliente> · <Proyecto>

<uno o dos párrafos de contexto libre — se recorta en el render, no aparece
en el documento final; la portada generada lo reemplaza>

---

## 1. Resumen ejecutivo
...
## 2. Alcance del servicio
...
## 3. Operación / funcionamiento diario
...
## 4. Niveles de servicio (SLA)
...
## 5. Modelo económico
...
## 6. Evolución del servicio (roadmap)
...
## 7. Requerimientos (del lado del cliente)
...
## 8. Consideraciones
...
## 9. Confidencialidad, datos y propiedad
...
## 10. Vigencia y aceptación
...

## Anexo A · <título del anexo>
...
## Anexo B · <título del anexo>
...
```

El cuerpo real del documento **empieza en el primer `## N. Título` numerado** —
todo lo anterior es un encabezado libre para quien escribe el Markdown, y el
script lo recorta porque la portada generada ya cubre esa información. Cualquier
`## Anexo X · ...` es candidato a extraerse como documento independiente (con su
propia portada) vía `output.anexos` en `config.json` — útil cuando una sola
sección técnica necesita reenviarse sola (a IT, a un tercero) sin el resto de la
propuesta comercial.

## Qué va en cada sección (la versión que ya convenció a un cliente enterprise)

1. **Resumen ejecutivo** — una promesa concreta en un párrafo, no un mission
   statement. Qué se resuelve, en qué tiempo, con qué garantía. El lector
   ejecutivo decide si sigue leyendo aquí.
2. **Alcance del servicio** — qué se entrega, explícitamente. Mejor una tabla
   de entregables que prosa.
3. **Operación diaria** — cómo funciona en la práctica, con horarios/SLAs
   reales si aplican (turnos, ventanas de procesamiento, etc.).
4. **Niveles de servicio** — tabla de métricas comprometidas, no adjetivos
   ("rápido", "confiable"). Un número o no va.
5. **Modelo económico** — la tabla de precios/volumen. Esta es la sección que
   el cliente va a mirar primero después de la portada; que sea escaneable.
6. **Evolución del servicio** — roadmap corto, qué crece con el tiempo. Señal
   de que esto no es un proyecto de una sola entrega.
7. **Requerimientos** — qué necesita el cliente proveer (accesos, infra,
   contactos, datos). Poner esto explícito evita el "ah, eso no lo teníamos
   contemplado" en semana 3.
8. **Consideraciones** — supuestos, riesgos conocidos, límites del alcance.
   Honestidad aquí ahorra una escalación después.
9. **Confidencialidad, datos y propiedad** — quién es dueño de qué, qué pasa
   con los datos al terminar el contrato. Legal lo va a leer primero que
   nadie más en la organización del cliente.
10. **Vigencia y aceptación** — cuánto dura la oferta, cómo se acepta.

Anexos: cualquier detalle técnico denso (arquitectura, diagramas de conexión,
especificación de un catálogo/dataset) que un lector ejecutivo no necesita para
decidir, pero que el equipo técnico del cliente sí va a auditar — sepáralo del
cuerpo principal así el documento comercial se mantiene legible.

## Tono

Enterprise/ejecutivo significa: frases cortas, cifras con su unidad, sin
adjetivos vacíos ("robusto", "de clase mundial", "innovador"), sin inflar
lo que el producto no hace todavía. Cada afirmación de capacidad debe poder
sostenerse si el cliente pregunta "¿cómo lo prueban?".
