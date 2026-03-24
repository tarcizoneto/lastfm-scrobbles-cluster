import json

def dumpJson(filename, data):
     with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def loadJson(fileDirectory):
    with open(fileDirectory, "r", encoding="utf-8") as f:
        return json.load(f)