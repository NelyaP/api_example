#!/usr/bin/env sh

python manage.py waitdb
python manage.py makemigrations
python manage.py migrate
python manage.py addgroups
python manage.py createsuperu --username=${SUPER_USERNAME} --password=${SUPER_PASS}
python manage.py loaddata ordstatuses.json
python manage.py loaddata ordtypes.json
python manage.py loaddata cities.json
python manage.py loaddata calculator.json
python manage.py runserver 0.0.0.0:8000