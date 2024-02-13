#!/usr/bin/env bash

echo "Running in $DJANGO_ENV environment"


python manage.py migrate
python manage.py collectstatic --no-input
echo "Running: python manage.py runserver 0.0.0.0:8000"
exec python manage.py runserver 0.0.0.0:8000

##!/bin/bash
#
## ==================================================
## Wait until Database is available before continuing
## ==================================================
#export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_URL:$POSTGRES_PORT/$POSTGRES_DB
#
#printf "\n" && echo "Checking Database is UP" | boxes -d shell -p a1l2
#until psql $DATABASE_URL -c '\l'; do
#  echo >&2 "Postgres is unavailable - sleeping"
#  sleep 1
#done
#
#echo >&2 "Postgres is up - continuing" && figlet "Postgres is up"
#
## =========================================
## Run inbuilt Django server if ENV is LOCAL
## =========================================
#
## Run development server
#printf "\n" && echo "Starting inbuilt django webserver" | boxes -d shell -p a1l2
#python manage.py makemigrations
#python manage.py migrate --noinput
#
#echo "Running: python manage.py runserver 0.0.0.0:8000"
#python manage.py runserver 0.0.0.0:8000
#
