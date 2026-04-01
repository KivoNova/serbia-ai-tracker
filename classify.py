def classify_news(text_en):
    text_lower = text_en.lower()
    
    # 以英文长文本进行多重逻辑打标分流拦截
    if any(word in text_lower for word in ['tech', 'software', 'it ', 'oracle', 'google', 'digital', 'ai', 'computer', 'app', 'code', 'microsoft']):
        return 'Tech'
    elif any(word in text_lower for word in ['energy', 'fuel', 'oil', 'gas', 'price', 'barrel', 'electricity', 'power', 'solar', 'coal', 'lithium', 'rio tinto']):
        return 'Energy'
    elif any(word in text_lower for word in ['bank', 'inflation', 'finance', 'interest', 'nbs', 'money', 'economy', 'tax', 'debt', 'salary', 'gdp', 'market', 'stock', 'investment', 'fund', 'euro', 'dinar', 'rsd']):
        return 'Finance'
    else:
        return 'All'

def generate_reasoning(sentiment, category, text_en):
    reasoning = "【VADER 离线统计算法引擎溯源 / 免除 LLM 外部调用】\n"
    reasoning += f"1. [赛道拦截提取词袋] 翻译提取英文原态语料 -> '{text_en[:80]}...'\n"
    reasoning += f"2. [情绪定点测写] 模型计算其波动极值 Compound 判定该事件带有着显著的 {sentiment} 定点特征。\n"
    
    if sentiment == 'Positive':
        reasoning += f"3. [跨维量化结论] 这一信号客观上将提振 {category} 宏观赛道的存量热度，我们直接判定为做多【利好 (Positive)】。"
    elif sentiment == 'Negative':
        reasoning += f"3. [跨维量化结论] 探测到悲观情绪高频集聚预演体，严重构成了实体企业打击面映射，做空降级为【利空 (Negative)】。"
    else:
        reasoning += f"3. [跨维量化结论] 正负向情绪对冲削减，且主词干极向模糊，预计走势不被其单一事件裹挟干扰，维持【横盘/中性 (Neutral)】。"
        
    return reasoning
