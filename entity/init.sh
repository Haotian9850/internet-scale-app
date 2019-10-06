#!/bin/bash          

python /app/portia/manage.py makemigrations main
python /app/portia/manage.py migrate
python /app/portia/manage.py loaddata /app/portia/fixture.json
mod_wsgi-express start-server --log-level info --working-directory /app --reload-on-changes /app/portia/portia/wsgi.py
