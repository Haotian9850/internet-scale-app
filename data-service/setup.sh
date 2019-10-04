#!/bin/bash  
pip install requests
mod_wsgi-express start-server --log-level info --working-directory /app --reload-on-changes /app/data_service/data_service/wsgi.py