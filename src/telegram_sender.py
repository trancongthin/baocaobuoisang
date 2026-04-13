import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    if not TOKEN or not CHAT_ID:
        return False, "Thiếu cấu hình TOKEN hoặc CHAT_ID"
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "Thành công"
    except Exception as e:
        return False, str(e)

def get_chat_id_from_updates():
    if not TOKEN:
        return None
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("ok") and len(data["result"]) > 0:
            # Lấy chat ID từ tin nhắn mới nhất
            return str(data["result"][-1]["message"]["chat"]["id"])
    except Exception as e:
        pass
    return None

if __name__ == "__main__":
    cid = get_chat_id_from_updates()
    if cid:
        print(f"CHAT_ID_FOUND={cid}")
    else:
        print("NO_MESSAGE_FOUND")
