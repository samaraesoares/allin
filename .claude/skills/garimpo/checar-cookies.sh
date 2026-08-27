#!/usr/bin/env bash
# Verifica se o Firefox tem sessão ativa do Instagram (cookie sessionid).
# Saída: "OK" se tem sessionid, "FALTA_LOGIN" se cookies sem IG, "FALTA_PROFILE" se sem profile.

PROFILES_DIR="$HOME/Library/Application Support/Firefox/Profiles"
[ -d "$PROFILES_DIR" ] || PROFILES_DIR="$HOME/.mozilla/firefox"

PROFILE=$(ls -d "$PROFILES_DIR"/*.default-release 2>/dev/null | head -1)
[ -z "$PROFILE" ] && PROFILE=$(ls -d "$PROFILES_DIR"/*.default 2>/dev/null | head -1)
[ -z "$PROFILE" ] && PROFILE=$(ls -d "$PROFILES_DIR"/*.dev-edition-default 2>/dev/null | head -1)

if [ -z "$PROFILE" ]; then
  echo "FALTA_PROFILE"
  exit 1
fi

DB="$PROFILE/cookies.sqlite"
if [ ! -f "$DB" ]; then
  echo "FALTA_LOGIN"
  exit 1
fi

TMP=$(mktemp -t cookies).sqlite
cp "$DB" "$TMP" 2>/dev/null
[ -f "$DB-wal" ] && cp "$DB-wal" "${TMP}-wal" 2>/dev/null
[ -f "$DB-shm" ] && cp "$DB-shm" "${TMP}-shm" 2>/dev/null

count=$(sqlite3 "$TMP" "SELECT COUNT(*) FROM moz_cookies WHERE host LIKE '%instagram%' AND name='sessionid';" 2>/dev/null)
rm -f "$TMP" "${TMP}-wal" "${TMP}-shm"

if [ "$count" = "1" ]; then
  echo "OK"
  exit 0
fi
echo "FALTA_LOGIN"
exit 1
