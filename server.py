import os
import threading
from flask import Flask
from telegram_bot_interactive import main as run_telegram_bot

# Khởi tạo một Web Server bù nhìn để đánh lừa Render.com giữ cho Bot luôn sống
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Morning Assistant Bot đang chạy khỏe mạnh 24/7 trên Đám mây!"

def start_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Chạy Web Server ở một luồng (thread) riêng biệt
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Vạch luồng chính để chạy linh hồn của con Bot Telegram
    run_telegram_bot()
