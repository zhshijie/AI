#!/usr/bin/env python3
"""
ETF投资策略分析脚本
使用AI分析ETF数据，生成投资建议
"""

import json
import os
import sys
from datetime import datetime

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from ai_analyzer import get_analyzer

def analyze_market_sentiment(etf_data):
    """
    分析市场情绪
    """
    realtime = etf_data['realtime']
    indicators = etf_data['indicators']
    
    sentiment_score = 50  # 中性基准
    
    # 价格趋势 (30%)
    change_percent = realtime.get('change_percent', 0)
    if change_percent > 2:
        sentiment_score += 15
    elif change_percent > 0:
        sentiment_score += 8
    elif change_percent > -2:
        sentiment_score -= 8
    else:
        sentiment_score -= 15
    
    # RSI指标 (25%)
    rsi = indicators.get('rsi', 50)
    if rsi > 70:
        sentiment_score -= 10  # 超买
    elif rsi > 60:
        sentiment_score += 5
    elif rsi > 40:
        sentiment_score += 10
    elif rsi > 30:
        sentiment_score += 5
    else:
        sentiment_score -= 10  # 超卖
    
    # MACD指标 (25%)
    macd = indicators.get('macd', {})
    if macd.get('macd', 0) > 0 and macd.get('dif', 0) > macd.get('dea', 0):
        sentiment_score += 12
    elif macd.get('macd', 0) > 0:
        sentiment_score += 6
    elif macd.get('dif', 0) > macd.get('dea', 0):
        sentiment_score += 3
    else:
        sentiment_score -= 8
    
    # 均线系统 (20%)
    ma5 = indicators.get('ma5', 0)
    ma10 = indicators.get('ma10', 0)
    ma20 = indicators.get('ma20', 0)
    current = realtime.get('current', 0)
    
    if current > ma5 > ma10 > ma20:
        sentiment_score += 10  # 多头排列
    elif current > ma5 > ma10:
        sentiment_score += 5
    elif current < ma5 < ma10 < ma20:
        sentiment_score -= 10  # 空头排列
    elif current < ma5 < ma10:
        sentiment_score -= 5
    
    # 限制在0-100范围
    sentiment_score = max(0, min(100, sentiment_score))
    
    # 情绪分类
    if sentiment_score >= 70:
        sentiment = "强烈看多"
        emoji = "🚀"
    elif sentiment_score >= 60:
        sentiment = "看多"
        emoji = "📈"
    elif sentiment_score >= 50:
        sentiment = "偏多"
        emoji = "😊"
    elif sentiment_score >= 40:
        sentiment = "中性"
        emoji = "😐"
    elif sentiment_score >= 30:
        sentiment = "偏空"
        emoji = "😟"
    else:
        sentiment = "看空"
        emoji = "📉"
    
    return {
        'score': round(sentiment_score, 1),
        'sentiment': sentiment,
        'emoji': emoji
    }

def generate_trading_signal(etf_data, sentiment):
    """
    生成交易信号
    """
    realtime = etf_data['realtime']
    indicators = etf_data['indicators']
    sentiment_score = sentiment['score']
    
    # 综合评分
    buy_signals = 0
    sell_signals = 0
    
    # 1. 情绪评分
    if sentiment_score >= 65:
        buy_signals += 2
    elif sentiment_score >= 55:
        buy_signals += 1
    elif sentiment_score <= 35:
        sell_signals += 2
    elif sentiment_score <= 45:
        sell_signals += 1
    
    # 2. RSI
    rsi = indicators.get('rsi', 50)
    if rsi < 30:
        buy_signals += 2  # 超卖
    elif rsi < 40:
        buy_signals += 1
    elif rsi > 70:
        sell_signals += 2  # 超买
    elif rsi > 60:
        sell_signals += 1
    
    # 3. MACD金叉死叉
    macd = indicators.get('macd', {})
    if macd.get('dif', 0) > macd.get('dea', 0) and macd.get('macd', 0) > 0:
        buy_signals += 2  # 金叉
    elif macd.get('dif', 0) < macd.get('dea', 0) and macd.get('macd', 0) < 0:
        sell_signals += 2  # 死叉
    
    # 4. 价格与布林带
    bollinger = indicators.get('bollinger', {})
    current = realtime.get('current', 0)
    if current < bollinger.get('lower', 0):
        buy_signals += 1  # 触及下轨
    elif current > bollinger.get('upper', 0):
        sell_signals += 1  # 触及上轨
    
    # 5. 成交量
    volume_change = indicators.get('volume_change', 0)
    change_percent = realtime.get('change_percent', 0)
    if volume_change > 50 and change_percent > 0:
        buy_signals += 1  # 放量上涨
    elif volume_change > 50 and change_percent < 0:
        sell_signals += 1  # 放量下跌
    
    # 生成建议
    if buy_signals >= 5:
        action = "强烈建议买入"
        action_code = "strong_buy"
        confidence = 90
    elif buy_signals >= 3:
        action = "建议买入"
        action_code = "buy"
        confidence = 75
    elif sell_signals >= 5:
        action = "建议卖出"
        action_code = "sell"
        confidence = 85
    elif sell_signals >= 3:
        action = "建议减仓"
        action_code = "reduce"
        confidence = 70
    else:
        action = "建议持有"
        action_code = "hold"
        confidence = 60
    
    return {
        'action': action,
        'action_code': action_code,
        'confidence': confidence,
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def identify_risks(etf_data, sentiment, signal):
    """
    识别投资风险
    """
    risks = []
    
    realtime = etf_data['realtime']
    indicators = etf_data['indicators']
    
    # 1. 超买超卖风险
    rsi = indicators.get('rsi', 50)
    if rsi > 75:
        risks.append({
            'level': 'high',
            'type': '超买风险',
            'description': f'RSI指标达到{rsi:.1f}，处于严重超买区域，短期可能面临回调压力'
        })
    elif rsi < 25:
        risks.append({
            'level': 'medium',
            'type': '超卖反弹',
            'description': f'RSI指标仅{rsi:.1f}，处于超卖区域，可能存在反弹机会，但需确认底部'
        })
    
    # 2. 趋势风险
    change_percent = realtime.get('change_percent', 0)
    if abs(change_percent) > 5:
        risks.append({
            'level': 'high',
            'type': '波动风险',
            'description': f'当日涨跌幅达{change_percent:.2f}%，市场波动剧烈，需谨慎操作'
        })
    
    # 3. 技术形态风险
    ma5 = indicators.get('ma5', 0)
    ma10 = indicators.get('ma10', 0)
    ma20 = indicators.get('ma20', 0)
    current = realtime.get('current', 0)
    
    if current < ma5 < ma10 < ma20:
        risks.append({
            'level': 'high',
            'type': '趋势风险',
            'description': '均线呈空头排列，下跌趋势明显，不建议抄底'
        })
    
    # 4. 成交量风险
    volume_change = indicators.get('volume_change', 0)
    if volume_change < -50:
        risks.append({
            'level': 'medium',
            'type': '流动性风险',
            'description': f'成交量萎缩{abs(volume_change):.1f}%，市场观望情绪浓厚'
        })
    
    # 5. 布林带风险
    bollinger = indicators.get('bollinger', {})
    if current > bollinger.get('upper', 0):
        risks.append({
            'level': 'medium',
            'type': '估值风险',
            'description': '价格突破布林带上轨，短期涨幅过大，注意回调风险'
        })
    
    # 6. 市场情绪风险
    if sentiment['score'] > 80:
        risks.append({
            'level': 'medium',
            'type': '情绪过热',
            'description': '市场情绪过于乐观，需警惕情绪反转带来的风险'
        })
    elif sentiment['score'] < 20:
        risks.append({
            'level': 'medium',
            'type': '恐慌情绪',
            'description': '市场恐慌情绪蔓延，虽有抄底机会但需等待企稳信号'
        })
    
    # 如果没有明显风险
    if not risks:
        risks.append({
            'level': 'low',
            'type': '常规风险',
            'description': '当前无明显技术风险，但仍需关注市场整体走势和政策变化'
        })
    
    return risks

def prepare_ai_prompt(etf_data_list):
    """
    准备AI分析提示词
    """
    prompt = "# ETF投资分析报告\n"
    prompt += f"分析时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n"
    
    for etf_data in etf_data_list:
        realtime = etf_data['realtime']
        indicators = etf_data['indicators']
        news = etf_data.get('news', [])
        
        prompt += f"## {etf_data['name']}({etf_data['code']})\n"
        prompt += f"### 实时行情\n"
        prompt += f"- 当前价: {realtime['current']}元\n"
        prompt += f"- 涨跌幅: {realtime['change_percent']}%\n"
        prompt += f"- 成交量: {realtime['volume']}手\n"
        prompt += f"- 最高价: {realtime['high']}元\n"
        prompt += f"- 最低价: {realtime['low']}元\n"
        
        prompt += f"### 技术指标\n"
        prompt += f"- RSI(14): {indicators.get('rsi', 0)}\n"
        prompt += f"- MA5: {indicators.get('ma5', 0)}\n"
        prompt += f"- MA10: {indicators.get('ma10', 0)}\n"
        prompt += f"- MA20: {indicators.get('ma20', 0)}\n"
        prompt += f"- MACD: DIF={indicators.get('macd', {}).get('dif', 0)}, DEA={indicators.get('macd', {}).get('dea', 0)}\n"
        prompt += f"- 布林带: 上轨={indicators.get('bollinger', {}).get('upper', 0)}, 中轨={indicators.get('bollinger', {}).get('middle', 0)}, 下轨={indicators.get('bollinger', {}).get('lower', 0)}\n"
        prompt += f"- 成交量变化: {indicators.get('volume_change', 0)}%\n"
        
        if news:
            prompt += f"### 相关新闻 (最近{len(news)}条)\n"
            for i, item in enumerate(news[:5], 1):
                prompt += f"{i}. {item['title']}\n"
            prompt += "\n"
    
    prompt += "请作为专业的投资分析师，基于以上数据，为每只ETF提供：\n"
    prompt += "1. 市场情绪分析（看多/看空/中性）\n"
    prompt += "2. 投资建议（买入/持有/卖出）及理由\n"
    prompt += "3. 关键风险提示\n"
    prompt += "4. 操作策略建议\n"
    prompt += "请用专业、客观的语言，给出具体可操作的建议。"
    
    return prompt

def analyze_with_ai(etf_data_list):
    """
    使用AI进行分析
    """
    try:
        ai_provider = os.getenv('AI_PROVIDER', 'groq')
        print(f"尝试使用 {ai_provider} AI 进行深度分析...")
        
        analyzer = get_analyzer(ai_provider)
        
        if analyzer.use_fallback:
            print("  ⚠️  AI服务不可用，将使用规则分析")
            return None
        
        # 准备提示词
        prompt = prepare_ai_prompt(etf_data_list)
        
        # 调用AI
        print(f"  正在调用 {ai_provider} AI API...")
        
        messages = [
            {
                'role': 'system',
                'content': '你是一位资深的ETF投资分析师，擅长技术分析和市场研判。请基于提供的数据，给出专业、客观、可操作的投资建议。'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        # 使用analyzer的内部方法
        response = analyzer._call_ai_api(messages)
        
        if response:
            print("  ✓ AI分析完成")
            return response
        else:
            print("  ❌ AI分析失败")
            return None
            
    except Exception as e:
        print(f"  ❌ AI分析出错: {e}")
        return None

def main():
    print("=" * 60)
    print("ETF投资策略分析任务")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 读取ETF数据
    data_file = 'data/etf_data.json'
    
    if not os.path.exists(data_file):
        print(f"❌ 错误: 未找到数据文件 {data_file}")
        print("   请先运行: python scripts/fetch_etf_data.py")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    etf_data_list = data.get('etfs', [])
    
    if not etf_data_list:
        print("❌ 错误: 数据文件为空")
        return
    
    print(f"加载了 {len(etf_data_list)} 只ETF数据")
    
    # 分析每只ETF
    analysis_results = []
    
    for etf_data in etf_data_list:
        print(f"分析 {etf_data['name']}({etf_data['code']})...")
        
        # 市场情绪分析
        sentiment = analyze_market_sentiment(etf_data)
        print(f"  市场情绪: {sentiment['emoji']} {sentiment['sentiment']} (评分: {sentiment['score']})")
        
        # 交易信号
        signal = generate_trading_signal(etf_data, sentiment)
        print(f"  投资建议: {signal['action']} (置信度: {signal['confidence']}%)")
        
        # 风险识别
        risks = identify_risks(etf_data, sentiment, signal)
        print(f"  风险提示: {len(risks)} 项")
        
        analysis_results.append({
            'code': etf_data['code'],
            'name': etf_data['name'],
            'sentiment': sentiment,
            'signal': signal,
            'risks': risks,
            'realtime': etf_data['realtime'],
            'indicators': etf_data['indicators']
        })
    
    # AI深度分析
    ai_analysis = analyze_with_ai(etf_data_list)
    
    # 保存分析结果
    output = {
        'updated_at': datetime.now().isoformat(),
        'analysis': analysis_results,
        'ai_analysis': ai_analysis,
        'summary': {
            'total_etfs': len(analysis_results),
            'buy_count': sum(1 for r in analysis_results if r['signal']['action_code'] in ['buy', 'strong_buy']),
            'hold_count': sum(1 for r in analysis_results if r['signal']['action_code'] == 'hold'),
            'sell_count': sum(1 for r in analysis_results if r['signal']['action_code'] in ['sell', 'reduce'])
        }
    }
    
    output_file = 'data/etf_strategy.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 分析结果已保存到 {output_file}")
    print("" + "=" * 60)
    print("分析汇总")
    print("=" * 60)
    
    for result in analysis_results:
        print(f"{result['name']}({result['code']})")
        print(f"  当前价: {result['realtime']['current']}元 ({result['realtime']['change_percent']:+.2f}%)")
        print(f"  市场情绪: {result['sentiment']['emoji']} {result['sentiment']['sentiment']}")
        print(f"  投资建议: {result['signal']['action']}")
        print(f"  主要风险: {result['risks'][0]['description']}")
    
    print("=" * 60)

if __name__ == '__main__':
    main()

