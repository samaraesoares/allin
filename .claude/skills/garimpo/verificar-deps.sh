#!/usr/bin/env bash
# Verifica se as ferramentas necessárias estão instaladas (Mac e Linux).

# Resolve as ferramentas independente de onde foram instaladas (pip --user, homebrew, ~/.local/bin).
export PATH="$HOME/Library/Python/3.9/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
FIREFOX="/Applications/Firefox.app/Contents/MacOS/firefox"
[ -x "$FIREFOX" ] || FIREFOX="$(command -v firefox || true)"

faltam=()
command -v gallery-dl >/dev/null && echo "OK gallery-dl"     || { echo "FALTA gallery-dl";     faltam+=("pip3 install --user --upgrade gallery-dl"); }
command -v yt-dlp     >/dev/null && echo "OK yt-dlp"         || { echo "FALTA yt-dlp";         faltam+=("pip3 install --user --upgrade yt-dlp"); }
command -v whisper    >/dev/null && echo "OK openai-whisper" || { echo "FALTA openai-whisper"; faltam+=("pip3 install --user --upgrade openai-whisper"); }
command -v ffmpeg     >/dev/null && echo "OK ffmpeg"         || { echo "FALTA ffmpeg";         faltam+=("brew install ffmpeg   (Linux: sudo apt install ffmpeg)"); }
[ -x "$FIREFOX" ]                && echo "OK Firefox"        || { echo "FALTA Firefox";        faltam+=("brew install --cask firefox   (Linux: sudo apt install firefox)"); }
command -v sqlite3    >/dev/null && echo "OK sqlite3"        || { echo "FALTA sqlite3 (vem com o sistema — instale com o gerenciador de pacotes)"; }

if [ ${#faltam[@]} -eq 0 ]; then
  echo
  echo "Tudo instalado."
  exit 0
fi

echo
echo "Pendências:"
for cmd in "${faltam[@]}"; do echo "  $cmd"; done
exit 1
