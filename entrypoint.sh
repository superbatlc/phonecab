#!/bin/sh
set -e

echo "Waiting for database..."
# Add database connectivity check here if needed

echo "Running migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Starting server..."
exec python3 manage.py runserver 0.0.0.0:8001