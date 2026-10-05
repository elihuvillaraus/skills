# Which engine to use: local or Gemini

This machine runs both. The saved default is `WATCH_ENGINE=local`, so nothing leaves the computer unless a run asks for `--engine gemini`. Pick per run; never rely on `auto` (it would send every video to Google as soon as a key exists).

## The difference in one line

- **local**: `ffmpeg` pulls frames, captions or Whisper give the transcript, and **you** look at the frames. First-hand, reproducible evidence; nothing is uploaded.
- **gemini**: Google's model watches the picture **and** the audio and `/watch` relays its text answer. Second-hand: you never see a frame. The video (or its URL) goes to Google.

## Decide in this order

1. **Is the video confidential?** Client demos (Telmex and similar), unreleased product, anything with personal data, or anything you are unsure about: **local, always.** The key in `hostings/.env.local` should be treated as **free tier** unless billing is confirmed in AI Studio; on the free tier Google may use submitted content to improve its products and human reviewers may read it. Only a paid-tier key lifts that, and even then prefer local for client material.
2. **Is it a public YouTube video, long (over ~10 min), or a "find the moment / summarize / why does the hook work" question?** **gemini.** No download needed, handles up to about 1 to 3 hours, and costs you only the text of the answer.
3. **Does the question depend on sound** (music, tone, sound design, mix, whether narration matches the picture)? **gemini** for public material. Local only hears speech.
4. **Does the question depend on exact pixels** (a typo in a title card, text legibility, a black frame, brand colors, layout of our own render)? **local**, at `--resolution 1024`, with `--timestamps` for the frames that matter. Gemini samples about 1 frame per second and can miss fast changes.
5. **Otherwise:** local (cheaper to trust, easier to audit).

## Use case table

| Case | Engine | Notes |
|---|---|---|
| Client or unreleased video | local | `--engine local`; never gemini |
| Our own HyperFrames render (QA) | local | `--detail balanced --resolution 1024`; add `--timestamps` for critical frames |
| Public YouTube analysis, hooks, competitors | gemini | pass `--start/--end` for long videos; ask for MM:SS citations |
| Reference reel for `motion-showreel` | gemini for sound and style, `analyze-reference.mjs` for BPM and cut timing | Gemini misjudged a 120 BPM click as "about 60 BPM" in our test; never trust it for tempo |
| Spanish video of ours, no captions | local (WhisperX, `es` hint is saved) | brand names can come out wrong ("Sellia" became "Celia"); proofread them |
| Need word-level timing of speech | `npx hyperframes transcribe` | local WhisperX returned one coarse segment for a 33 s clip |
| Agent or model that cannot read images | gemini only | not verified for Copilot or OpenCode models; check first |
| Gemini returns 429 or any failure | local if the video is not confidential | never switch silently when a person is present: say what failed and offer local |
| Unattended or scheduled run | same rules; nobody can approve an upload | confidential: local only. Public and Gemini fails: rerun local automatically |

## Agents

- **Claude Code (Opus or Sonnet):** both engines work. Local costs context (about 200 tokens per 512 px frame, so about 20k for 100 frames; an estimate), Gemini costs almost none. Prefer Gemini for long public videos, local for anything visual or private.
- **Codex and ChatGPT Work:** need network access enabled (`[sandbox_workspace_write] network_access = true`) for downloads and for Gemini.
- **Claude Chat and Cowork:** not supported by this skill.
- **Copilot CLI, OpenCode, Gemini CLI:** untested here. Our `gemini` CLI login currently fails with a 403 license error, so it cannot replace the API key.

## Measured on this machine (2026-10-05, M-series Mac)

| Run | Time | Result |
|---|---|---|
| local, 33 s Spanish video, frames only | 1.4 s | 16 frames at 512 px, on-screen text legible, no voice |
| local + WhisperX (`es`) on the same video | 10 s | very good Spanish transcript; one segment; "Celia" for "Sellia" |
| local, YouTube 1-min window | 9.5 s | title and channel metadata, 17 keyframes, 65 caption segments with fine timestamps |
| gemini, 8 s synthetic file upload | 9.8 s | 2.5k Google tokens; tempo wrong by 2x |
| gemini, same YouTube minute | 10.6 s | 6.7k Google tokens; detailed visual and spoken breakdown with timestamps; did not know the video title |

One-time cost of the local engine: about 1 GB for WhisperX under `~/.cache/watch`, plus `yt-dlp` and `deno` from Homebrew (keep `yt-dlp` current: `brew upgrade yt-dlp`; a YouTube 403 is almost always an outdated `yt-dlp`).

## Commands

```bash
RUN=~/.agents/skills/watch/scripts/run.sh
$RUN watch "<url-or-file>" --question "<question>"                       # local (default)
$RUN watch "<youtube-url>" --engine gemini --question "<question>" --start 2:15 --end 4:00
$RUN watch "<file>" --engine local --detail balanced --resolution 1024 --timestamps 0:12,0:30
WATCH_WHISPERX_LANGUAGE=en $RUN watch "<english-file>"                  # override the saved "es" hint
$RUN setup --json                                                        # health check
```

`run.sh` loads only the `GEMINI_API_KEY` line from `/Users/elihuvillaraus/Docs/Sites/MarketINC/hostings/.env.local` (override with `WATCH_KEY_FILE`). That file also holds mail, WHM, restic and Stalwart secrets, so never `source` it and never print the key.
