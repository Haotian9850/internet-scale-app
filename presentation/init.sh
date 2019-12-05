pip install redis
pip install requests
echo "[]" > /app/history.json 
mod_wsgi-express start-server --log-level info --working-directory /app --reload-on-changes /app/frontend/frontend/wsgi.py

