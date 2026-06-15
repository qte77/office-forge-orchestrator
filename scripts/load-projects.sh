#!/usr/bin/env bash
# Load PROJECTS[] and PROJECT_NAMES[] arrays from config/projects.conf (SOT)
# Format: path:display-name (comments with #, blank lines skipped)
# Usage: source scripts/load-projects.sh

OFFICE_FORGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECTS_CONF="${OFFICE_FORGE_ROOT}/config/projects.conf"

if [[ ! -f "$PROJECTS_CONF" ]]; then
  echo "Error: $PROJECTS_CONF not found" >&2
  exit 1
fi

PROJECTS=()
PROJECT_NAMES=()

while IFS=: read -r path name; do
  [[ -z "$path" || "$path" == \#* ]] && continue
  # Expand tilde
  path="${path/#\~/$HOME}"
  PROJECTS+=("$path")
  PROJECT_NAMES+=("$name")
done < "$PROJECTS_CONF"
