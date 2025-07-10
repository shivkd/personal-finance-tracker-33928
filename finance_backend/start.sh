#!/bin/bash
# Startup script for FastAPI backend in Docker development

set -e

# Set WORKDIR to backend root and robust PYTHONPATH for container context
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)/src:$(pwd)"

uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
