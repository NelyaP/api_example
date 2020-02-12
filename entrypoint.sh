#!/usr/bin/env sh

python manage.py waitdb
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata orders.json
python manage.py runserver 0.0.0.0:8000