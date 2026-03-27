#!/usr/bin/env bash
# Run a task in a specific project directory using Claude Code
# Usage: ./run.sh "task description" [project-path]
set -euo pipefail

TASK="${1:?Usage: $0 \"task description\" [project-path]}"
PROJECT_PATH="${2:-.}"

if [ ! -d "$PROJECT_PATH" ]; then
  echo "Error: $PROJECT_PATH is not a directory" >&2
  exit 1
fi

echo "Running task in $(basename "$PROJECT_PATH"): $TASK"
cd "$PROJECT_PATH"
claude -p "$TASK"
