#!/usr/bin/env bash
set -o errexit

python -m gunicorn parklaysuites.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --log-level info
