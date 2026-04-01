import feedparser
import re

def fetch_rss_news():
    # 截取具有公信力的财经订阅源
    feeds = [
        {"url": "https://www.blic.rs/rss/Biznis", "source": "Blic Biznis"},
        {"url": "https://www.blic.rs/rss/IT", "source": "Blic ITTech"}
    ]
    articles = []
    
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            if not parsed.entries:
                continue
                
            # 我们每次只取头条的5个热点去重跑，免得算太久
            for entry in parsed.entries[:5]: 
                title = entry.get("title", "")
                summary_raw = entry.get("summary", "")
                # 清理掉网页中的图片和HTML等杂质
                summary_clean = re.sub(r'<[^>]+>', '', summary_raw).strip()
                
                text = f"{title}. {summary_clean}"
                if len(text) > 10:
                    articles.append({
                        "source": feed["source"],
                        "url": entry.get("link", feed["url"]),
                        "original": text
                    })
        except Exception as e:
            print(f"Failed to fetch {feed['url']}: {e}")
            
    return articles
