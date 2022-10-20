#!/bin/bash
# Initialize options for gunicorn
OPTS=(
  --env FLASK_APP=billing-ai
  --env FLASK_ENV=development
  --workers 2
  -b 0.0.0.0:5001
  --reload
  --daemon
)

#Run gunicorn
gunicorn "${OPTS[@]}" wsgi:app