#!/usr/bin/env bash

set -euo pipefail

# Move to the repository root, regardless of where this script is called.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

uv run --project code code/generate_sessions.py "$@"
