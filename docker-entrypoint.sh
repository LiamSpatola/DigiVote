#!/bin/sh

cd digivote
# Migrating the changes to the database
python3 manage.py migrate

# Check if superuser exists
if [ -z "$(python3 manage.py shell -c 'from django.contrib.auth.models import User; User.objects.filter(username=__import__("os").environ["DJANGO_SUPERUSER_USERNAME"]).exists()')" ]; then
    # Creating a super user with the env variables supplied by the user if user doesn't exist already
    python3 manage.py createsuperuser --no-input --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL}
fi

exec "$@"