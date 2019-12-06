from services.logging_service import read_search_history

import json


def get_history(request):
    return {
        "history": read_search_history()
    }