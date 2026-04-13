import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_morning_report(news_text, tasks_text):
    if not GEMINI_API_KEY:
        return "Lỗi: Không tìm thấy GEMINI_API_KEY. Vui lòng kiểm tra lại file .env"
        
    genai.configure(api_key=GEMINI_API_KEY)
    
    try:
        # Sử dụng mô hình Flash nhanh gọn
        model = genai.GenerativeModel('gemini-flash-latest') 
        
        prompt = f"""
        Bạn là một Trợ lý Ảo cá nhân chuyên nghiệp. Bây giờ là sáng sớm. Nhiệm vụ của bạn là tổng hợp các sự kiện dưới đây và viết một bản Báo cáo Buổi sáng gửi qua di động cho Chủ tịch (Sếp).

        Quy tắc:
        - Giọng điệu tôn trọng, chuyên nghiệp nhưng vẫn đầy năng lượng.
        - Khuyến khích sử dụng Emoji minh họa cho đẹp mắt.
        - Tuyệt đối không xài định dạng đánh dấu in dậm kiểu phức tạp.
        - Ở phần TIN TỨC, DỨT KHOÁT KHÔNG NÓI CHUNG CHUNG. Bắt buộc phải chia theo từng mốc (Marketing, Đầu tư, AI...) và phải lấy ví dụ ĐÍCH DANH TÊN người, TÊN doanh nghiệp và SỰ KIỆN cụ thể từ dữ liệu báo chí.
        
        MẪU TRÌNH BÀY PHẦN TIN TỨC BẮT BUỘC (chỉ là ví dụ cách trình bày):
        Về Marketing:
        - Tập đoàn A đã áp dụng chiến lược...
        - Nhân vật B đã chi tiền cho dự án...
        
        Về Đầu tư:
        - Quỹ C vừa rót vốn...
        
        Về AI:
        - Hãng công nghệ D ra mắt...

        THÔNG TIN ĐẦU VÀO:
        ---
        Tin tức thô (Hãy nhặt ra các trường hợp thật cụ thể, đích danh để điền vào form):
        {news_text}
        
        ---
        Công việc chủ tịch cần giải quyết hôm nay từ hệ thống (Nhắc nhở nhẹ nhàng và cổ vũ Sếp thực hiện):
        {tasks_text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi không gọi được AI xử lý: {e}"

# Khởi tạo vùng nhớ Session lưu trữ các câu chuyện theo từng User
_chat_sessions = {}

def chat_with_ai(chat_id, user_message):
    if not GEMINI_API_KEY:
        return "Lỗi: Tôi đang bị lạc mất thẻ API Key, không thể tư duy."
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Nếu Sếp chưa từng chat, tạo một bảng ghi nhớ mới cho Sếp
    if chat_id not in _chat_sessions:
        model = genai.GenerativeModel(
            'gemini-flash-latest',
            system_instruction=(
                "Bạn là 'Trợ lý AI Đám mây', một thư ký riêng tận tụy của Chủ tịch. "
                "Hãy trả lời mọi câu hỏi của Sếp một cách cực kỳ rành mạch, sắc bén, tôn trọng và thông minh. "
                "Tuyệt đối không xài định dạng in dậm hay format phức tạp. "
                "Đôi khi hãy chèn thêm các ký tự emoji một cách tinh tế để trình bày đẹp mắt. "
                "Sẵn sàng tóm tắt văn bản, phân tích số liệu hoặc tâm sự khi Sếp cần."
            )
        )
        _chat_sessions[chat_id] = model.start_chat(history=[])
        
    try:
        # Gửi tin nhắn vào luồng nhớ chung và lấy câu trả lời
        response = _chat_sessions[chat_id].send_message(user_message)
        return response.text
    except Exception as e:
        return f"Xin lỗi Sếp, mạch tư duy của tôi đang bị tắc nghẽn, lỗi kỹ thuật: {e}"

if __name__ == "__main__":
    print("Testing AI Summarizer...")
    print(generate_morning_report("Thị trường chứng khoán hôm nay tích cực.", "Xem báo cáo quý 1"))
