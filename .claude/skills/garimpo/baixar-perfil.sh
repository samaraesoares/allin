#!/usr/bin/env bash
# Uso: ./baixar-perfil.sh @usuario "<nome-da-pasta>" [limite]
# Baixa posts do perfil, organiza em carrosseis/reels/estaticos.
# Pra reels, já extrai prints (1 frame a cada 0.5s).

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORGANIZAR="$SCRIPT_DIR/organizar.py"

# ffmpeg precisa estar no PATH pro yt-dlp interno do gallery-dl mergear DASH.
# Resolve as ferramentas independente de onde foram instaladas (pip --user, homebrew, ~/.local/bin).
export PATH="$HOME/Library/Python/3.9/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
GDL="$(command -v gallery-dl || true)"
FFMPEG="$(command -v ffmpeg || true)"

if [ -z "$GDL" ] || [ -z "$FFMPEG" ]; then
  echo "Faltam ferramentas (gallery-dl e/ou ffmpeg). Rode: $SCRIPT_DIR/verificar-deps.sh" >&2
  exit 1
fi

if [ -z "$1" ]; then
  echo "Uso: $0 @usuario [\"nome-da-pasta\"] [limite]"
  exit 1
fi

USER="${1#@}"
PASTA="${2:-$USER}"
LIMITE="${3:-}"

# Por padrão os downloads ficam dentro do workspace, em dados/garimpo/
RAIZ="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
DEST_ROOT="${GARIMPO_DEST_ROOT:-$RAIZ/dados/garimpo}"
DEST="${DEST_ROOT}/${PASTA}"
TMP="${DEST}/_raw"
URL="https://www.instagram.com/${USER}/posts/"

# GARIMPO_RESUME=1 mantém o que já foi baixado e deixa o gallery-dl pular existentes
[ "${GARIMPO_RESUME:-0}" = "1" ] || rm -rf "$TMP"
mkdir -p "$TMP"
echo "Baixando posts de @${USER} → $DEST"
echo

# Pacing configurável via env (defaults humanizados pra driblar anti-scraping do IG)
SLEEP_REQUEST="${GARIMPO_SLEEP_REQUEST:-6.0-12.0}"
SLEEP_EXTRACTOR="${GARIMPO_SLEEP_EXTRACTOR:-8.0-15.0}"
SLEEP_DOWNLOAD="${GARIMPO_SLEEP:-2.0-5.0}"

ARGS=(
  --cookies-from-browser firefox
  --sleep-request "$SLEEP_REQUEST"
  --sleep-extractor "$SLEEP_EXTRACTOR"
  --sleep "$SLEEP_DOWNLOAD"
  --sleep-429 60
  --retries 6
  --write-metadata
  -d "$TMP"
)
# --post-range conta POSTS (não arquivos); carrossel de N imagens = 1 post
[ -n "$LIMITE" ] && ARGS+=(--post-range "1-${LIMITE}")

if ! "$GDL" "${ARGS[@]}" "$URL" 2>&1 | grep -v "NotOpenSSLWarning\|warnings.warn"; then
  echo
  echo "Erro no download. Possíveis causas:"
  echo "  - Firefox aberto travando cookies → osascript -e 'tell application \"Firefox\" to quit'"
  echo "  - Sessão expirada → relogar no IG via Firefox"
  exit 1
fi

# Achar pasta onde os arquivos foram parar (gallery-dl/instagram/<user>/)
RAW_USER_DIR=$(find "$TMP" -type d -path "*/instagram/${USER}" 2>/dev/null | head -1)
[ -z "$RAW_USER_DIR" ] && RAW_USER_DIR=$(find "$TMP" -type d -name "$USER" 2>/dev/null | head -1)

if [ -z "$RAW_USER_DIR" ]; then
  echo "Erro: não achei pasta de download em $TMP"
  find "$TMP" -type d | head
  exit 1
fi

echo
echo "Organizando em carrosseis/reels/estaticos..."
python3 "$ORGANIZAR" "$RAW_USER_DIR" "$DEST" "$FFMPEG"

# Limpar tmp
rm -rf "$TMP"
