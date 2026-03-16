#!/bin/bash
# Skill Arena Launcher - Load environment variables before running

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Load .env from auth directory if it exists
if [ -f "$PROJECT_ROOT/auth/.env" ]; then
    echo "Loading environment from auth/.env..."
    export $(grep -v '^#' "$PROJECT_ROOT/auth/.env" | xargs)
elif [ -f "$PROJECT_ROOT/.env" ]; then
    echo "Loading environment from .env..."
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
else
    echo "Warning: No .env file found"
fi

# Run the skill-arena script with all arguments
python "$SCRIPT_DIR/scripts/skill-arena.py" "$@"
