# Cartesia TTS — reference

Base URL: `https://api.cartesia.ai`. Auth: `X-API-Key: ${CARTESIA_API_KEY}` header (not `Authorization: Bearer` — Cartesia's own convention, different from the KIE gateway). Every request also needs `Cartesia-Version: 2026-03-01` (a date-stamped API version header, bumped from the older `2024-11-13` — re-verified working via `GET /voices/{id}` on 2026-07-20. If requests start failing with a version-mismatch error, check `https://docs.cartesia.ai` for the current date string and bump it).

## Non-streaming synthesis (the common case)

```
POST /tts/bytes
```

Request body:
```json
{
  "model_id": "sonic-3.5",
  "transcript": "Texto a narrar.",
  "voice": { "mode": "id", "id": "<voice-uuid>" },
  "output_format": { "container": "mp3", "bit_rate": 128000, "sample_rate": 44100 },
  "language": "es",
  "generation_config": { "speed": 1, "volume": 1 }
}
```

Response: raw audio bytes with `Content-Type: audio/mpeg` (for mp3) — write directly to a file with `curl -o out.mp3`, there is no JSON envelope to unwrap on success.

### `model_id`
- `sonic-3.5` — current default (re-verified by user 2026-07-20). Good default for narration.
- `sonic-2` — older tier, still functional, kept here only as a fallback if `sonic-3.5` ever 404s.
- Check `https://docs.cartesia.ai/api-reference/tts/bytes` for newer model IDs (Cartesia ships new `sonic-*` generations periodically).

### `voice`
`{ "mode": "id", "id": "<uuid>" }` — pick from Cartesia's voice catalog. Two standardized `es-MX` voices, confirmed via `GET /voices/{id}` on 2026-07-20:

| Name | id | gender | notes |
|---|---|---|---|
| Daniela – Relaxed Woman | `5c5ad5e7-1020-476b-8b91-fdcbe9cc313c` | feminine | Default. "Calm and trusting Mexican accented female for natural conversations." Zeus tutorial narration standard since 2026-07-08. |
| Pedro – Formal Speaker | `15d0c2e2-8d29-44c3-be23-d585d5f154a1` | masculine | "Formal and steady Mexican adult for clear and concise exchanges of information." Use when the script/persona calls for a male voice. |

- To find other voices: `GET /voices` (list) and `GET /voices/{id}` (detail — includes `name`, `description`, `gender`, `language`, `country`, and a preview audio URL). List first, don't guess IDs.
- Cartesia also supports voice cloning (`mode: "clone"` style requests with an uploaded audio sample) for a custom/brand voice — only reach for this if the user explicitly wants a cloned voice; it's a materially different, higher-effort request shape than picking a catalog voice.

### `output_format`
- `{ "container": "mp3", "bit_rate": 128000, "sample_rate": 44100 }` — safe default for narration mixed under video; small file size, universally playable.
- `{ "container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100 }` — lossless 16-bit, smaller than `pcm_f32le`; good default when a lossless WAV is needed.
- `{ "container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100 }` — lossless 32-bit float, larger files; only if downstream processing (further mixing/mastering) specifically needs float precision.

### `language`
- ISO 639-1 code (`"es"`, `"en"`, etc.) — must match the voice's actual language for natural prosody. Mismatching language and voice (e.g. `language: "en"` on a Spanish-native voice) produces accented, unnatural output.

### `generation_config`
- `{ "speed": 1, "volume": 1 }` — neutral defaults (1.0 = normal), introduced with `sonic-3.5`.
- `speed`: e.g. `0.9` for a slightly slower, more measured read; `1.1` for a slightly faster, more conversational one. Prefer this over rewriting punctuation when only pacing needs to change.
- `volume`: only adjust if downstream mixing needs a pre-attenuated clip; otherwise leave at `1`.

## Version history

- **2026-07-20**: bumped default `model_id` `sonic-2` → `sonic-3.5` and `Cartesia-Version` `2024-11-13` → `2026-03-01` (user-provided curl, re-verified via a live `GET /voices/{id}` call). Added `generation_config` (new in `sonic-3.5`) and the second catalog voice (Pedro, masculine).

## Streaming synthesis (lower first-byte latency)

```
POST /tts/sse
```
Server-sent-events variant of the same request body — returns audio in chunks as it's generated rather than waiting for the full clip. Only reach for this if you're building a live/interactive narration path; for pre-rendering video narration (the common case in this skill), `/tts/bytes` is simpler and sufficient.

## Batching multiple lines — use a Python driver, not nested bash

Nesting a `python3 -c "..."` JSON-builder inside a bash script's `curl -d "$(...)"` breaks on quoting once your payload has literal `{`/`}` characters colliding with the outer shell's own quoting. Write a standalone script instead:

```python
import json, os, subprocess

ENV_FILE = "/Users/elihuvillaraus/Docs/SaaS/ai-content-machine/marcus/frontend/.env.local"
api_key = None
with open(ENV_FILE) as f:
    for line in f:
        if line.startswith("CARTESIA_API_KEY="):
            api_key = line.strip().split("=", 1)[1]
            break

VOICE_ID = "5c5ad5e7-1020-476b-8b91-fdcbe9cc313c"
lines = [
    {"id": "scene-01", "text": "Primera línea del guion."},
    {"id": "scene-02", "text": "Segunda línea del guion."},
]

for line in lines:
    payload = {
        "model_id": "sonic-3.5",
        "transcript": line["text"],
        "voice": {"mode": "id", "id": VOICE_ID},
        "output_format": {"container": "mp3", "bit_rate": 128000, "sample_rate": 44100},
        "language": "es",
        "generation_config": {"speed": 1, "volume": 1},
    }
    out_path = f"{line['id']}.mp3"
    cmd = [
        "curl", "-s", "-X", "POST", "https://api.cartesia.ai/tts/bytes",
        "-H", f"X-API-Key: {api_key}",
        "-H", "Cartesia-Version: 2026-03-01",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
        "-o", out_path,
        "-w", "%{http_code} %{size_download}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"{line['id']}: {result.stdout.strip()}")
```

This is the exact pattern used to generate all 12 narration lines for the two Zeus tutorial videos (2026-07-08) — copy it directly rather than re-deriving the quoting from scratch.

## Pacing / delivery control

Cartesia's `sonic-3.5` model reads punctuation for natural pauses — use full stops, commas, and em-dashes deliberately in the `transcript` to shape pacing rather than looking for an SSML-style rate parameter (there isn't one on the `/tts/bytes` endpoint as of 2026-07; `generation_config.speed` is a blunter, clip-wide alternative — see above). Short sentences separated by periods read as more measured/confident; long comma-joined sentences read faster and more conversational. For a tutorial VO, prefer the former.
