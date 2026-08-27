#!/usr/bin/env bash
# Uso: ./mergear.sh <pasta-com-videos>
# Junta vídeos+áudio órfãos do gallery-dl (formato DASH).

set -e

export PATH="$HOME/Library/Python/3.9/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
FFMPEG="$(command -v ffmpeg || true)"

if [ -z "$1" ]; then
  echo "Uso: $0 <pasta-com-videos>"
  exit 1
fi

if [ -z "$FFMPEG" ]; then
  echo "ffmpeg não encontrado. Rode verificar-deps.sh" >&2
  exit 1
fi

cd "$1"
shopt -s nullglob
count=0
for v in *v.mp4; do
  id=$(echo "$v" | sed 's/v\.mp4$//')
  audio=$(ls "${id}"*a.m4a 2>/dev/null | head -1)
  if [ -n "$audio" ]; then
    "$FFMPEG" -hide_banner -loglevel error -y -i "$v" -i "$audio" -c copy "${id}.mp4" </dev/null
    rm "$v" "$audio"
    echo "Merged: ${id}.mp4"
    count=$((count+1))
  fi
done
echo "Total mergeado: $count"
