#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DUMP_DIR="$PROJECT_DIR/dump"
OUT_FILE="${1:-$DUMP_DIR/odoo_backup_$(date +%Y%m%d_%H%M%S).dump}"

if docker compose version >/dev/null 2>&1; then
	DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
	DC=(docker-compose)
else
	echo "Error: neither 'docker compose' nor 'docker-compose' is available."
	exit 1
fi

cd "$PROJECT_DIR"
mkdir -p "$DUMP_DIR"

echo "Starting db container..."
"${DC[@]}" up -d db

echo "Exporting database to: $OUT_FILE"
"${DC[@]}" exec -T db pg_dump -U odoo -d postgres -Fc > "$OUT_FILE"

echo "Done. Backup file: $OUT_FILE"