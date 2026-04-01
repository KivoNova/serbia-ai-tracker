import feedparser
import re

def fetch_rss_news():
    # 截取具有公信力的财经订阅源
    feeds = [
        {"url": "https://www.blic.rs/rss/Biznis/Vesti", "source": "Blic Biznis"},
        {"url": "https://www.blic.rs/rss/IT", "source": "Blic Tech"},
        {"url": "https://www.blic.rs/rss/Slobodno-vreme/Auto", "source": "Blic EV/Energy"},
        {"url": "https://www.b92.net/info/rss/biz.xml", "source": "B92 Economy"}
    ]
    articles = []
    
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            if not parsed.entries:
                continue
                
            # 我们每次只取头条的热点去重跑（放宽到 12 条以满足各个赛道的填充）
            for entry in parsed.entries[:12]: 
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
