#!/bin/zsh

set -euo pipefail

# Activates the local virtualenv and installs the Chromium browser required for UI tests.
REPO_DIR="/Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice"

cd "$REPO_DIR"
unalias deactivate 2>/dev/null || true
source .venv/bin/activate
python -m playwright install chromium
