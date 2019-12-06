import json 
import pytz
from datetime import datetime
from datetime import timezone

# TODO: rewrite as list (iterate)
def log_search_entry(keyword):
    history = read_search_history()
    found = False
    tz = pytz.timezone("US/Eastern")
    for entry in history:
        if entry["name"] == keyword:
            entry["views"] += 1
            found = True
    if not found:
        history.append({
            "name": keyword,
            "views": 1,
            "last_searched": datetime.now(tz).strftime("%H:%M:%S")
        })
    with open("history.json", "w") as f:
        f.write(json.dumps(history))


def read_search_history():
    history = dict()
    result = []
    with open("history.json", "r") as h:
        history = json.load(h)
    for entry in history:
        result.append({
            "name": entry["name"],
            "views": entry["views"],
            "last_searched": entry["last_searched"]
        })
    return result