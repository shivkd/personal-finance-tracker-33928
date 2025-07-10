#!/bin/bash
# Startup script for FastAPI backend in Docker development

set -e

export PYTHONPATH=$(pwd)/src # Ensure src is in PYTHONPATH for absolute imports

uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
