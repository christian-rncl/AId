import json


def get_fields(r):
    return json.loads(r)[0]['fields']