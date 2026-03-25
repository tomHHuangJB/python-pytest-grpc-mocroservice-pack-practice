#!/bin/zsh

set -euo pipefail

# Builds and starts the local FastAPI practice environment with Docker Compose.
REPO_DIR="/Users/tomhuang/Documents/job/resume/doble/python-pytest-grpc-mocroservice-pack-practice"

cd "$REPO_DIR"
docker compose up --build
