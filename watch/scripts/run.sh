#!/usr/bin/env bash
# Run the watch scripts with the Gemini key loaded from the MarketINC hostings env file.
# Reads ONLY the GEMINI_API_KEY line: that file also holds SMTP, WHM, restic and Stalwart
# secrets, which must never reach yt-dlp, ffmpeg, or any subprocess. An already exported
# GEMINI_API_KEY wins; override the file with WATCH_KEY_FILE.
#
#   run.sh watch  <url-or-path> --question "..." [--engine local|gemini] [other watch.py flags]
#   run.sh setup  --json | --check | --engine local | --backend whisperx --detail balanced
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
KEY_FILE="${WATCH_KEY_FILE:-/Users/elihuvillaraus/Docs/Sites/MarketINC/hostings/.env.local}"

if [ -z "${GEMINI_API_KEY:-}" ] && [ -f "$KEY_FILE" ]; then
  line="$(grep -E '^[[:space:]]*(export[[:space:]]+)?GEMINI_API_KEY=' "$KEY_FILE" | tail -1 || true)"
  if [ -n "$line" ]; then
    value="${line#*=}"
    value="${value%$'\r'}"
    value="${value#\"}"; value="${value%\"}"
    value="${value#\'}"; value="${value%\'}"
    if [ -n "$value" ]; then export GEMINI_API_KEY="$value"; fi
  fi
fi

target="${1:-}"
case "$target" in
  watch|setup) shift ;;
  *) echo "usage: run.sh watch|setup [args]" >&2; exit 2 ;;
esac
exec python3 "$DIR/$target.py" "$@"
