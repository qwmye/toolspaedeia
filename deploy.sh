#!/usr/bin/env bash
# Post-pull deployment script for PythonAnywhere.
#
# Usage (from the repo root on PythonAnywhere):
#   git pull && bash deploy.sh
#
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
MANAGE="$PROJECT_DIR/toolspaedeia/manage.py"

export DJANGO_SETTINGS_MODULE="toolspaedeia.settings_pythonanywhere"

echo "==> Installing / syncing dependencies…"
cd "$PROJECT_DIR"
uv sync

echo "==> Applying database migrations…"
uv run python "$MANAGE" migrate --noinput

echo "==> Collecting static files…"
uv run python "$MANAGE" collectstatic --noinput

PA_USER="qwmyee"
PA_DOMAIN="$PA_USER.pythonanywhere.com"
PA_API="https://www.pythonanywhere.com/api/v0/user/$PA_USER/webapps/$PA_DOMAIN/reload/"

echo "==> Reloading web app…"
curl -s -X POST -H "Authorization: Token $PYTHONANYWHERE_API_TOKEN" "$PA_API"
echo ""

echo "==> Done."
