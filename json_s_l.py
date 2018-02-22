import json


def save(file, obj):
    file += ".json"
    with open(file, "w") as file:
        file.write(json.dumps(obj))


def load(file):
    file += ".json"
    with open(file, "r") as file:
        return file.read()
