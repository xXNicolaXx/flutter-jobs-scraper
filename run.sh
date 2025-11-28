#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$BASE_DIR/venv"
if [ -f "$VENV_DIR/bin/activate" ]; then
  source "$VENV_DIR/bin/activate"
fi
cd "$BASE_DIR" || exit 1
/usr/bin/python3 main.py
