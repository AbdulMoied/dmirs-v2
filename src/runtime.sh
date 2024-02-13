#!/bin/bash

# Migrate database
printf "\n" && echo "Running django database migrations"
python manage.py migrate --noinput

# Assign groups and permissions

printf "\n" && echo "Assign Groups and permissions"

python manage.py add_groups_and_permissions


# Get Data from Jira

printf "\n" && echo "Get Data From jira"

python manage.py get_data_from_jira
