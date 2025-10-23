import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# 新闻API配置（可选）
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

# RSS订阅源列表（完全免费，无需API密钥）
RSS_FEEDS = [
    {
        'url': 'https://feeds.bbci.co.uk/news/business/rss.xml',
        'source': 'BBC Business',
        'country': 'UK'
    },
    {
        'url': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
        'source': 'CNBC',
        'country': 'USA'
    },
    {
        'url': 'https://www.ft.com/?format=rss',
        'source': 'Financial Times',
        'country': 'UK'
    },
    {
        'url': 'https://www.bloomberg.com/feed/podcast/etf-report.xml',
        'source': 'Bloomberg',
        'country': 'USA'
    }
]

def fetch_from_rss(feed_url: str, source: str, country: str) -> List[Dict]:
    """从RSS订阅源获取新闻"""
    news_list = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(feed_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 解析RSS XML
            root = ET.fromstring(response.content)
            
            # 查找所有item标签
            items = root.findall('.//item')
            
            for item in items[:10]:  # 每个源取10条
                try:
                    title = item.find('title').text if item.find('title') is not None else ''
                    description = item.find('description').text if item.find('description') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    
                    # 清理HTML标签
                    if description:
                        soup = BeautifulSoup(description, 'html.parser')
                        description = soup.get_text().strip()
                    
                    # 转换日期格式
                    try:
                        if pub_date:
                            pub_date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                            pub_date = pub_date_obj.isoformat()
                    except:
                        pub_date = datetime.now().isoformat()
                    
                    news_item = {
                        'id': hash(link),
                        'title': title,
                        'description': description[:300] if description else '',
                        'url': link,
                        'source': source,
                        'published_at': pub_date,
                        'category': categorize_news(title + ' ' + description),
                        'country': country,
                        'image_url': get_placeholder_image(),
                        'fetched_at': datetime.now().isoformat()
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    print(f"解析RSS项目时出错: {str(e)}")
                    continue
            
            print(f"从 {source} 获取到 {len(news_list)} 条新闻")
            
    except Exception as e:
        print(f"获取RSS订阅源失败 ({source}): {str(e)}")
    
    return news_list

def fetch_from_google_news() -> List[Dict]:
    """从Google News爬取经济新闻"""
    news_list = []
    
    try:
        # Google News RSS - 商业类别
        url = 'https://news.google.com/rss/search?q=economy+OR+stock+market+OR+GDP+OR+inflation&hl=en-US&gl=US&ceid=US:en'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            for item in items[:15]:  # 取15条
                try:
                    title = item.find('title').text if item.find('title') is not None else ''
                    description = item.find('description').text if item.find('description') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    
                    # 清理HTML
                    if description:
                        soup = BeautifulSoup(description, 'html.parser')
                        description = soup.get_text().strip()
                    
                    # 转换日期
                    try:
                        if pub_date:
                            pub_date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                            pub_date = pub_date_obj.isoformat()
                    except:
                        pub_date = datetime.now().isoformat()
                    
                    news_item = {
                        'id': hash(link),
                        'title': title,
                        'description': description[:300] if description else '',
                        'url': link,
                        'source': 'Google News',
                        'published_at': pub_date,
                        'category': categorize_news(title + ' ' + description),
                        'country': 'Global',
                        'image_url': get_placeholder_image(),
                        'fetched_at': datetime.now().isoformat()
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    print(f"解析Google News项目时出错: {str(e)}")
                    continue
            
            print(f"从 Google News 获取到 {len(news_list)} 条新闻")
            
    except Exception as e:
        print(f"获取Google News失败: {str(e)}")
    
    return news_list

def fetch_from_yahoo_finance() -> List[Dict]:
    """从Yahoo Finance爬取新闻"""
    news_list = []
    
    try:
        # Yahoo Finance RSS
        url = 'https://finance.yahoo.com/news/rssindex'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            for item in items[:10]:
                try:
                    title = item.find('title').text if item.find('title') is not None else ''
                    description = item.find('description').text if item.find('description') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    
                    if description:
                        soup = BeautifulSoup(description, 'html.parser')
                        description = soup.get_text().strip()
                    
                    try:
                        if pub_date:
                            pub_date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                            pub_date = pub_date_obj.isoformat()
                    except:
                        pub_date = datetime.now().isoformat()
                    
                    news_item = {
                        'id': hash(link),
                        'title': title,
                        'description': description[:300] if description else '',
                        'url': link,
                        'source': 'Yahoo Finance',
                        'published_at': pub_date,
                        'category': categorize_news(title + ' ' + description),
                        'country': 'USA',
                        'image_url': get_placeholder_image(),
                        'fetched_at': datetime.now().isoformat()
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    print(f"解析Yahoo Finance项目时出错: {str(e)}")
                    continue
            
            print(f"从 Yahoo Finance 获取到 {len(news_list)} 条新闻")
            
    except Exception as e:
        print(f"获取Yahoo Finance失败: {str(e)}")
    
    return news_list

def fetch_economic_news() -> List[Dict]:
    """从多个来源获取经济新闻"""
    print("开始获取经济新闻...")
    
    all_news = []
    
    # 1. 从Google News获取
    print("\n[1/3] 从 Google News 获取...")
    google_news = fetch_from_google_news()
    all_news.extend(google_news)
    time.sleep(2)
    
    # 2. 从Yahoo Finance获取
    print("\n[2/3] 从 Yahoo Finance 获取...")
    yahoo_news = fetch_from_yahoo_finance()
    all_news.extend(yahoo_news)
    time.sleep(2)
    
    # 3. 从RSS订阅源获取
    print("\n[3/3] 从 RSS 订阅源获取...")
    for feed in RSS_FEEDS:
        try:
            rss_news = fetch_from_rss(feed['url'], feed['source'], feed['country'])
            all_news.extend(rss_news)
            time.sleep(1)
        except Exception as e:
            print(f"RSS订阅源 {feed['source']} 失败: {str(e)}")
            continue
    
    # 去重（基于URL）
    seen_urls = set()
    unique_news = []
    for news in all_news:
        if news['url'] not in seen_urls:
            seen_urls.add(news['url'])
            unique_news.append(news)
    
    # 按发布时间排序
    unique_news.sort(key=lambda x: x['published_at'], reverse=True)
    
    print(f"\n总共获取 {len(unique_news)} 条去重后的新闻")
    return unique_news

def categorize_news(text: str) -> str:
    """根据文本内容分类新闻"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['fed', 'central bank', 'interest rate', 'monetary', 'ecb', 'pboc']):
        return '货币政策'
    elif any(word in text_lower for word in ['gdp', 'growth', 'inflation', 'unemployment', 'cpi', 'ppi']):
        return '经济数据'
    elif any(word in text_lower for word in ['stock', 'market', 'trading', 'shares', 'dow', 'nasdaq', 's&p']):
        return '股市动态'
    elif any(word in text_lower for word in ['oil', 'gold', 'commodity', 'crude', 'silver', 'copper']):
        return '大宗商品'
    elif any(word in text_lower for word in ['currency', 'forex', 'exchange rate', 'dollar', 'euro', 'yuan']):
        return '外汇市场'
    elif any(word in text_lower for word in ['crypto', 'bitcoin', 'blockchain', 'ethereum']):
        return '数字货币'
    elif any(word in text_lower for word in ['trade', 'tariff', 'export', 'import', 'wto']):
        return '国际贸易'
    else:
        return '综合财经'

def get_placeholder_image() -> str:
    """获取占位图片"""
    images = [
        'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/c114dc3c-72a6-44d4-93a8-b97d0608ad58/image_1761210122_4_1.png',
        'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/5f2cdbe0-ff90-4dd6-847d-f845db12d841/image_1761210122_6_1.jpg',
        'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/d73313bb-1da1-4247-8ca6-de693c674018/image_1761210124_5_1.png',
        'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/e21eb98a-5751-440c-8dc6-b04471809fc8/image_1761210124_7_1.png'
    ]
    import random
    return random.choice(images)

def analyze_with_ai(news_list: List[Dict]) -> Dict:
    """使用AI分析投资温度"""
    print("\n开始AI分析...")
    
    # 简化的情感分析（基于关键词）
    positive_keywords = [
        'surge', 'rise', 'gain', 'growth', 'increase', 'boost', 'rally',
        'positive', 'optimistic', 'strong', 'recovery', 'improve', 'beat',
        'up', 'higher', 'advance', 'jump', 'soar', 'climb'
    ]
    
    negative_keywords = [
        'fall', 'drop', 'decline', 'decrease', 'loss', 'crash', 'plunge',
        'negative', 'pessimistic', 'weak', 'recession', 'concern', 'miss',
        'down', 'lower', 'tumble', 'sink', 'slump', 'slide'
    ]
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    key_factors = []
    
    for news in news_list[:30]:  # 分析最新30条
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
    
    # 计算投资温度分数
    total = positive_count + negative_count + neutral_count
    if total > 0:
        temperature_score = ((positive_count * 1.0 + neutral_count * 0.5) / total) * 100
    else:
        temperature_score = 50.0
    
    # 确定情绪和分析文本
    if temperature_score >= 70:
        sentiment = "乐观"
        sentiment_emoji = "😊"
        analysis_text = f"当前全球经济新闻整体偏向积极（积极新闻占比{positive_count}/{total}），市场情绪乐观。多项经济指标表现良好，投资者信心较强。建议适度增加风险资产配置，关注科技、消费等成长性板块。"
    elif temperature_score >= 50:
        sentiment = "中性"
        sentiment_emoji = "😐"
        analysis_text = f"当前全球经济新闻喜忧参半（积极{positive_count}条，消极{negative_count}条），市场情绪相对中性。经济数据有好有坏，建议保持均衡配置，关注市场变化，适时调整投资组合。"
    else:
        sentiment = "谨慎"
        sentiment_emoji = "😟"
        analysis_text = f"当前全球经济新闻偏向消极（消极新闻占比{negative_count}/{total}），市场存在较多不确定性。建议降低风险敞口，增加防御性资产配置，如债券、黄金等避险资产。"
    
    analysis_result = {
        'temperature_score': round(temperature_score, 2),
        'sentiment': sentiment,
        'sentiment_emoji': sentiment_emoji,
        'analysis_text': analysis_text,
        'key_factors': key_factors,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'analyzed_news_count': total,
        'analyzed_at': datetime.now().isoformat(),
        'categories_distribution': get_category_distribution(news_list)
    }
    
    print(f"分析完成: 温度={temperature_score:.1f}°, 情绪={sentiment}")
    return analysis_result

def get_category_distribution(news_list: List[Dict]) -> Dict[str, int]:
    """统计新闻分类分布"""
    distribution = {}
    for news in news_list:
        category = news.get('category', '其他')
        distribution[category] = distribution.get(category, 0) + 1
    return distribution

def save_data(news_list: List[Dict], analysis: Dict):
    """保存数据到JSON文件"""
    os.makedirs('data', exist_ok=True)
    
    # 保存新闻数据
    with open('data/news.json', 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': datetime.now().isoformat(),
            'total_count': len(news_list),
            'news': news_list
        }, f, ensure_ascii=False, indent=2)
    
    # 保存分析结果
    with open('data/analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 数据已保存到 data/ 目录")

def main():
    """主函数"""
    print("=" * 60)
    print("全球经济新闻爬取与分析任务")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取新闻
    news_list = fetch_economic_news()
    
    if not news_list:
        print("\n⚠️  未获取到新闻数据，使用模拟数据")
        news_list = generate_mock_news()
    
    # AI分析
    analysis = analyze_with_ai(news_list)
    
    # 保存数据
    save_data(news_list, analysis)
    
    print("\n" + "=" * 60)
    print("✅ 任务完成!")
    print(f"📰 获取新闻: {len(news_list)} 条")
    print(f"🌡️  投资温度: {analysis['temperature_score']:.1f}°")
    print(f"😊 市场情绪: {analysis['sentiment']}")
    print("=" * 60)

def generate_mock_news() -> List[Dict]:
    """生成模拟新闻数据（备用）"""
    mock_news = [
        {
            'id': 1,
            'title': 'Federal Reserve Maintains Interest Rates, Markets React Positively',
            'description': 'The Federal Reserve announced it will maintain benchmark interest rates at 5.25%-5.50%, in line with market expectations. Major US stock indices rose collectively.',
            'url': 'https://example.com/news1',
            'source': 'Wall Street Journal',
            'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
            'category': '货币政策',
            'country': 'USA',
            'image_url': 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/c114dc3c-72a6-44d4-93a8-b97d0608ad58/image_1761210122_4_1.png',
            'fetched_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'title': 'China GDP Growth Exceeds Expectations, Strong Economic Recovery',
            'description': 'China Q3 GDP grew 5.2% year-on-year, exceeding market expectations of 4.8%. Both consumption and investment showed improvement.',
            'url': 'https://example.com/news2',
            'source': 'Reuters',
            'published_at': (datetime.now() - timedelta(hours=5)).isoformat(),
            'category': '经济数据',
            'country': 'China',
            'image_url': 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/5f2cdbe0-ff90-4dd6-847d-f845db12d841/image_1761210122_6_1.jpg',
            'fetched_at': datetime.now().isoformat()
        },
        {
            'id': 3,
            'title': 'European Central Bank Hints at Possible Rate Cut, Euro Under Pressure',
            'description': 'ECB President Lagarde indicated the central bank may consider rate cuts if inflation continues to decline. EUR/USD fell 0.8%.',
            'url': 'https://example.com/news3',
            'source': 'Financial Times',
            'published_at': (datetime.now() - timedelta(hours=8)).isoformat(),
            'category': '货币政策',
            'country': 'EU',
            'image_url': 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/d73313bb-1da1-4247-8ca6-de693c674018/image_1761210124_5_1.png',
            'fetched_at': datetime.now().isoformat()
        },
        {
            'id': 4,
            'title': 'Global Tech Stocks Rally on AI Breakthrough News',
            'description': 'Global tech stocks rose collectively on AI technology breakthrough news. Nvidia, Microsoft and other tech giants hit record highs.',
            'url': 'https://example.com/news4',
            'source': 'CNBC',
            'published_at': (datetime.now() - timedelta(hours=12)).isoformat(),
            'category': '股市动态',
            'country': 'Global',
            'image_url': 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/e21eb98a-5751-440c-8dc6-b04471809fc8/image_1761210124_7_1.png',
            'fetched_at': datetime.now().isoformat()
        },
        {
            'id': 5,
            'title': 'Oil Prices Drop Sharply on Global Growth Concerns',
            'description': 'International oil prices fell more than 3% in a single day on concerns about slowing global economic growth. Energy stocks declined broadly.',
            'url': 'https://example.com/news5',
            'source': 'Bloomberg',
            'published_at': (datetime.now() - timedelta(hours=18)).isoformat(),
            'category': '大宗商品',
            'country': 'Global',
            'image_url': 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/c114dc3c-72a6-44d4-93a8-b97d0608ad58/image_1761210122_4_1.png',
            'fetched_at': datetime.now().isoformat()
        },
        {
            'id': 6,
            'title': 'UK Inflation Rate Falls to 2.5%, Below Expectations',
            'description': 'UK CPI rose 2.5% year-on-year in October, below market expectations of 2.8%. Expectations for Bank of England rate cuts increased.',
            'url': 'https://example.com/news6',
            'source': 'BBC',
            'published_at': (datetime.now() - timedelta(hours=24)).isoformat(),
            'category': '经济数据',
            'country': 'UK',
            'image_url': 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/5f2cdbe0-ff90-4dd6-847d-f845db12d841/image_1761210122_6_1.jpg',
            'fetched_at': datetime.now().isoformat()
        }
    ]
    return mock_news

if __name__ == '__main__':
    main()
