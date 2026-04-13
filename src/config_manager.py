import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'topics.json')

def load_topics():
    if not os.path.exists(CONFIG_FILE):
        # Mặc định danh sách chủ đề ban đầu ban đầu
        default_topics = ["Phân tích Marketing", "Góc nhìn Doanh nhân", "Xu hướng Đầu tư chung, Công nghệ và Trí tuệ AI"]
        save_topics(default_topics)
        return default_topics
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_topics(topics):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=4)

def add_topic(topic):
    topics = load_topics()
    # Check trùng lặp bằng lower case
    for t in topics:
        if t.lower() == topic.lower():
            return False
    topics.append(topic)
    save_topics(topics)
    return True

def remove_topic(topic):
    topics = load_topics()
    topic_lower = topic.lower()
    for t in topics:
        if t.lower() == topic_lower:
            topics.remove(t)
            save_topics(topics)
            return True, t
    return False, None
