import os
import requests
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

url = "https://api.notion.com/v1/search"
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
payload = {
    "filter": {"value": "database", "property": "object"}
}

try:
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        for db in data["results"]:
            title = db.get("title", [{}])
            text = title[0].get("plain_text", "Untitled") if title else "Untitled"
            print(f"FOUND DB: {text} | ID: {db['id']}")
    else:
        print("NO_DATABASE_FOUND")
except Exception as e:
    print(f"ERROR: {e}")
