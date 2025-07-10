#!/bin/bash
# Startup script for FastAPI backend in Docker development

set -e

export PYTHONPATH="$(cd "$(dirname "$0")"; pwd)/src"  # Ensure src is in PYTHONPATH for absolute imports, regardless of invocation directory

uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
