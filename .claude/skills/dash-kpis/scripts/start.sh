#!/usr/bin/env bash
# Abre o painel do negócio no navegador. Não precisa instalar nada.
cd "$(dirname "$0")" || exit 1
PY=$(command -v python3 || command -v python)
if [ -z "$PY" ]; then
  echo "Python 3 não encontrado."
  echo "Mac: rode 'xcode-select --install' no terminal."
  echo "Windows: instale em python.org (marque 'Add Python to PATH')."
  exit 1
fi
exec "$PY" server.py "$@"
