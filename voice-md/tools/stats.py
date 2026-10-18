#!/usr/bin/env python3
"""Estadísticas de voz de uno o más textos (español), sin red ni dependencias.

Uso: stats.py archivo1.txt [archivo2.txt ...]    (o texto por stdin con "-")
Imprime JSON: longitud de frases, palabras frecuentes, aperturas, emoji, preguntas, tuteo/ustedeo.
"""
import json, re, sys, unicodedata
from collections import Counter

STOP = set("""a al algo ante con como cual cuando de del desde donde el ella ellos en entre era es esa ese eso esta este esto
fue ha han hay la las le les lo los me mi mis muy ni no nos o para pero por porque que se si sin sobre son su sus te tu tus
un una uno unos unas y ya yo""".split())
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")

def words(t):
    return [w for w in re.findall(r"[a-záéíóúñü0-9']+", t.lower())]

def main(paths):
    texts = [sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read() for p in paths]
    text = "\n".join(texts)
    sents = [s.strip() for s in re.split(r"(?<=[.!?…])\s+|\n+", text) if len(words(s)) >= 2]
    lens = [len(words(s)) for s in sents]
    ws = words(text)
    content = Counter(w for w in ws if w not in STOP and len(w) > 3)
    bigrams = Counter(" ".join(p) for p in zip(ws, ws[1:]) if not (p[0] in STOP and p[1] in STOP))
    openers = Counter(" ".join(words(s)[:2]) for s in sents)
    n = max(len(ws), 1)
    tu = sum(ws.count(w) for w in ("tú", "tu", "tus", "te", "puedes", "tienes", "sabes"))
    ud = sum(ws.count(w) for w in ("usted", "ustedes", "puede", "tiene", "sabe", "pueden", "tienen"))
    print(json.dumps({
        "palabras": len(ws),
        "frases": len(sents),
        "palabras_por_frase_media": round(sum(lens) / max(len(lens), 1), 1),
        "frase_mas_larga": max(lens, default=0),
        "preguntas_pct": round(100 * sum("?" in s for s in sents) / max(len(sents), 1), 1),
        "exclamaciones_pct": round(100 * sum("!" in s for s in sents) / max(len(sents), 1), 1),
        "emoji_por_1000_palabras": round(1000 * len(EMOJI.findall(text)) / n, 1),
        "yo_nosotros_pct": round(100 * sum(ws.count(w) for w in ("yo", "mi", "me", "nosotros", "nuestro", "nuestra")) / n, 2),
        "trato": {"tu": tu, "usted": ud},
        "palabras_frecuentes": content.most_common(25),
        "bigramas_frecuentes": [b for b in bigramas_top(bigrams)],
        "aperturas_frecuentes": [o for o in openers.most_common(8) if o[1] > 1],
    }, ensure_ascii=False, indent=2))

def bigramas_top(c):
    return [x for x in c.most_common(15) if x[1] > 1]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
