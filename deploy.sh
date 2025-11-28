#!/bin/bash
set -e
BASE_DIR="/root/flutter-jobs-scraper"
PYTHON_BIN="/usr/bin/python3"
mkdir -p "$BASE_DIR"
cd "$BASE_DIR"
$PYTHON_BIN -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python - <<PY
from utils import init_db
init_db()
PY
CRON_CMD="0 */6 * * * $BASE_DIR/run.sh >> $BASE_DIR/run.log 2>&1"
( crontab -l 2>/dev/null | grep -Fv "$BASE_DIR/run.sh" || true; echo "$CRON_CMD" ) | crontab -
