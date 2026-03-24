#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IN_FILE="${1:-}"
DUMP_DIR="$PROJECT_DIR/dump"

if docker compose version >/dev/null 2>&1; then
  DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  DC=(docker-compose)
else
  echo "Error: neither 'docker compose' nor 'docker-compose' is available."
  exit 1
fi

if [[ -z "$IN_FILE" ]]; then
  if [[ -d "$DUMP_DIR" ]]; then
    IN_FILE="$(ls -1t "$DUMP_DIR"/odoo_backup_*.dump 2>/dev/null | head -n 1 || true)"
  fi
  if [[ -z "$IN_FILE" ]]; then
    echo "No backup provided and no dump found in $DUMP_DIR"
    exit 1
  fi
fi

if [[ ! -f "$IN_FILE" ]]; then
  echo "File not found: $IN_FILE"
  exit 1
fi

cd "$PROJECT_DIR"

echo "Starting db container..."
"${DC[@]}" up -d db

echo "Recreating database..."
"${DC[@]}" exec -T db dropdb -U odoo --if-exists postgres
"${DC[@]}" exec -T db createdb -U odoo postgres

echo "Restoring from: $IN_FILE"
"${DC[@]}" exec -T db pg_restore -U odoo -d postgres --no-owner --clean < "$IN_FILE"

echo "Starting full stack..."
"${DC[@]}" up -d

echo "Done. Database imported."