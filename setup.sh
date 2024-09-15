#!/bin/bash

# For the docker image

# Change into the correct dir
cd digivote

# Apply database migrations
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser --no-input --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}

# Start the server
exec "$@"
