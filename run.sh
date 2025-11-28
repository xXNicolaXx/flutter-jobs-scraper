#!/bin/bash
set -e

BASE_DIR=$(pwd)
source "$BASE_DIR/venv/bin/activate"
cd "$BASE_DIR"

# Carica variabili .env
export $(grep -v '^#' .env | xargs)

# Esegui lo script principale
python main.py
