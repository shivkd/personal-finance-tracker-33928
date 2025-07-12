#!/bin/bash
cd /home/kavia/workspace/code-generation/personal-finance-tracker-33928/finance_backend

# Only source venv if it exists (prevents error if absent)
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Exclude .knowledge directory from linting
flake8 . --exclude=.knowledge,venv

LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

