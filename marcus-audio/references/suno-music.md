# Suno (via KIE gateway) — music generation reference

Base URL: `${KIE_API_BASE_URL}` (default `https://api.kie.ai`). Auth: `Authorization: Bearer ${KIE_API_KEY}` — the same gateway and credential `cinematic-marcus`/`marcus-images` use for image/video, but music has its **own dedicated endpoint pair**, distinct from the generic `/api/v1/jobs/createTask` used for images/video:

```
POST /api/v1/generate                      — create a music task
GET  /api/v1/generate/record-info?taskId=  — poll status / fetch results
```

## Create task — request shape

```ts
interface KieMusicGenerateRequest {
  prompt: string;
  customMode: boolean;
  instrumental: boolean;
  model: "V4" | "V4_5" | "V4_5PLUS" | "V4_5ALL" | "V5";
  callBackUrl: string;              // REQUIRED — 422s without it, use a placeholder if you have no webhook
  style?: string;                   // customMode: true only
  title?: string;                   // customMode: true only
  vocalGender?: "m" | "f";          // customMode: true only
  negativeTags?: string;            // customMode: true only
  styleWeight?: number;             // customMode: true only
  weirdnessConstraint?: number;     // customMode: true only
  audioWeight?: number;             // customMode: true only
  personaId?: string;               // customMode: true only
}
```

### Simple mode (instrumental bed — the common case for a video background track)

```json
{
  "prompt": "Corporate tech underscore, minimal deep house pulse, soft arpeggios, confident and premium, no vocals, product tutorial background music",
  "customMode": false,
  "instrumental": true,
  "model": "V4_5",
  "callBackUrl": "https://example.com/noop"
}
```
With `customMode: false`, the `prompt` string alone drives genre/mood/instrumentation — write it like a music-supervisor brief (genre, tempo feel, mood, "no vocals" if instrumental, comparison points like "premium, polished, product-launch energy").

### Custom mode (branded / lyrical track)

Set `customMode: true` and add:
- `style` — genre/mood tags, comma-separated (e.g. `"deep house, corporate, minimal, 122bpm"`)
- `title` — a track title (Suno will also auto-generate one if omitted)
- `vocalGender` — `"m"` or `"f"` if the track has vocals
- `negativeTags` — things to avoid (e.g. `"aggressive, distorted, lo-fi"`)
- `styleWeight` / `weirdnessConstraint` / `audioWeight` — advanced Suno knobs (0-1 range) for how strictly to follow the style tags vs. explore, and how much the (optional) audio reference influences the result. Leave unset unless iterating on a track that's landing wrong.
- `personaId` — reuse a previously-generated voice/style persona across tracks for consistency (only relevant across multiple related generations).

### Response
```json
{ "code": 200, "msg": "success", "data": { "taskId": "982e498d6d7f38cbddcd70ff585ad30d" } }
```
`code: 422` with `"msg":"Please enter callBackUrl."` means you omitted `callBackUrl` — always include it even with a throwaway placeholder if you're not wiring a real webhook.

## Poll for completion

```bash
curl -s "${KIE_API_BASE_URL:-https://api.kie.ai}/api/v1/generate/record-info?taskId=${TASK_ID}" \
  -H "Authorization: Bearer ${KIE_API_KEY}"
```

Response once complete:
```json
{
  "code": 200, "msg": "success",
  "data": {
    "taskId": "...",
    "status": "SUCCESS",
    "response": {
      "sunoData": [
        {
          "id": "...", "title": "Glass Protocol",
          "audioUrl": "https://tempfile.aiquickdraw.com/r/....mp3",
          "streamAudioUrl": "https://musicfile.kie.ai/...",
          "imageUrl": "https://musicfile.kie.ai/....jpeg",
          "tags": "deep house, minimal, 122bpm, corporate tech",
          "duration": 173.48
        },
        { "...second variant, same taskId..." }
      ]
    }
  }
}
```

- `status` moves `PENDING` → ... → `SUCCESS` (or a failure state — check `errorMessage` if `code` isn't 200 on a later poll). Generation typically takes **1-3 minutes** for a full track; poll every 10-15s, don't tight-loop.
- **Two variants per task** (`sunoData[0]` and `[1]`) — same prompt, different takes. They can differ meaningfully in tempo emphasis, mix density, and actual rendered duration. Inspect both (`title`, `tags`, `duration`) before picking one; don't hardcode index `0`.
- `duration` is the **full generated track length** (Suno renders complete songs, typically 2-4 minutes, even from an instrumental-bed prompt) — it is NOT your target video length. Always trim with ffmpeg to the length you actually need.
- `audioUrl` / `sourceAudioUrl` point at `tempfile.aiquickdraw.com` — **temporary hosting**, download immediately:
  ```bash
  curl -sL "$AUDIO_URL" -o music-bed-full.mp3
  ```

## Trimming to your video's length

```bash
# trim to N seconds with a 2.5s fade-out so it doesn't cut abruptly
ffmpeg -y -i music-bed-full.mp3 -t <N> -af "afade=t=out:st=<N-2.5>:d=2.5" music-bed.mp3
```

## Model tiers

| model | notes |
|---|---|
| `V4` | oldest/fastest tier, lower fidelity |
| `V4_5` | solid default — good instrumental quality, fast turnaround (verified 2026-07-08) |
| `V4_5PLUS` | higher fidelity variant of V4.5 |
| `V4_5ALL` | broadest style range |
| `V5` | newest/highest-fidelity tier — reach for this when quality matters more than turnaround |

## Webhook callback (only relevant if you wire up `KIE_CALLBACK_SECRET`)

If `NEXT_PUBLIC_APP_URL` and `KIE_CALLBACK_SECRET` are set and you build a real `callBackUrl` (see `getKieCallbackUrl()` pattern in the Marcus app, `lib/services/kie/api-client.ts`), KIE POSTs progress to your webhook instead of requiring polling:

```ts
interface KieMusicCallbackData {
  callbackType: "text" | "first" | "complete";  // only act on "complete"
  task_id: string;
  data: KieMusicTrack[];
}
```
Ignore `"text"`/`"first"` callbacks (intermediate stages); only `"complete"` carries the final `sunoData`-equivalent track list. For one-off skill-driven generation (the common case — an agent generating a background bed for a specific video), polling `record-info` is simpler than standing up a webhook receiver and is the recommended default.
