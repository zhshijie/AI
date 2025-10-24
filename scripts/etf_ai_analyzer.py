#!/usr/bin/env python3
"""
ETF AI 分析器
专门用于 ETF 投资策略的 AI 深度分析
"""

import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Optional

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from ai_analyzer import get_analyzer


class ETFAIAnalyzer:
    """ETF AI 分析器类"""
    
    def __init__(self, provider: str = None):
        """
        初始化 ETF AI 分析器
        
        Args:
            provider: AI 提供商 ('groq', 'openrouter', 'deepseek')
        """
        self.provider = provider or os.getenv('AI_PROVIDER', 'groq')
        self.analyzer = None
        self.available = False
        
        try:
            self.analyzer = get_analyzer(self.provider)
            self.available = not self.analyzer.use_fallback
        except Exception as e:
            print(f"⚠️  初始化 AI 分析器失败: {e}")
            self.available = False
    
    def is_available(self) -> bool:
        """检查 AI 服务是否可用"""
        return self.available
    
    def prepare_prompt(self, etf_data_list: List[Dict]) -> str:
        """
        准备 AI 分析提示词
        
        Args:
            etf_data_list: ETF 数据列表
            
        Returns:
            str: 格式化的提示词
        """
        prompt = "# ETF投资分析报告\n"
        prompt += f"分析时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}\n"
        
        for etf_data in etf_data_list:
            realtime = etf_data['realtime']
            indicators = etf_data['indicators']
            news = etf_data.get('news', [])
            
            prompt += f"## {etf_data['name']}({etf_data['code']})\n"
            
            # 实时行情
            prompt += f"### 实时行情\n"
            prompt += f"- 当前价: {realtime['current']}元\n"
            prompt += f"- 涨跌幅: {realtime['change_percent']}%\n"
            prompt += f"- 成交量: {realtime['volume']}手\n"
            prompt += f"- 最高价: {realtime['high']}元\n"
            prompt += f"- 最低价: {realtime['low']}元\n"
            
            # 技术指标
            prompt += f"### 技术指标\n"
            prompt += f"- RSI(14): {indicators.get('rsi', 0)}\n"
            prompt += f"- MA5: {indicators.get('ma5', 0)}\n"
            prompt += f"- MA10: {indicators.get('ma10', 0)}\n"
            prompt += f"- MA20: {indicators.get('ma20', 0)}\n"
            
            macd = indicators.get('macd', {})
            prompt += f"- MACD: DIF={macd.get('dif', 0)}, DEA={macd.get('dea', 0)}\n"
            
            bollinger = indicators.get('bollinger', {})
            prompt += f"- 布林带: 上轨={bollinger.get('upper', 0)}, "
            prompt += f"中轨={bollinger.get('middle', 0)}, "
            prompt += f"下轨={bollinger.get('lower', 0)}\n"
            prompt += f"- 成交量变化: {indicators.get('volume_change', 0)}%\n"
            
            # 相关新闻
            if news:
                prompt += f"### 相关新闻 (最近{len(news)}条)\n"
                for i, item in enumerate(news[:5], 1):
                    prompt += f"{i}. {item['title']}\n"
                prompt += "\n"
        
        # 分析要求
        prompt += "请作为专业的投资分析师，基于以上数据，为每只ETF提供：\n"
        prompt += "1. 市场情绪分析（看多/看空/中性）\n"
        prompt += "2. 投资建议（买入/持有/卖出）及理由\n"
        prompt += "3. 关键风险提示\n"
        prompt += "4. 操作策略建议\n"
        prompt += "请用专业、客观的语言，给出具体可操作的建议。"
        
        return prompt
    
    def analyze(self, etf_data_list: List[Dict]) -> Optional[Dict]:
        """
        使用 AI 进行 ETF 投资分析
        
        Args:
            etf_data_list: ETF 数据列表
            
        Returns:
            Dict: AI 分析结果，包含 analysis_text, provider, model
            None: 分析失败
        """
        if not self.available:
            print("  ⚠️  AI 服务不可用")
            return None
        
        try:
            print(f"尝试使用 {self.provider} AI 进行深度分析...")
            print(f"✓ 使用 {self.provider} AI 服务进行分析")
            
            # 准备提示词
            prompt = self.prepare_prompt(etf_data_list)
            
            # 构建消息
            messages = [
                {
                    'role': 'system',
                    'content': '你是一位资深的ETF投资分析师，擅长技术分析和市场研判。'
                               '请基于提供的数据，给出专业、客观、可操作的投资建议。'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
            
            # 调用 AI API
            result = self._call_api(messages)
            
            if result:
                print("✓ AI分析完成")
                return result
            else:
                print("  ❌ AI分析失败")
                return None
                
        except Exception as e:
            print(f"  ❌ AI分析出错: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _call_api(self, messages: List[Dict]) -> Optional[Dict]:
        """
        调用 AI API
        
        Args:
            messages: 消息列表
            
        Returns:
            Dict: API 响应结果
            None: 调用失败
        """
        try:
            print(f"  正在调用 {self.provider} AI API...")
            
            # 准备请求头
            headers = {
                'Authorization': f'Bearer {self.analyzer.api_key}',
                'Content-Type': 'application/json'
            }
            
            # 根据不同的提供商设置不同的请求头
            if self.provider == 'openrouter':
                headers['HTTP-Referer'] = self.analyzer.config.get(
                    'site_url', 'https://github.com'
                )
                headers['X-Title'] = self.analyzer.config.get(
                    'site_name', 'ETF Investment Analyzer'
                )
            
            # 准备请求体
            payload = {
                'model': self.analyzer.config['model'],
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 3000
            }
            
            print(f"API URL: {self.analyzer.config['api_url']}")
            print(f"Model: {self.analyzer.config['model']}")
            
            # 发送请求
            response = requests.post(
                self.analyzer.config['api_url'],
                headers=headers,
                json=payload,
                timeout=60
            )
            
            print(f"响应状态码: {response.status_code}")
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    print(f"✓ 获取到AI响应内容，长度: {len(content)} 字符")
                    
                    # 返回 Markdown 格式的文本分析
                    return {
                        'analysis_text': content,
                        'provider': self.provider,
                        'model': self.analyzer.config['model']
                    }
                else:
                    print(f"❌ API响应格式错误")
                    print(f"响应内容: {result}")
                    return None
            else:
                print(f"❌ API请求失败: {response.status_code}")
                if response.text:
                    print(f"错误信息: {response.text[:500]}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ API请求超时")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ API请求异常: {e}")
            return None
        except Exception as e:
            print(f"❌ API调用失败: {e}")
            import traceback
            traceback.print_exc()
            return None


def analyze_etf_with_ai(etf_data_list: List[Dict], provider: str = None) -> Optional[Dict]:
    """
    便捷函数：使用 AI 分析 ETF 数据
    
    Args:
        etf_data_list: ETF 数据列表
        provider: AI 提供商（可选）
        
    Returns:
        Dict: AI 分析结果
        None: 分析失败
    """
    analyzer = ETFAIAnalyzer(provider)
    
    if not analyzer.is_available():
        print("⚠️  AI 服务不可用，请配置 API 密钥")
        print("   export GROQ_API_KEY='your-api-key'")
        print("   export AI_PROVIDER='groq'")
        return None
    
    return analyzer.analyze(etf_data_list)


# 测试代码
if __name__ == '__main__':
    print("=" * 60)
    print("ETF AI 分析器测试")
    print("=" * 60)
    print()
    
    # 测试数据
    test_etf_data = [
        {
            'code': '562500',
            'name': '机器人ETF',
            'realtime': {
                'current': 1.024,
                'change_percent': 1.49,
                'volume': 150000,
                'high': 1.035,
                'low': 1.015
            },
            'indicators': {
                'rsi': 41.39,
                'ma5': 1.008,
                'ma10': 1.015,
                'ma20': 1.049,
                'macd': {'dif': -0.005, 'dea': -0.008},
                'bollinger': {'upper': 1.080, 'middle': 1.025, 'lower': 0.967},
                'volume_change': 69.97
            },
            'news': []
        }
    ]
    
    # 测试分析
    result = analyze_etf_with_ai(test_etf_data)
    
    if result:
        print("=" * 60)
        print("✅ AI 分析成功")
        print("=" * 60)
        print(f"提供商: {result['provider']}")
        print(f"模型: {result['model']}")
        print(f"分析内容:")
        print(result['analysis_text'][:500] + "...")
    else:
        print("=" * 60)
        print("❌ AI 分析失败")
        print("=" * 60)
        print("请检查:")
        print("1. 是否配置了 API 密钥")
        print("2. 网络连接是否正常")
        print("3. API 配额是否充足")

