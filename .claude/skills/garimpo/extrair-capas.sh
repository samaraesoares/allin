#!/usr/bin/env bash
# Uso: ./extrair-capas.sh "/caminho/da/pasta-com-videos" [idioma]
# Idioma: pt (default), en, es, fr, etc. Use "auto" pra deixar Whisper detectar.
# Pra cada vídeo: extrai prints (1 frame a cada 0.5s) + transcreve (openai-whisper).
# Headlines são geradas pelo Claude depois, lendo os .txt.

set -e

# ffmpeg precisa estar no PATH pro whisper extrair áudio.
# Resolve as ferramentas independente de onde foram instaladas (pip --user, homebrew, ~/.local/bin).
export PATH="$HOME/Library/Python/3.9/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
FFMPEG="$(command -v ffmpeg || true)"
WHISPER="$(command -v whisper || true)"

if [ -z "$FFMPEG" ] || [ -z "$WHISPER" ]; then
  echo "Faltam ferramentas (ffmpeg e/ou whisper). Rode: $(dirname "${BASH_SOURCE[0]}")/verificar-deps.sh" >&2
  exit 1
fi

if [ -z "$1" ]; then
  echo "Uso: $0 \"/caminho/da/pasta-com-videos\""
  exit 1
fi

PASTA="$1"
IDIOMA="${2:-pt}"
[ -d "$PASTA" ] || { echo "Pasta não existe: $PASTA"; exit 1; }

PRINTS_DIR="${PASTA}/prints"
TRANSC_DIR="${PASTA}/transcricoes"
HEAD_DIR="${PASTA}/headlines"
mkdir -p "$PRINTS_DIR" "$TRANSC_DIR" "$HEAD_DIR"

shopt -s nocaseglob nullglob
total=0
for v in "$PASTA"/*.mp4 "$PASTA"/*.mov "$PASTA"/*.webm "$PASTA"/*.mkv "$PASTA"/*.m4v; do
  [ -f "$v" ] || continue
  base=$(basename "$v")
  base="${base%.*}"

  # 1. Prints a cada 0.5s
  VPRINTS="${PRINTS_DIR}/${base}"
  mkdir -p "$VPRINTS"
  echo "[$base] extraindo prints..."
  "$FFMPEG" -hide_banner -loglevel error -i "$v" -vf "fps=2" -q:v 2 "$VPRINTS/%03d.jpg" </dev/null
  pcount=$(ls "$VPRINTS"/*.jpg 2>/dev/null | wc -l | tr -d ' ')
  echo "[$base]   → $pcount prints"

  # 2. Transcrição (PT-BR, modelo small via openai-whisper)
  if [ -s "$TRANSC_DIR/${base}.txt" ]; then
    echo "[$base] transcrição já existe, pulando"
  else
    echo "[$base] transcrevendo (whisper small, idioma=$IDIOMA)..."
    WARGS=("$v" --model small --output_dir "$TRANSC_DIR" --output_format txt --verbose False)
    [ "$IDIOMA" != "auto" ] && WARGS+=(--language "$IDIOMA")
    "$WHISPER" "${WARGS[@]}" 2>&1 | tail -3
    if [ -s "$TRANSC_DIR/${base}.txt" ]; then
      preview=$(head -c 80 "$TRANSC_DIR/${base}.txt")
      echo "[$base]   → \"${preview}...\""
    elif [ -f "$TRANSC_DIR/${base}.txt" ]; then
      echo "[$base]   ⚠ áudio sem fala detectada (instrumental/música) — txt vazio"
    else
      echo "[$base]   ✗ falhou transcrição"
    fi
  fi

  total=$((total + 1))
done

echo
echo "Concluído. $total vídeos processados."
echo "  Prints:        $PRINTS_DIR/"
echo "  Transcrições:  $TRANSC_DIR/  (vazio = vídeo instrumental)"
echo "  Headlines:     $HEAD_DIR/    (Claude gera depois, lendo os .txt)"
