#!/usr/bin/env python3
"""
AI分析功能测试脚本
用于测试AI分析器是否正常工作
"""

import os
import sys
import json

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def test_ai_analyzer():
    """测试AI分析器"""
    print("=" * 60)
    print("AI新闻分析功能测试")
    print("=" * 60)
    
    # 检查环境变量
    print("\n[1/4] 检查环境变量...")
    
    providers = {
        'groq': 'GROQ_API_KEY',
        'openrouter': 'OPENROUTER_API_KEY',
        'deepseek': 'DEEPSEEK_API_KEY'
    }
    
    available_providers = []
    for provider, env_key in providers.items():
        api_key = os.getenv(env_key, '')
        if api_key:
            print(f"  ✓ {provider}: 已配置 ({env_key})")
            available_providers.append(provider)
        else:
            print(f"  ✗ {provider}: 未配置 ({env_key})")
    
    if not available_providers:
        print("⚠️  未配置任何AI服务，将使用备用分析方法")
        print("建议配置至少一个AI服务以获得更好的分析质量")
        print("推荐配置Groq（完全免费）：")
        print("1. 访问 https://console.groq.com/")
        print("2. 注册并获取API密钥")
        print("3. 设置环境变量：export GROQ_API_KEY='your-api-key'")
        print("继续使用备用分析方法进行测试...")
    
    # 导入分析器
    print("[2/4] 导入AI分析器...")
    try:
        from ai_analyzer import get_analyzer
        print("  ✓ AI分析器模块导入成功")
    except ImportError as e:
        print(f"  ✗ 导入失败: {str(e)}")
        return False
    
    # 准备测试数据
    print("[3/4] 准备测试数据...")
    test_news = [
        {
            'id': 1,
            'title': 'Federal Reserve Maintains Interest Rates, Markets React Positively',
            'description': 'The Federal Reserve announced it will maintain benchmark interest rates at 5.25%-5.50%, in line with market expectations. Major US stock indices rose collectively.',
            'category': '货币政策',
            'source': 'Reuters',
            'published_at': '2025-10-23T15:00:00Z'
        },
        {
            'id': 2,
            'title': 'China GDP Growth Exceeds Expectations, Strong Economic Recovery',
            'description': 'China\'s Q3 GDP grew 5.2% year-on-year, exceeding market expectations of 4.8%. Both consumption and investment showed improvement.',
            'category': '经济数据',
            'source': 'Bloomberg',
            'published_at': '2025-10-23T12:00:00Z'
        },
        {
            'id': 3,
            'title': 'Oil Prices Drop Sharply on Global Growth Concerns',
            'description': 'International oil prices fell more than 3% in a single day on concerns about slowing global economic growth.',
            'category': '大宗商品',
            'source': 'CNBC',
            'published_at': '2025-10-23T09:00:00Z'
        },
        {
            'id': 4,
            'title': 'Global Tech Stocks Rally on AI Breakthrough News',
            'description': 'Global tech stocks rose collectively on AI technology breakthrough news. Nvidia, Microsoft hit record highs.',
            'category': '股市动态',
            'source': 'Financial Times',
            'published_at': '2025-10-23T06:00:00Z'
        },
        {
            'id': 5,
            'title': 'European Central Bank Hints at Possible Rate Cut',
            'description': 'ECB President Lagarde indicated the central bank may consider rate cuts if inflation continues to decline.',
            'category': '货币政策',
            'source': 'BBC',
            'published_at': '2025-10-23T03:00:00Z'
        }
    ]
    print(f"  ✓ 准备了 {len(test_news)} 条测试新闻")
    
    # 执行分析
    print("[4/4] 执行AI分析...")
    
    # 确定使用哪个提供商
    if available_providers:
        provider = available_providers[0]
        print(f"  使用 {provider} 进行分析...")
    else:
        provider = 'groq'  # 默认，会自动降级到备用方法
        print("  使用备用分析方法...")
    
    try:
        analyzer = get_analyzer(provider)
        result = analyzer.analyze_news(test_news)
        
        print("" + "=" * 60)
        print("分析结果")
        print("=" * 60)
        
        # 显示关键指标
        print(f"📊 投资温度: {result.get('temperature_score', 0):.1f}°")
        print(f"😊 市场情绪: {result.get('sentiment', '未知')} {result.get('sentiment_emoji', '')}")
        print(f"📈 积极新闻: {result.get('positive_count', 0)} 条")
        print(f"📉 消极新闻: {result.get('negative_count', 0)} 条")
        print(f"📊 中性新闻: {result.get('neutral_count', 0)} 条")
        
        # 显示分析文本
        print(f"💡 分析结论:")
        analysis_text = result.get('analysis_text', '无')
        # 自动换行显示
        import textwrap
        wrapped_text = textwrap.fill(analysis_text, width=58)
        for line in wrapped_text.split(''):
            print(f"   {line}")
        
        # 显示关键因素
        print(f"\n🔑 关键因素:")
        key_factors = result.get('key_factors', [])
        for i, factor in enumerate(key_factors[:5], 1):
            if isinstance(factor, dict):
                factor_text = f"{factor.get('type', '?')} {factor.get('category', '')}: {factor.get('title', '')}"
            else:
                factor_text = str(factor)
            print(f"   {i}. {factor_text[:70]}")
        
        # 显示AI提供商
        ai_provider = result.get('ai_provider', 'unknown')
        print(f"🤖 分析引擎: {ai_provider}")
        
        # 保存结果
        output_file = 'test_analysis_result.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 完整结果已保存到: {output_file}")
        
        print("" + "=" * 60)
        print("✅ 测试完成！")
        print("=" * 60)
        
        # 给出建议
        if ai_provider == 'fallback_rules':
            print("💡 建议:")
            print("   当前使用的是备用分析方法（基于规则）")
            print("   建议配置AI服务以获得更专业的分析结果")
            print("   推荐使用Groq（完全免费）：https://console.groq.com/")
        else:
            print("🎉 恭喜！AI分析功能运行正常")
            print(f"   当前使用: {ai_provider}")
            print("   可以在GitHub Actions中使用此配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 分析失败: {str(e)}")
        import traceback
        print("详细错误信息:")
        traceback.print_exc()
        return False


def main():
    """主函数"""
    success = test_ai_analyzer()
    
    if success:
        print("" + "=" * 60)
        print("下一步操作")
        print("=" * 60)
        print("1. 如果测试成功，可以在GitHub仓库中配置相同的环境变量")
        print("   Settings → Secrets and variables → Actions → New repository secret")
        print("2. 运行完整的新闻爬取和分析:")
        print("   python scripts/fetch_news.py")
        print("3. 查看详细的AI配置指南:")
        print("   cat AI_ANALYSIS_GUIDE.md")
        sys.exit(0)
    else:
        print("" + "=" * 60)
        print("故障排查")
        print("=" * 60)
        print("1. 检查是否正确安装了依赖:")
        print("   pip install -r requirements.txt")
        print("2. 检查环境变量是否正确设置:")
        print("   echo $GROQ_API_KEY")
        print("3. 查看详细的故障排查指南:")
        print("   cat AI_ANALYSIS_GUIDE.md")
        sys.exit(1)


if __name__ == '__main__':
    main()

