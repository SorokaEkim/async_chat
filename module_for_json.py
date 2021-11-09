import json
import os

def read_json_file(path: str):
    """Чтение из json."""
    with open(path, 'r', encoding="utf-8") as read_file:
        data = json.load(read_file)

    return data

def write_json_file(path, data):
    """Запись в json"""
    with open(path, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False)
        