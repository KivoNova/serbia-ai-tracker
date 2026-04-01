import json
import os
from scraper import fetch_rss_news
from sentiment import analyze_and_translate
from classify import classify_news, generate_reasoning

def generate_reports():
    print(">>> 启动 GitHub Actions Serverless 全离线分析引擎...")
    raw_articles = fetch_rss_news()
    
    final_data = []
    
    for idx, article in enumerate(raw_articles):
        print(f"处理数据节点 [{idx+1}/{len(raw_articles)}]: {article['source']}")
        
        # 调用无 API 拦截网
        sentiment, text_en, text_zh = analyze_and_translate(article['original'])
        category = classify_news(text_en)
        reasoning = generate_reasoning(sentiment, category, text_en)
        
        item = {
            "source": article["source"],
            "url": article["url"],
            "lang": "塞尔维亚语",
            "targetLang": "sr",
            "original": article["original"],
            "zhSummary": text_zh,
            "sentiment": sentiment,
            "category": category,
            "reasoning": reasoning
        }
        final_data.append(item)
    
    # 构建双输出模式
    os.makedirs('data', exist_ok=True)
    os.makedirs('public', exist_ok=True)
    
    # 1. 结构化 JSON 纯数据存档 (Cloudflare Pages 等接口可读取)
    with open('data/news.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    # 2. 生成内嵌式 JS 数据源 (直接兼容原版单文件纯前端)
    with open('public/feed_data.js', 'w', encoding='utf-8') as f:
        json_str = json.dumps(final_data, ensure_ascii=False, indent=4)
        f.write(f"// GitHub Actions Auto Generated Data\nconst realNewsData = {json_str};\n")
        
    print(f">>> 成功序列化 {len(final_data)} 条多空分析数据并落盘！等待部署分发。")

if __name__ == '__main__':
    generate_reports()
