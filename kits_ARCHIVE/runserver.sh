#!/bin/bash
cd /ticketApp/karma/
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
export DJANGO_SUPERUSER_PASSWORD=isolemnlyswearthatiamuptonogood
python manage.py createsuperuser --username Chadsnuts --email chad@nuts.com --no-input
/opt/conda/bin/gunicorn --access-logfile - --workers 3 --bind unix:/ticketApp/database/gunicorn/karma.sock karma.wsgi:application