#!/usr/bin/env bash
# Generate workspace.code-workspace from config/projects.conf (single source of truth)
# Creates folders list + terminal tasks with runOn: folderOpen

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load-projects.sh"

WORKSPACE_FILE="${OFFICE_FORGE_ROOT}/workspace.code-workspace"

if ! command -v jq &>/dev/null; then
  echo "Error: jq required for workspace generation" >&2
  exit 1
fi

# Build folders array
folders='[]'
for i in "${!PROJECTS[@]}"; do
  folders=$(echo "$folders" | jq \
    --arg p "${PROJECTS[$i]}" \
    --arg n "${PROJECT_NAMES[$i]}" \
    '. + [{"path": $p, "name": $n}]')
done

# Build tasks array
tasks="[]"
for i in "${!PROJECTS[@]}"; do
  tasks=$(echo "$tasks" | jq \
    --arg label "${PROJECT_NAMES[$i]}" \
    --arg cwd "${PROJECTS[$i]}" \
    '. + [{
      "label": $label,
      "type": "shell",
      "command": "exec $SHELL",
      "options": { "cwd": $cwd },
      "runOptions": { "runOn": "folderOpen" },
      "presentation": { "group": "projects", "reveal": "always" },
      "problemMatcher": []
    }]')
done

# Write workspace file
jq -n \
  --argjson folders "$folders" \
  --argjson tasks "$tasks" \
  '{folders: $folders, tasks: {version: "2.0.0", tasks: $tasks}}' \
  > "$WORKSPACE_FILE"

echo "Generated $WORKSPACE_FILE with ${#PROJECTS[@]} projects and tasks"
