import json 


def log_search_entry(keyword):
    history = read_search_history()
    if keyword in history:
        history[keyword] += 1
    else:
        history.setdefault(keyword, 1)
    with open("history.json", "w") as f:
        f.write(json.dumps(history))


def read_search_history():
    history = dict()
    result = []
    with open("history.json", "r") as h:
        history = json.load(h)
    for key in history:
        result.append({
            "name": key,
            "views": history[key]
        })
    return result