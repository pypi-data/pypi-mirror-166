import json


def load_from_file(filename):
    with open(filename, "rb") as f:
        return json.loads(f.read())
