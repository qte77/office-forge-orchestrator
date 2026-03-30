#!/usr/bin/env bash
# Run a task in a specific project directory using Claude Code
# Usage: ./run.sh "task description" [project-path]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load-projects.sh"

TASK="${1:?Usage: $0 \"task description\" [project-path]}"
PROJECT_PATH="${2:-.}"

# Validate project path is a known project
valid=false
for path in "${PROJECTS[@]}"; do
  if [[ "$PROJECT_PATH" == "$path" ]]; then
    valid=true
    break
  fi
done

if [ "$valid" = false ] && [ "$PROJECT_PATH" != "." ]; then
  echo "Warning: '$PROJECT_PATH' is not in config/projects.conf" >&2
fi

if [ ! -d "$PROJECT_PATH" ]; then
  echo "Error: $PROJECT_PATH is not a directory" >&2
  exit 1
fi

echo "Running task in $(basename "$PROJECT_PATH"): $TASK"
cd "$PROJECT_PATH"
claude -p "$TASK"
