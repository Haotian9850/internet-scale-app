#!/bin/bash    
chmod -R 777 /app/portia/emails
python /app/portia/manage.py migrate
python /app/portia/manage.py makemigrations
python /app/portia/manage.py flush --no-input
#python /app/portia/manage.py loaddata /app/portia/fixture.json
mod_wsgi-express start-server --log-level info --working-directory /app --reload-on-changes /app/portia/portia/wsgi.py
