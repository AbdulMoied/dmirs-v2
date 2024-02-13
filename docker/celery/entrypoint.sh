#!/usr/bin/env bash

echo "Running in $DJANGO_ENV environment"

sleep 5

exec celery -A sunset_backend worker -l info --concurrency=2
