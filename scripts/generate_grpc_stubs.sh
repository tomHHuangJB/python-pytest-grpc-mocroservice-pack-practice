#!/bin/zsh

set -euo pipefail

# Activates the local virtualenv and regenerates Python gRPC stub files.
REPO_DIR="/Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice"

cd "$REPO_DIR"
unalias deactivate 2>/dev/null || true
source .venv/bin/activate
python -m grpc_tools.protoc -I proto --python_out=src --grpc_python_out=src proto/order_app/grpc_contracts/inventory.proto
