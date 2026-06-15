#!/usr/bin/env bash
# Show status of all managed office projects
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load-projects.sh"

echo "Office Projects Status"
echo "══════════════════════════════════════════"

for i in "${!PROJECTS[@]}"; do
  path="${PROJECTS[$i]}"
  name="${PROJECT_NAMES[$i]}"

  if [ ! -d "$path" ]; then
    printf "  %-30s  ⚠  NOT FOUND\n" "$name"
    continue
  fi

  file_count=$(find "$path" -maxdepth 2 -type f 2>/dev/null | wc -l)
  printf "  %-30s  📁 %d files\n" "$name" "$file_count"
done
