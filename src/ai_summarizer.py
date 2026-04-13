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
        - Trình bày dạng các đoạn gạch đầu dòng gọn gàng, phù hợp đọc lướt trên điện thoại.
        - Khuyến khích sử dụng Emoji minh họa cho đẹp mắt.
        - Tuyệt đối không xài định dạng đánh dấu in dậm kiểu phức tạp.

        THÔNG TIN ĐẦU VÀO:
        ---
        Tin tức nóng trong nước và thế giới (hãy tự động lọc ra 3-5 diễn biến sốc/quan trọng nhất):
        {news_text}
        
        ---
        Công việc chủ tịch cần giải quyết hôm nay từ hệ thống (Nhắc nhở nhẹ nhàng và cổ vũ Sếp thực hiện):
        {tasks_text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi không gọi được AI xử lý: {e}"

if __name__ == "__main__":
    print("Testing AI Summarizer...")
    print(generate_morning_report("Thị trường chứng khoán hôm nay tích cực.", "Xem báo cáo quý 1"))
