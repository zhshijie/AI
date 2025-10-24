"""
AI新闻分析模块
使用免费的AI API进行智能新闻分析和投资建议生成
"""

import requests
import json
import os
from typing import List, Dict
import time

# 支持多个免费AI服务
AI_PROVIDERS = {
    'groq': {
        'api_url': 'https://api.groq.com/openai/v1/chat/completions',
        'api_key_env': 'GROQ_API_KEY',
        'model': 'llama-3.1-70b-versatile',
        'free': True
    },
    'openrouter': {
        'api_url': 'https://openrouter.ai/api/v1/chat/completions',
        'api_key_env': 'OPENROUTER_API_KEY',
        'model': 'deepseek/deepseek-r1:free',  # 更新为2025年可用的免费模型
        'free': True,
        'site_url': 'https://github.com',
        'site_name': 'Economic News Analyzer'
    },
    'deepseek': {
        'api_url': 'https://api.deepseek.com/v1/chat/completions',
        'api_key_env': 'DEEPSEEK_API_KEY',
        'model': 'deepseek-chat',
        'free': False  # 需要付费，但价格很低
    }
}

class AINewsAnalyzer:
    """AI新闻分析器"""
    
    def __init__(self, provider='groq'):
        """
        初始化AI分析器
        
        Args:
            provider: AI服务提供商 ('groq', 'openrouter', 'deepseek')
        """
        self.provider = provider
        self.config = AI_PROVIDERS.get(provider)
        
        if not self.config:
            raise ValueError(f"不支持的AI提供商: {provider}")
        
        # 从环境变量获取API密钥
        self.api_key = os.getenv(self.config['api_key_env'], '')
        
        if not self.api_key:
            print(f"⚠️  未设置 {self.config['api_key_env']} 环境变量，将使用备用分析方法")
            self.use_fallback = True
        else:
            self.use_fallback = False
            print(f"✓ 使用 {provider} AI 服务进行分析")
    
    def analyze_news(self, news_list: List[Dict]) -> Dict:
        """
        分析新闻列表，生成投资建议
        
        Args:
            news_list: 新闻列表
            
        Returns:
            分析结果字典
        """
        if self.use_fallback or not self.api_key:
            print("使用备用分析方法（基于规则）")
            return self._fallback_analysis(news_list)
        
        try:
            # 准备新闻摘要
            news_summary = self._prepare_news_summary(news_list[:30])
            
            # 调用AI进行分析
            analysis_result = self._call_ai_api(news_summary)
            
            if analysis_result:
                print("✓ AI分析完成")
                return analysis_result
            else:
                print("AI分析失败，使用备用方法")
                return self._fallback_analysis(news_list)
                
        except Exception as e:
            print(f"AI分析出错: {str(e)}，使用备用方法")
            return self._fallback_analysis(news_list)
    
    def _prepare_news_summary(self, news_list: List[Dict]) -> str:
        """准备新闻摘要文本"""
        summary_parts = []
        
        for i, news in enumerate(news_list, 1):
            title = news.get('title', '')
            description = news.get('description', '')
            category = news.get('category', '')
            source = news.get('source', '')
            
            summary_parts.append(
                f"{i}. [{category}] {title}"
                f"   来源: {source}"
                f"   摘要: {description[:150]}"
            )
        
        return "\n".join(summary_parts)
    
    def _call_ai_api(self, news_summary) -> Dict:
        """调用AI API进行分析
        
        Args:
            news_summary: 可以是字符串（新闻摘要）或列表（消息列表）
        """
        
        # 判断 news_summary 的类型
        if isinstance(news_summary, list):
            # 如果是列表，说明是直接传入的 messages
            messages = news_summary
            news_count = 0  # 无法从 messages 中准确计算新闻数量
        else:
            # 如果是字符串，构建标准的 prompt
            prompt = f"""
【新闻摘要】
{news_summary}

【分析要求】
请从以下几个维度进行分析：
1. 整体市场情绪（乐观/中性/谨慎）
2. 投资温度评分（0-100分，分数越高表示投资价值越高）
3. 关键影响因素（列出3-5个最重要的因素）
4. 积极因素和消极因素的数量统计
5. 详细的投资建议和风险提示

【输出格式】
请严格按照以下JSON格式输出（不要包含任何其他文字）：
{{
  "temperature_score": 75.5,
  "sentiment": "乐观",
  "sentiment_emoji": "😊",
  "analysis_text": "详细的分析文本，至少200字...",
  "key_factors": [
    "✓ 因素1: 描述...",
    "✗ 因素2: 描述...",
    "✓ 因素3: 描述..."
  ],
  "positive_count": 15,
  "negative_count": 8,
  "neutral_count": 7,
  "investment_advice": {{
    "short_term": "短期投资建议...",
    "medium_term": "中期投资建议...",
    "risk_warning": "风险提示..."
  }}
}}

注意：
- temperature_score范围0-100，70以上为乐观，50-70为中性，50以下为谨慎
- sentiment只能是"乐观"、"中性"或"谨慎"
- sentiment_emoji对应：乐观😊、中性😐、谨慎😟
- key_factors用✓表示积极因素，✗表示消极因素
- analysis_text要详细、专业，至少200字
"""
            messages = [
                {
                    'role': 'system',
                    'content': '你是一位专业的金融分析师，擅长分析全球经济新闻并给出投资建议。'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
            # 计算新闻数量
            news_count = len(news_summary.split('\n')) if isinstance(news_summary, str) else 0

        content = None  # 初始化 content 变量
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # 根据不同的提供商设置不同的请求头
            if self.provider == 'openrouter':
                headers['HTTP-Referer'] = self.config.get('site_url', 'https://github.com')
                headers['X-Title'] = self.config.get('site_name', 'Economic News Analyzer')
            
            payload = {
                'model': self.config['model'],
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 2000
            }
            
            print(f"正在调用 {self.provider} AI API...")
            print(f"API URL: {self.config['api_url']}")
            print(f"Model: {self.config['model']}")
            
            response = requests.post(
                self.config['api_url'],
                headers=headers,
                json=payload,
                timeout=60
            )
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    
                    # 检查响应结构
                    if 'choices' not in result or len(result['choices']) == 0:
                        print(f"❌ API响应格式错误: 缺少 choices 字段")
                        print(f"完整响应: {json.dumps(result, indent=2, ensure_ascii=False)[:1000]}")
                        return None
                    
                    content = result['choices'][0]['message']['content']
                    print(f"✓ 获取到AI响应内容，长度: {len(content)} 字符")
                    
                    # 提取JSON内容
                    content = content.strip()
                    
                    # 尝试多种方式提取JSON
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        content = content.split('```')[1].split('```')[0].strip()
                    
                    # 如果内容以 { 开头但不完整，尝试找到完整的JSON
                    if content.startswith('{') and not content.endswith('}'):
                        print(f"⚠️  检测到不完整的JSON响应")
                        # 尝试找到最后一个完整的 }
                        last_brace = content.rfind('}')
                        if last_brace > 0:
                            content = content[:last_brace + 1]
                            print(f"✓ 修复后的内容长度: {len(content)} 字符")
                    
                    print(f"准备解析的JSON内容（前200字符）: {content[:200]}")
                    
                    # 解析JSON
                    analysis_data = json.loads(content)
                    
                    # 验证必需字段
                    required_fields = ['temperature_score', 'sentiment', 'analysis_text']
                    missing_fields = [f for f in required_fields if f not in analysis_data]
                    if missing_fields:
                        print(f"❌ 缺少必需字段: {missing_fields}")
                        return None
                    
                    # 添加元数据
                    from datetime import datetime
                    analysis_data['analyzed_at'] = datetime.now().isoformat()
                    # 修复：根据 news_summary 的类型来计算新闻数量
                    if isinstance(news_summary, str):
                        analysis_data['analyzed_news_count'] = len(news_summary.split('\n'))
                    else:
                        # 如果是列表，尝试从 analysis_data 中获取，或设为0
                        analysis_data['analyzed_news_count'] = analysis_data.get('analyzed_news_count', 0)
                    analysis_data['ai_provider'] = self.provider
                    
                    print(f"✓ JSON解析成功，温度评分: {analysis_data.get('temperature_score')}")
                    return analysis_data
                    
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {str(e)}")
                    if content:
                        print(f"AI返回内容（前500字符）: {content[:500]}")
                        print(f"AI返回内容（后100字符）: {content[-100:]}")
                    else:
                        print(f"AI返回的原始响应: {response.text[:1000]}")
                    return None
                    
            else:
                print(f"❌ API请求失败: {response.status_code}")
                print(f"错误详情: {response.text[:500]}")
                print(f"请求URL: {self.config['api_url']}")
                print(f"使用模型: {self.config['model']}")
                
                if response.status_code == 404:
                    print("可能的原因:")
                    print("1. API URL 不正确")
                    print("2. 模型名称不正确或不可用")
                    print("3. API 端点已更改")
                    print("建议:")
                    print("- 运行测试脚本: python test_openrouter_debug.py")
                    print("- 或切换到 Groq: export AI_PROVIDER='groq'")
                elif response.status_code == 401:
                    print("认证失败，请检查API密钥是否正确")
                elif response.status_code == 429:
                    print("请求过于频繁，请稍后再试")
                
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ API请求超时（60秒）")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"❌ 网络连接错误: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ API调用失败: {type(e).__name__}: {str(e)}")
            import traceback
            print(f"详细错误信息:{traceback.format_exc()}")
            return None
    
    def _fallback_analysis(self, news_list: List[Dict]) -> Dict:
        """备用分析方法（基于规则）"""
        print("使用基于规则的备用分析方法")
        
        # 关键词列表
        positive_keywords = [
            'surge', 'rise', 'gain', 'growth', 'increase', 'boost', 'rally',
            'positive', 'optimistic', 'strong', 'recovery', 'improve', 'beat',
            'up', 'higher', 'advance', 'jump', 'soar', 'climb', 'exceed'
        ]
        
        negative_keywords = [
            'fall', 'drop', 'decline', 'decrease', 'loss', 'crash', 'plunge',
            'negative', 'pessimistic', 'weak', 'recession', 'concern', 'miss',
            'down', 'lower', 'tumble', 'sink', 'slump', 'slide', 'worry'
        ]
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        key_factors = []
        
        # 分析每条新闻
        for news in news_list[:30]:
            text = (news.get('title', '') + ' ' + news.get('description', '')).lower()
            
            pos_score = sum(1 for word in positive_keywords if word in text)
            neg_score = sum(1 for word in negative_keywords if word in text)
            
            if pos_score > neg_score:
                positive_count += 1
                if len(key_factors) < 5:
                    key_factors.append(f"✓ {news['category']}: {news['title'][:60]}...")
            elif neg_score > pos_score:
                negative_count += 1
                if len(key_factors) < 5:
                    key_factors.append(f"✗ {news['category']}: {news['title'][:60]}...")
            else:
                neutral_count += 1
        
        # 计算投资温度
        total = positive_count + negative_count + neutral_count
        if total > 0:
            temperature_score = ((positive_count * 1.0 + neutral_count * 0.5) / total) * 100
        else:
            temperature_score = 50.0
        
        # 确定情绪
        if temperature_score >= 70:
            sentiment = "乐观"
            sentiment_emoji = "😊"
            analysis_text = f"当前全球经济新闻整体偏向积极（积极{positive_count}条，消极{negative_count}条），市场情绪乐观。多项经济指标表现良好，投资者信心较强。建议适度增加风险资产配置，关注科技、消费等成长性板块。同时注意控制仓位，设置止损点位。"
        elif temperature_score >= 50:
            sentiment = "中性"
            sentiment_emoji = "😐"
            analysis_text = f"当前全球经济新闻喜忧参半（积极{positive_count}条，消极{negative_count}条），市场情绪相对中性。部分积极因素提振市场信心，但也存在一些不确定性。建议保持均衡配置，关注市场变化，适时调整投资组合。"
        else:
            sentiment = "谨慎"
            sentiment_emoji = "😟"
            analysis_text = f"当前全球经济新闻偏向消极（积极{positive_count}条，消极{negative_count}条），市场情绪谨慎。多项不利因素影响市场信心，建议降低风险资产配置，增加防御性资产比重，密切关注市场动态。"
        
        # 统计分类分布
        categories_distribution = {}
        for news in news_list[:30]:
            category = news.get('category', '其他')
            categories_distribution[category] = categories_distribution.get(category, 0) + 1
        
        from datetime import datetime
        return {
            'temperature_score': round(temperature_score, 1),
            'sentiment': sentiment,
            'sentiment_emoji': sentiment_emoji,
            'analysis_text': analysis_text,
            'key_factors': key_factors,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'analyzed_news_count': min(30, len(news_list)),
            'analyzed_at': datetime.now().isoformat(),
            'categories_distribution': categories_distribution,
            'ai_provider': 'fallback_rules'
        }


def get_analyzer(provider='groq'):
    """
    获取AI分析器实例
    
    Args:
        provider: AI服务提供商
        
    Returns:
        AINewsAnalyzer实例
    """
    return AINewsAnalyzer(provider)


# 使用示例
if __name__ == '__main__':
    # 测试代码
    analyzer = get_analyzer('groq')
    
    # 模拟新闻数据
    test_news = [
        {
            'title': 'Federal Reserve Maintains Interest Rates',
            'description': 'The Fed keeps rates steady amid economic uncertainty',
            'category': '货币政策',
            'source': 'Reuters'
        }
    ]
    
    result = analyzer.analyze_news(test_news)
    print(json.dumps(result, indent=2, ensure_ascii=False))
