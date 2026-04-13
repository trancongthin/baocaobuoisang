import sys
import os

from src.news_scraper import get_top_news
from src.notes_reader import get_today_tasks
from src.ai_summarizer import generate_morning_report
from src.telegram_sender import send_telegram_message

def main():
    print("🌅 Đang bắt đầu khởi động Trợ lý Buổi Sáng...")
    
    print("1. Đang quét 10 báo mạng lớn nhất...")
    news_text = get_top_news()
    
    print("2. Đang truy cập quyền Notion của bạn...")
    tasks_text = get_today_tasks()
    
    print("3. Đang chuyển cho não bộ Gemini biên soạn báo cáo...")
    report = generate_morning_report(news_text, tasks_text)
    
    print("4. Đang gửi báo cáo về thẳng cấu hình Telegram của Sếp...")
    success, msg = send_telegram_message(report)
    
    if success:
        print("✅ Hoàn tất! Báo cáo đã bay vào điện thoại của Sếp. Chúc Sếp một ngày mới năng suất!")
    else:
        print(f"❌ Có lỗi khi gửi qua Telegram: {msg}")

if __name__ == "__main__":
    main()
