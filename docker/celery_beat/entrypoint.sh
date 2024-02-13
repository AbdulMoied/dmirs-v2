#!/usr/bin/env bash

echo "Running in $DJANGO_ENV environment"

sleep 5

exec celery -A sunset_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
