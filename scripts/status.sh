#!/usr/bin/env bash
# Show status of all managed office projects
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="$SCRIPT_DIR/../projects.conf"

if [ ! -f "$CONF" ]; then
  echo "Error: projects.conf not found" >&2
  exit 1
fi

echo "Office Projects Status"
echo "══════════════════════════════════════════"

while IFS= read -r line; do
  # Skip comments and empty lines
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  [[ -z "${line// }" ]] && continue

  # Extract path (strip inline comment)
  project_path="${line%%#*}"
  project_path="${project_path%% *}"
  project_path="${project_path%% }"

  # Expand tilde
  project_path="${project_path/#\~/$HOME}"

  name="$(basename "$project_path")"

  if [ ! -d "$project_path" ]; then
    printf "  %-30s  ⚠  NOT FOUND\n" "$name"
    continue
  fi

  file_count=$(find "$project_path" -maxdepth 2 -type f 2>/dev/null | wc -l)
  printf "  %-30s  📁 %d files\n" "$name" "$file_count"

done < "$CONF"
