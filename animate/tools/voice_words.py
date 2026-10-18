#!/usr/bin/env python3
"""Word timings for a voice-over, read from the audio itself (faster-whisper, local, no API).
   usage: python tools/voice_words.py <voice.wav> [--model small.en]
   prints JSON: [{"w": "word", "t0": 1.23, "t1": 1.51}, ...]
Called by tools/voice.mjs; it falls back to an estimate when faster-whisper isn't installed (pip install faster-whisper)."""
import json
import sys


def main():
    args = sys.argv[1:]
    model = 'small.en'
    lang = 'en'
    if '--lang' in args:
        i = args.index('--lang')
        lang = args[i + 1]
        del args[i:i + 2]
    if '--model' in args:
        i = args.index('--model')
        model = args[i + 1]
        del args[i:i + 2]
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device='cpu', compute_type='int8')
    # decode with ffmpeg (16 kHz mono float) so PyAV's version never matters
    import subprocess, numpy as np
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', args[0], '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    segs, _ = m.transcribe(audio, word_timestamps=True, vad_filter=False, beam_size=5, language=lang)
    out = []
    for s in segs:
        for w in s.words or []:
            out.append({'w': w.word.strip(), 't0': round(w.start, 3), 't1': round(w.end, 3)})
    print(json.dumps(out))


if __name__ == '__main__':
    main()
