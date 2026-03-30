#!/usr/bin/env bash
# Open parallel Claude Code sessions — one per managed project
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/load-projects.sh"

SESSION_NAME="office-forge-orchestrator"

if ! command -v tmux &>/dev/null; then
  echo "Error: tmux required for parallel sessions" >&2
  exit 1
fi

if ! command -v claude &>/dev/null; then
  echo "Error: claude CLI required" >&2
  exit 1
fi

# Create or attach to tmux session
tmux new-session -d -s "$SESSION_NAME" 2>/dev/null || true

window_idx=0
for i in "${!PROJECTS[@]}"; do
  path="${PROJECTS[$i]}"
  name="${PROJECT_NAMES[$i]}"

  if [ ! -d "$path" ]; then
    continue
  fi

  if [ "$window_idx" -eq 0 ]; then
    tmux rename-window -t "$SESSION_NAME:0" "$name"
    tmux send-keys -t "$SESSION_NAME:0" "cd '$path' && claude" Enter
  else
    tmux new-window -t "$SESSION_NAME" -n "$name"
    tmux send-keys -t "$SESSION_NAME:$window_idx" "cd '$path' && claude" Enter
  fi

  ((window_idx++))
done

if [ "$window_idx" -eq 0 ]; then
  echo "No valid projects in config/projects.conf" >&2
  exit 1
fi

echo "Started $window_idx CC sessions in tmux session '$SESSION_NAME'"
echo "Attach with: tmux attach -t $SESSION_NAME"
