---
name: voice-md
description: Genera el voice.md (ficha de voz) de una marca o persona a partir de muestras reales (reels, captions, correos, textos del sitio), no de adivinanzas. Mide estilo con un script local sin costo de modelo, redacta la ficha en español con citas como evidencia, la confirma con el usuario y la deja lista para las skills ig-* (instagram-agent-skill), copywriting, content-creator y cualquier guion. Usar cuando pidan "voice.md", "tono de marca", "ficha de voz", "que suene como yo/nosotros", o antes de escribir contenido en serie para MarketINC, ChatIA, TRUTH u otra marca.
argument-hint: "[marca o persona] [archivos, URLs o textos de muestra]"
---

# voice-md

Produce un `voice.md` por marca. Una ficha vacía o inventada hace que todo lo que se escriba después suene genérico; esta skill la construye desde lo que la marca ya dijo.

## Dónde vive

- Ficha de cada marca: `~/.claude/voices/<slug>.md` (slug en minúsculas: `marketinc`, `chatia`, `truth`).
- Las skills `ig-*` leen un solo archivo, `~/.claude/instagram/voice.md`. `activar` lo apunta a la marca con la que se trabaja (symlink; si existe un archivo real ahí, no lo borres: muestra su contenido y pregunta).

## Proceso

1. **Intake mínimo.** Pregunta solo lo que falte: marca/persona, handle, a quién le habla (concreto), qué vende, canal principal. Si el proyecto ya tiene `AGENTS.md`, brand book o memoria de la marca, léelos antes de preguntar.
2. **Muestras.** Pide 3 a 10 piezas que suenen más a la marca. Acepta archivos, texto pegado o URLs (páginas con el navegador; videos y reels con la skill `watch` para obtener la transcripción). Menos de 3 piezas: avisa que la ficha saldrá débil y márcala `borrador`.
3. **Medir (sin costo de modelo).** Junta las muestras en archivos de texto y corre:
   `python3 -I <esta-skill>/tools/stats.py muestra1.txt muestra2.txt`
   Da largo de frase, preguntas/exclamaciones, emoji, trato tú/usted, palabras y bigramas frecuentes, aperturas repetidas. Úsalo como evidencia de "palabras que uso" y "ritmo", no como veredicto.
4. **Redactar** con las secciones de abajo. Regla de oro: cada afirmación sobre el estilo lleva una cita corta de una muestra o una cifra del script. Lo que no esté respaldado se marca `por confirmar`.
5. **Prueba de oído.** Escribe 3 líneas en esa voz y 3 que suenen genéricas sobre el mismo tema. El usuario dice cuáles son suyas; ajusta la ficha con la respuesta.
6. **Guardar.** Escribe `~/.claude/voices/<slug>.md` (con `estado: confirmada` solo si el usuario la aprobó) y ofrece `activar`. Registra en el backlog si quedan campos `por confirmar`.

## Estructura de la ficha

Mantén los encabezados de la plantilla de instagram-agent-skill para que esas skills la lean sin cambios, y añade los bloques marcados con (+).

```
---
marca: <nombre>
estado: borrador | confirmada
fecha: <YYYY-MM-DD>
muestras: <n> (<de dónde>)
---
# voice.md · <marca>

## Who I am            (nombre, handle, qué hago en una frase, a quién le hablo, qué vendo)
## What I sound like   (3 muestras textuales; en cámara soy…; palabras que uso; palabras que nunca diría;
                        groserías; emoji; cara en cámara; voz en off o a cámara; ritmo en palabras por minuto)
## My positions        (3 a 5 creencias propias, de las muestras o confirmadas)
## Off limits          (temas, clientes o cifras que no se mencionan, afirmaciones prohibidas)
## Proof I can use     (solo cifras e historias que el usuario dio o que están en documentos suyos)
## The ask             (CTA de una palabra, a dónde lleva, enlace)
## (+) Ritmo y forma    (largo medio de frase, preguntas %, apertura típica, trato tú/usted, números del script)
## (+) Ejemplos buenos / malos (las líneas de la prueba de oído, con la razón)
## (+) Por confirmar    (lista de campos sin respaldo)
```

## Reglas

- Nunca inventes pruebas ni cifras. Si "Proof I can use" no tiene fuente, déjala vacía con `{{tu cifra}}`.
- Respeta lo que ya está decidido por marca: p. ej. se promueven las plataformas propias con cifras, pero no se nombran clientes de socios (ej. Telmex vía HITSS). Revisa la memoria del proyecto antes de llenar "Off limits".
- Español por defecto, con el registro (tú/usted, mexicano/neutro) que midan las muestras. El léxico anti-"slop" de ig-human es inglés: no lo apliques a esta voz.
- La ficha describe cómo suena la marca; no la reescribas más pulida de lo que es. Si las muestras tienen muletillas útiles, consérvalas.
- Una ficha por marca. No mezcles la voz de la persona con la de la empresa: si hay ambas, haz dos archivos y que uno referencie al otro.
