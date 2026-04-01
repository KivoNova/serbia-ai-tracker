from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

# 实例化离线的英文分析模型
analyzer = SentimentIntensityAnalyzer()

# 实例化基于网页仿真的无键值翻译器
translator_sr_en = GoogleTranslator(source='sr', target='en')
translator_en_zh = GoogleTranslator(source='en', target='zh-CN')

def analyze_and_translate(text_sr):
    # 第一层：语言清洗转换中枢 塞尔维亚语 -> 英语 (因为 VADER 是原生英语逻辑库)
    try:
        text_en = translator_sr_en.translate(text_sr)
        time.sleep(0.5) # 防止 GitHub IP 防刷触发
    except Exception as e:
        print("Translation to EN failed:", e)
        text_en = text_sr
        
    # 第二层：翻译成母语中文 (专供国内看板展厅展示)
    try:
        text_zh = translator_en_zh.translate(text_en)
        time.sleep(0.5)
    except Exception as e:
        print("Translation to ZH failed:", e)
        text_zh = text_en
        
    # 第三层：离线的自然语言情绪分类运算
    scores = analyzer.polarity_scores(text_en)
    compound = scores['compound']
    
    # 制定策略交易员准则边界
    if compound >= 0.15:
        sentiment = 'Positive'
    elif compound <= -0.15:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
        
    return sentiment, text_en, text_zh
