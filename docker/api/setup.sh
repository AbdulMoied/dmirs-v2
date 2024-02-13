#!/bin/bash

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Setup complete."
