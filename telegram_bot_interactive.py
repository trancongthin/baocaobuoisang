import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from src.config_manager import load_topics, add_topic, remove_topic
from src.news_scraper import get_top_news
from src.notes_reader import get_today_tasks
from src.ai_summarizer import generate_morning_report

load_dotenv()
# Thêm lớp khiên tút lại mã khóa: Tự động gọt bỏ dấu ngoặc kép và dấu cách thừa nếu Sếp chép lố tay
_raw_token = os.getenv("TELEGRAM_BOT_TOKEN") or ""
TOKEN = _raw_token.strip().strip('"').strip("'")

_raw_chat = os.getenv("TELEGRAM_CHAT_ID") or ""
ALLOWED_CHAT_ID = _raw_chat.strip().strip('"').strip("'")

# Bật log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Xác thực đúng sếp thì mới tiếp
    if str(update.effective_chat.id) != ALLOWED_CHAT_ID:
        await update.message.reply_text("Xin lỗi, tôi là thư ký kín chỉ phục vụ Sếp của tôi thôi.")
        return
    await update.message.reply_text(
        "👋 Chào Chủ Tịch! Trợ lý báo cáo cá nhân khẩn cấp đã sẵn sàng.\n\n"
        "Các lệnh hiện có:\n"
        "📜 /baocao - Yêu cầu báo cáo tình hình ngay lập tức\n"
        "🔍 /chude - Xem danh sách các mảng phần loại tin tức\n"
        "➕ /them [Tên] - Thêm thể loại để mai đọc (VD: /them trí tuệ nhân tạo)\n"
        "➖ /xoa [Tên] - Loại bỏ chủ đề cũ không quan tâm nữa"
    )

async def list_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ALLOWED_CHAT_ID: return
    topics = load_topics()
    if not topics:
        await update.message.reply_text("Hệ thống chưa học chủ đề tin tức nào.")
        return
    
    msg = "📚 **Các mảng thông tin đang theo dõi:**\n"
    for idx, t in enumerate(topics):
        msg += f"{idx+1}. {t}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def cmd_add_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ALLOWED_CHAT_ID: return
    if not context.args:
        await update.message.reply_text("Sếp gõ thiếu từ khóa rồi. Hãy gõ: `/them kinh doanh bất động sản`", parse_mode="Markdown")
        return
    
    topic = " ".join(context.args)
    if add_topic(topic):
        await update.message.reply_text(f"✅ Đã dặn dò hệ thống Google News tìm kiếm tin tức về **{topic}** từ ngày mai.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"⚠️ Chủ đề **{topic}** đã tồn tại trong não bộ rồi Sếp ạ.", parse_mode="Markdown")

async def cmd_remove_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ALLOWED_CHAT_ID: return
    if not context.args:
        await update.message.reply_text("Gõ thiếu mất rồi. Hãy gõ: `/xoa kinh doanh`", parse_mode="Markdown")
        return
        
    topic = " ".join(context.args)
    success, real_name = remove_topic(topic)
    if success:
        await update.message.reply_text(f"🗑 Đã vứt chủ đề **{real_name}** vào thùng rác.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ Không tìm thấy chủ đề nào tên giống vậy để xóa.", parse_mode="Markdown")

async def baocao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != ALLOWED_CHAT_ID: return
    
    msg = await update.message.reply_text("🔄 Đang hối hả cào tin tức và lật tung Notion. Sếp đợi 15 giây nhé...")
    
    news_text = get_top_news()
    tasks_text = get_today_tasks()
    report = generate_morning_report(news_text, tasks_text)
    
    await msg.edit_text(report, parse_mode="Markdown")

def main():
    if not TOKEN:
        print("Lỗi: Không tìm thấy TELEGRAM_BOT_TOKEN")
        return
        
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("baocao", baocao))
    app.add_handler(CommandHandler("chude", list_topics))
    app.add_handler(CommandHandler("them", cmd_add_topic))
    app.add_handler(CommandHandler("xoa", cmd_remove_topic))

    print("🤖 Bot đang chạy ngầm lẩn khuất chờ lệnh...!")
    app.run_polling()

if __name__ == '__main__':
    main()
