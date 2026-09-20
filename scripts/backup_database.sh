#!/bin/sh
set -eu

DATABASE_PATH="${DATABASE_PATH:-meal_planner.db}"
BACKUP_DIR="${BACKUP_DIR:-backups}"

if [ ! -f "$DATABASE_PATH" ]; then
    printf 'Database not found: %s\n' "$DATABASE_PATH" >&2
    exit 1
fi

mkdir -p "$BACKUP_DIR"
BACKUP_PATH="$BACKUP_DIR/meal_planner-$(date +%Y%m%d-%H%M%S).db"
cp "$DATABASE_PATH" "$BACKUP_PATH"
printf 'Backup created: %s\n' "$BACKUP_PATH"
