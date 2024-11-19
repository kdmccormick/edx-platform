#!/usr/bin/env bash

settings1="${1:-lms.envs.common}"
settings2="${2:-${DJANGO_SETTINGS_MODULE:-lms.envs.tutor.development}}"
set -euo pipefail

DJANGO_SETTINGS_MODULE="$settings1" scripts/settings_wizard.py to-json > /tmp/settings1.json
DJANGO_SETTINGS_MODULE="$settings2" scripts/settings_wizard.py to-json > /tmp/settings2.json
scripts/settings_wizard.py diff-json /tmp/settings1.json /tmp/settings2.json | black -
