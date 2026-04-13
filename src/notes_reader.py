import os
import requests
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def get_today_tasks():
    if not NOTION_API_KEY or not DATABASE_ID:
        return "Notion chưa được cấu hình."

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    payload = {
        "page_size": 20
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        tasks = []
        for page in data.get("results", []):
            props = page.get("properties", {})
            title = "Untitled"
            for prop_name, prop_data in props.items():
                if prop_data.get("type") == "title":
                    title_parts = prop_data.get("title", [])
                    if title_parts:
                        title = title_parts[0].get("plain_text", "Untitled")
                        
                # Bỏ qua các task đã đánh dấu Checkbox hoàn thành
                if prop_data.get("type") == "checkbox" and prop_data.get("checkbox") == True:
                    title = None
                # Bỏ qua các status tên "Done"
                if prop_data.get("type") == "status" and prop_data.get("status") and prop_data["status"].get("name", "").lower() in ["done", "completed"]:
                    title = None

            if title:
                tasks.append(f"- {title}")
                
        if not tasks:
            return "Hôm nay không có đầu việc nào đang dang dở trên Notion."
        return "\n".join(tasks)

    except Exception as e:
        return f"Lỗi đọc Notion: {e}"

if __name__ == "__main__":
    print(get_today_tasks())
