#!/usr/bin/env bash
# Usage: diff_settings.sh my/old/settings.py my/new/settings.py
# Should be run in a venv with edx-platform requirements installed
set -euxo pipefail
DJANGO_SETTINGS_MODULE="$1" ./settings_wizard.py to-json > settings1.json
DJANGO_SETTINGS_MODULE="$2" ./settings_wizard.py to-json > settings2.json
diff settings1.json settings2.json
