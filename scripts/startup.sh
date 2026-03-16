#!/usr/bin/env bash
# EM-Assist session startup script
# Run this at the start of every session: bash scripts/startup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$REPO_ROOT/config/config.yaml"

# ---------------------------------------------------------------------------
# 1. Resolve data directory from config
# ---------------------------------------------------------------------------
# Simple extraction — requires PyYAML not needed here, just grep the value
DATA_DIR=$(grep 'index:' "$CONFIG" | head -1 | sed 's|.*: *"*||;s|".*||;s|/index.yaml||' | sed "s|~|$HOME|")

if [[ -z "$DATA_DIR" ]]; then
  DATA_DIR="$HOME/Documents/em-assist"
fi

echo "Data directory: $DATA_DIR"

if [[ ! -d "$DATA_DIR" ]]; then
  echo "WARNING: Data directory does not exist: $DATA_DIR"
  echo "  Run the following to scaffold template files and create the directory:"
  echo "    python scripts/init-data.py"
  exit 1
fi

# ---------------------------------------------------------------------------
# 2. Data sync (placeholder — extend when remote storage is configured)
# ---------------------------------------------------------------------------
# TODO: Add sync logic here when a remote is set up.
# Examples:
#   git -C "$DATA_DIR" pull --rebase   # if data lives in a git repo
#   rclone sync remote:em-assist "$DATA_DIR"  # if using cloud storage
echo "Data sync: not configured (skipping)"

# ---------------------------------------------------------------------------
# 3. Rebuild the search index
# ---------------------------------------------------------------------------
echo "Rebuilding index..."

# Ensure venv exists
VENV="$REPO_ROOT/.venv"
if [[ ! -d "$VENV" ]]; then
  echo "Creating Python virtual environment..."
  python3 -m venv "$VENV"
fi

# Install dependencies if needed
"$VENV/bin/pip" install --quiet -r "$REPO_ROOT/requirements.txt"

# Run reindex
"$VENV/bin/python" "$REPO_ROOT/scripts/reindex.py"

echo "Startup complete."
