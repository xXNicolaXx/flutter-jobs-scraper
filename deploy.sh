#!/bin/bash
set -e

BASE_DIR=$(pwd)
PYTHON_BIN="/usr/bin/python3"

cd "$BASE_DIR"

# Virtual environment
$PYTHON_BIN -m venv venv
source venv/bin/activate

# Aggiorna pip e installa dipendenze
pip install --upgrade pip
pip install -r requirements.txt

# Installazione browser Playwright
python -m playwright install-deps
python -m playwright install

# Inizializza DB
python - <<PY
from utils import init_db
init_db()
PY

# Imposta cron job ogni 6 ore usando run.sh
CRON_CMD="0 */6 * * * $BASE_DIR/run.sh >> $BASE_DIR/run.log 2>&1"
( crontab -l 2>/dev/null | grep -Fv "$BASE_DIR/run.sh" || true; echo "$CRON_CMD" ) | crontab -

echo "Setup completato! Cron job impostato."
