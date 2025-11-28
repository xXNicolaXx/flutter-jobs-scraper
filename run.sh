#!/bin/bash
set -e

# Calcola il path assoluto dello script
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Attiva la venv corretta
source "$BASE_DIR/venv/bin/activate"

# Carica variabili da .env
export $(grep -v '^#' "$BASE_DIR/.env" | xargs)

# Vai nella directory del progetto
cd "$BASE_DIR"

# Esegui il main
python3 main.py
