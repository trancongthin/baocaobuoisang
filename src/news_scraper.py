import urllib.parse
import feedparser
from src.config_manager import load_topics

def get_top_news():
    topics = load_topics()
    if not topics:
        return "Hiện máy chủ chưa theo dõi mảng tin tức nào. Sếp hãy nhắn /them [từ khóa] để hệ thống tìm đọc nhé!"
    
    news_items = []
    
    for topic in topics:
        # Encode từ khóa để vứt vào Google News
        query = urllib.parse.quote(topic)
        url = f"https://news.google.com/rss/search?q={query}&hl=vi&gl=VN&ceid=VN:vi"
        
        try:
            feed = feedparser.parse(url)
            # Quét đúng 2 tin nổi bật nhất tránh tình trạng AI bị ngộp nhảm
            news_items.append(f"Mảng: {topic.upper()}")
            count = 0
            for entry in feed.entries:
                if count >= 2: break
                title = entry.title
                news_items.append(f"Tin {count+1}: {title}")
                count += 1
            news_items.append("")
        except Exception as e:
            print(f"Lỗi khi rọi tin {topic}: {e}")
            
    if not news_items:
        return "Xin lỗi sếp, hệ thống không lùng sục được tin tức nào hôm nay."
        
    return "\n".join(news_items).strip()

if __name__ == "__main__":
    print(get_top_news())
