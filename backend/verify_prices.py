import requests
import json

try:
    r = requests.get("http://localhost:8000/api/prices/current")
    data = r.json()
    print("--- Current Prices ---")
    for item in data.get("data", []):
        print(f"{item['fund']}: {item['price']} ({item['source']})")
except Exception as e:
    print(e)
