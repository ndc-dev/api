import jsonschema
import requests
import json
import codecs

if __name__ == "__main__":
    url = "http://127.0.0.1:8000/ndc9.json"
    r = requests.get(url, headers={"content-type": "application/json"})
    data = r.json()
    with codecs.open("jsonschema.json", "r", "utf-8") as file:
        json_schema = json.load(file)
        for item in data.values():
            jsonschema.validate(item, json_schema)
        # jsonschema.validate(data["724.4"], json_schema)
