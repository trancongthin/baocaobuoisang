import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram_bot_interactive import main as run_telegram_bot

# Ép hệ thống nhả chữ ra màn hình chẩn đoán ngay lập tức (không chờ bộ đệm)
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Bot is live!")

    def log_message(self, format, *args):
        pass # Tắt bớt log rác

def run_dummy_server():
    port = int(os.environ.get("PORT", 5000))
    print(f"👉 [Hệ Thống] Đang bật lá chắn giữ nhịp đập ở cổng {port}...")
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=run_dummy_server)
    t.daemon = True
    t.start()
    
    print("👉 [Hệ Thống] Đang kích hoạt não bộ Telegram Bot...")
    try:
        run_telegram_bot()
    except Exception as e:
        print(f"\n\n🚨 LỖI CỰC KỲ KHẨN CẤP GÂY SẬP BOT: {e}\n\n")
