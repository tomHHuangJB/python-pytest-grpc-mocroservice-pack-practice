#!/bin/zsh

set -euo pipefail

# Stops the local Docker Compose practice environment.
REPO_DIR="/Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice"

cd "$REPO_DIR"
docker compose down
