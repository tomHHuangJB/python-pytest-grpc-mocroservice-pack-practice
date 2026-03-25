#!/bin/zsh

set -euo pipefail

# Activates the local virtualenv and runs all pytest checks except UI tests.
REPO_DIR="/Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice"

cd "$REPO_DIR"
unalias deactivate 2>/dev/null || true
source .venv/bin/activate
unset PYTEST_PLUGINS
python -m pytest -m "not ui"
