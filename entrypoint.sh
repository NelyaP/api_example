#!/usr/bin/env sh

python manage.py waitdb
python manage.py makemigrations
python manage.py migrate
python manage.py addgroups
python manage.py createsuperu --username=admin --password=pwd0123456789

python manage.py runserver 0.0.0.0:8000