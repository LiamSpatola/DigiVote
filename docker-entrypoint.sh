#!/bin/bash

cd digivote
# Migrating the changes to the database
python3 manage.py migrate
# Creating a super user with the env variables supplied by the user
python3 manage.py createsuperuser --no-input --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}

exec "$@"
