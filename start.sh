#!/bin/bash
set -e

echo "Waiting for mysql..."
sleep 15

exec gunicorn --access-logfile - --bind 0.0.0.0:80 --timeout 60 app:app
