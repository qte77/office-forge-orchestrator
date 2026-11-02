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

# Headless runs start in Manual mode, where every call needing approval is
# denied, so set the mode explicitly. JSON output on stdout carries .result,
# .is_error and .total_cost_usd for the caller; status messages go to stderr.
# --add-dir loads the office-forge skills; its files stay read-only.
ORCH_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PERMISSION_MODE="${OFFICE_FORGE_PERMISSION_MODE:-acceptEdits}"
MAX_BUDGET_USD="${OFFICE_FORGE_MAX_BUDGET_USD:-5}"

echo "Running task in $(basename "$PROJECT_PATH"): $TASK" >&2
cd "$PROJECT_PATH"
claude -p "$TASK" \
  --add-dir "$ORCH_ROOT" \
  --disallowedTools "Edit(/${ORCH_ROOT}/**)" \
  --permission-mode "$PERMISSION_MODE" \
  --permission-prompts none \
  --output-format json \
  --max-budget-usd "$MAX_BUDGET_USD"
