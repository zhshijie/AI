import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# 腾讯相关关键词
TENCENT_KEYWORDS = [
    'Tencent', '腾讯', 'WeChat', '微信', 'QQ', 
    'Tencent Cloud', '腾讯云', 'Tencent Games', '腾讯游戏',
    'Honor of Kings', '王者荣耀', 'PUBG Mobile', '和平精英',
    'Tencent Music', '腾讯音乐', 'Tencent Video', '腾讯视频',
    'Tencent Holdings', '00700.HK', 'TCEHY'
]

# 相关行业关键词
INDUSTRY_KEYWORDS = [
    'gaming', 'game', '游戏', 'esports', '电竞',
    'social media', '社交媒体', 'messaging', '即时通讯',
    'cloud computing', '云计算', 'fintech', '金融科技',
    'digital payment', '数字支付', 'streaming', '流媒体',
    'AI', 'artificial intelligence', '人工智能',
    'metaverse', '元宇宙', 'VR', 'AR'
]

# RSS订阅源（聚焦科技和金融）
RSS_FEEDS = [
    {
        'url': 'https://feeds.bbci.co.uk/news/technology/rss.xml',
        'source': 'BBC Technology',
        'country': 'UK'
    },
    {
        'url': 'https://www.cnbc.com/id/19854910/device/rss/rss.html',
        'source': 'CNBC Technology',
        'country': 'USA'
    },
    {
        'url': 'https://feeds.reuters.com/reuters/technologyNews',
        'source': 'Reuters Technology',
        'country': 'Global'
    }
]

def fetch_from_google_news_tencent() -> List[Dict]:
    """从Google News获取腾讯相关新闻"""
    news_list = []
    
    try:
        # 搜索腾讯相关新闻
        search_query = 'Tencent OR 腾讯 OR WeChat OR 微信'
        url = f'https://news.google.com/rss/search?q={search_query}&hl=en-US&gl=US&ceid=US:en'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            for item in items[:15]:
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
                        'id': abs(hash(link)) % (10 ** 8),
                        'title': title,
                        'description': description[:300] if description else '',
                        'url': link,
                        'source': 'Google News',
                        'published_at': pub_date,
                        'category': categorize_tencent_news(title + ' ' + description),
                        'country': 'Global',
                        'image_url': get_placeholder_image(),
                        'fetched_at': datetime.now().isoformat(),
                        'relevance_score': calculate_relevance(title + ' ' + description)
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    print(f"解析Google News项目时出错: {str(e)}")
                    continue
            
            print(f"从 Google News 获取到 {len(news_list)} 条腾讯相关新闻")
            
    except Exception as e:
        print(f"获取Google News失败: {str(e)}")
    
    return news_list

def fetch_from_rss(feed_url: str, source: str, country: str) -> List[Dict]:
    """从RSS订阅源获取新闻并筛选腾讯相关"""
    news_list = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(feed_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            for item in items[:20]:
                try:
                    title = item.find('title').text if item.find('title') is not None else ''
                    description = item.find('description').text if item.find('description') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    
                    # 计算相关性
                    text = title + ' ' + description
                    relevance = calculate_relevance(text)
                    
                    # 只保留相关性较高的新闻
                    if relevance < 1:
                        continue
                    
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
                        'id': abs(hash(link)) % (10 ** 8),
                        'title': title,
                        'description': description[:300] if description else '',
                        'url': link,
                        'source': source,
                        'published_at': pub_date,
                        'category': categorize_tencent_news(text),
                        'country': country,
                        'image_url': get_placeholder_image(),
                        'fetched_at': datetime.now().isoformat(),
                        'relevance_score': relevance
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    print(f"解析RSS项目时出错: {str(e)}")
                    continue
            
            print(f"从 {source} 获取到 {len(news_list)} 条相关新闻")
            
    except Exception as e:
        print(f"获取RSS订阅源失败 ({source}): {str(e)}")
    
    return news_list

def calculate_relevance(text: str) -> int:
    """计算新闻与腾讯的相关性分数"""
    text_lower = text.lower()
    score = 0
    
    # 腾讯直接相关
    for keyword in TENCENT_KEYWORDS:
        if keyword.lower() in text_lower:
            score += 3
    
    # 行业相关
    for keyword in INDUSTRY_KEYWORDS:
        if keyword.lower() in text_lower:
            score += 1
    
    return score

def categorize_tencent_news(text: str) -> str:
    """根据文本内容分类腾讯相关新闻"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['game', 'gaming', '游戏', 'esports', '电竞', 'honor of kings', 'pubg']):
        return '游戏业务'
    elif any(word in text_lower for word in ['wechat', '微信', 'qq', 'social', '社交', 'messaging']):
        return '社交平台'
    elif any(word in text_lower for word in ['cloud', '云计算', 'tencent cloud', '腾讯云']):
        return '云服务'
    elif any(word in text_lower for word in ['fintech', '金融科技', 'payment', '支付', 'wepay']):
        return '金融科技'
    elif any(word in text_lower for word in ['music', '音乐', 'video', '视频', 'streaming', '流媒体']):
        return '数字内容'
    elif any(word in text_lower for word in ['ai', 'artificial intelligence', '人工智能', 'machine learning']):
        return 'AI技术'
    elif any(word in text_lower for word in ['stock', 'share', '股价', 'market cap', '市值', 'earnings', '财报']):
        return '股市表现'
    elif any(word in text_lower for word in ['regulation', '监管', 'policy', '政策', 'government', '政府']):
        return '政策监管'
    elif any(word in text_lower for word in ['metaverse', '元宇宙', 'vr', 'ar', 'virtual reality']):
        return '元宇宙'
    elif any(word in text_lower for word in ['investment', '投资', 'acquisition', '收购', 'partnership', '合作']):
        return '投资并购'
    else:
        return '综合动态'

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

def fetch_tencent_news() -> List[Dict]:
    """从多个来源获取腾讯相关新闻"""
    print("开始获取腾讯相关新闻...")
    
    all_news = []
    
    # 1. 从Google News获取
    print("\n[1/2] 从 Google News 获取腾讯新闻...")
    google_news = fetch_from_google_news_tencent()
    all_news.extend(google_news)
    time.sleep(2)
    
    # 2. 从RSS订阅源获取
    print("\n[2/2] 从 RSS 订阅源获取相关新闻...")
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
    
    # 按相关性和发布时间排序
    unique_news.sort(key=lambda x: (x.get('relevance_score', 0), x['published_at']), reverse=True)
    
    print(f"\n总共获取 {len(unique_news)} 条去重后的腾讯相关新闻")
    return unique_news

def analyze_tencent_investment(news_list: List[Dict]) -> Dict:
    """分析腾讯投资建议"""
    print("\n开始腾讯投资分析...")
    
    # 情感分析关键词
    positive_keywords = [
        'surge', 'rise', 'gain', 'growth', 'increase', 'boost', 'rally',
        'positive', 'optimistic', 'strong', 'recovery', 'improve', 'beat',
        'up', 'higher', 'advance', 'jump', 'soar', 'climb', 'profit',
        'revenue', 'success', 'innovation', 'breakthrough', 'expansion'
    ]
    
    negative_keywords = [
        'fall', 'drop', 'decline', 'decrease', 'loss', 'crash', 'plunge',
        'negative', 'pessimistic', 'weak', 'recession', 'concern', 'miss',
        'down', 'lower', 'tumble', 'sink', 'slump', 'slide', 'regulation',
        'fine', 'penalty', 'ban', 'restriction', 'lawsuit', 'investigation'
    ]
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    key_factors = []
    category_sentiment = {}
    
    for news in news_list[:30]:  # 分析最新30条
        text = (news.get('title', '') + ' ' + news.get('description', '')).lower()
        category = news.get('category', '综合动态')
        
        pos_score = sum(1 for word in positive_keywords if word in text)
        neg_score = sum(1 for word in negative_keywords if word in text)
        
        # 统计分类情感
        if category not in category_sentiment:
            category_sentiment[category] = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        if pos_score > neg_score:
            positive_count += 1
            category_sentiment[category]['positive'] += 1
            if len(key_factors) < 8:
                key_factors.append({
                    'type': 'positive',
                    'category': category,
                    'title': news['title'][:80]
                })
        elif neg_score > pos_score:
            negative_count += 1
            category_sentiment[category]['negative'] += 1
            if len(key_factors) < 8:
                key_factors.append({
                    'type': 'negative',
                    'category': category,
                    'title': news['title'][:80]
                })
        else:
            neutral_count += 1
            category_sentiment[category]['neutral'] += 1
    
    # 计算投资温度分数
    total = positive_count + negative_count + neutral_count
    if total > 0:
        temperature_score = ((positive_count * 1.0 + neutral_count * 0.5) / total) * 100
    else:
        temperature_score = 50.0
    
    # 生成投资建议
    investment_advice = generate_investment_advice(
        temperature_score, 
        positive_count, 
        negative_count, 
        neutral_count,
        category_sentiment
    )
    
    # 确定情绪
    if temperature_score >= 70:
        sentiment = "乐观"
        sentiment_emoji = "😊"
    elif temperature_score >= 50:
        sentiment = "中性"
        sentiment_emoji = "😐"
    else:
        sentiment = "谨慎"
        sentiment_emoji = "😟"
    
    # 统计分类分布
    categories_distribution = {}
    for news in news_list:
        cat = news.get('category', '综合动态')
        categories_distribution[cat] = categories_distribution.get(cat, 0) + 1
    
    analysis_result = {
        'temperature_score': round(temperature_score, 1),
        'sentiment': sentiment,
        'sentiment_emoji': sentiment_emoji,
        'investment_advice': investment_advice,
        'key_factors': key_factors,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'analyzed_news_count': len(news_list),
        'analyzed_at': datetime.now().isoformat(),
        'categories_distribution': categories_distribution,
        'category_sentiment': category_sentiment
    }
    
    print(f"分析完成: 温度={temperature_score:.1f}, 情绪={sentiment}")
    return analysis_result

def generate_investment_advice(score, positive, negative, neutral, category_sentiment):
    """生成详细的投资建议"""
    
    advice = {
        'overall_rating': '',
        'risk_level': '',
        'recommendation': '',
        'detailed_analysis': '',
        'key_opportunities': [],
        'key_risks': [],
        'action_items': []
    }
    
    if score >= 75:
        advice['overall_rating'] = '强烈看好'
        advice['risk_level'] = '中等风险'
        advice['recommendation'] = '建议增持'
        advice['detailed_analysis'] = f"基于最新{positive + negative + neutral}条新闻分析，腾讯整体表现积极（积极新闻{positive}条，占比{positive/(positive+negative+neutral)*100:.1f}%）。多项业务板块展现强劲增长势头，市场情绪乐观，投资价值凸显。"
        
        advice['key_opportunities'] = [
            '游戏业务持续增长，新游戏上线表现强劲',
            '云服务市场份额扩大，企业数字化转型需求旺盛',
            '社交平台用户活跃度提升，广告收入增长潜力大',
            'AI技术应用落地，为各业务线赋能'
        ]
        
        advice['key_risks'] = [
            '监管政策变化可能影响部分业务',
            '市场竞争加剧需要持续创新投入'
        ]
        
        advice['action_items'] = [
            '建议在当前价位适度增持，目标仓位可提升至15-20%',
            '重点关注季度财报，特别是游戏和云服务收入',
            '设置止盈点，建议在上涨20%后分批获利了结',
            '长期持有，关注3-6个月的业绩表现'
        ]
        
    elif score >= 60:
        advice['overall_rating'] = '谨慎看好'
        advice['risk_level'] = '中等风险'
        advice['recommendation'] = '建议持有'
        advice['detailed_analysis'] = f"基于最新{positive + negative + neutral}条新闻分析，腾讯整体表现稳健（积极新闻{positive}条，消极新闻{negative}条）。虽然面临一些挑战，但核心业务基本面良好，具备中长期投资价值。"
        
        advice['key_opportunities'] = [
            '核心业务保持稳定增长',
            '新业务布局逐步显现成效',
            '技术创新持续推进'
        ]
        
        advice['key_risks'] = [
            '行业竞争压力增大',
            '监管环境存在不确定性',
            '部分业务增长放缓'
        ]
        
        advice['action_items'] = [
            '建议维持当前仓位，观察后续发展',
            '密切关注政策动向和竞争格局变化',
            '设置止损点，建议在下跌15%时考虑减仓',
            '等待更明确的投资信号再做调整'
        ]
        
    elif score >= 45:
        advice['overall_rating'] = '中性观望'
        advice['risk_level'] = '中高风险'
        advice['recommendation'] = '建议观望'
        advice['detailed_analysis'] = f"基于最新{positive + negative + neutral}条新闻分析，腾讯当前面临较多不确定性（积极新闻{positive}条，消极新闻{negative}条）。市场情绪偏谨慎，建议保持观望态度，等待更清晰的方向信号。"
        
        advice['key_opportunities'] = [
            '估值处于相对合理区间',
            '长期基本面仍然稳固'
        ]
        
        advice['key_risks'] = [
            '短期业绩压力较大',
            '监管政策影响持续',
            '市场竞争加剧',
            '宏观经济环境不确定'
        ]
        
        advice['action_items'] = [
            '建议暂时观望，不建议新增仓位',
            '已持有者可考虑减持至5-10%仓位',
            '设置严格止损，建议在下跌10%时止损',
            '等待明确的转机信号再考虑入场'
        ]
        
    else:
        advice['overall_rating'] = '谨慎看空'
        advice['risk_level'] = '高风险'
        advice['recommendation'] = '建议减持'
        advice['detailed_analysis'] = f"基于最新{positive + negative + neutral}条新闻分析，腾讯当前面临较大挑战（消极新闻{negative}条，占比{negative/(positive+negative+neutral)*100:.1f}%）。多项负面因素叠加，市场情绪悲观，建议谨慎对待，适度降低仓位。"
        
        advice['key_opportunities'] = [
            '估值可能已经反映部分负面因素',
            '危机中可能孕育转机'
        ]
        
        advice['key_risks'] = [
            '监管压力持续加大',
            '核心业务增长受阻',
            '市场份额流失风险',
            '投资者信心不足',
            '股价可能继续承压'
        ]
        
        advice['action_items'] = [
            '建议减持至3-5%以下仓位或清仓',
            '避免抄底，等待明确的底部信号',
            '关注政策面和基本面的重大变化',
            '可考虑转向其他更稳健的投资标的'
        ]
    
    return advice

def save_data(news_list: List[Dict], analysis: Dict):
    """保存数据到JSON文件"""
    # 确保data目录存在
    os.makedirs('data', exist_ok=True)
    
    # 保存新闻数据
    news_data = {
        'updated_at': datetime.now().isoformat(),
        'total_count': len(news_list),
        'news': news_list
    }
    
    with open('data/tencent_news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n新闻数据已保存到 data/tencent_news.json")
    
    # 保存分析结果
    with open('data/tencent_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    print(f"分析结果已保存到 data/tencent_analysis.json")

def main():
    """主函数"""
    print("=" * 60)
    print("腾讯新闻爬取与投资分析系统")
    print("=" * 60)
    
    try:
        # 获取新闻
        news_list = fetch_tencent_news()
        
        if not news_list:
            print("\n警告: 未能获取到任何新闻，使用模拟数据")
            # 使用模拟数据
            news_list = generate_mock_data()
        
        # AI分析
        analysis = analyze_tencent_investment(news_list)
        
        # 保存数据
        save_data(news_list, analysis)
        
        print("\n" + "=" * 60)
        print("任务完成!")
        print(f"- 获取新闻: {len(news_list)} 条")
        print(f"- 投资温度: {analysis['temperature_score']}")
        print(f"- 投资建议: {analysis['investment_advice']['recommendation']}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()

def generate_mock_data():
    """生成模拟数据"""
    mock_news = [
        {
            'id': 1,
            'title': 'Tencent Reports Strong Q3 Earnings, Gaming Revenue Surges 20%',
            'description': 'Tencent Holdings reported better-than-expected third-quarter earnings, with gaming revenue showing robust growth of 20% year-over-year.',
            'url': 'https://example.com/news1',
            'source': 'Reuters',
            'published_at': datetime.now().isoformat(),
            'category': '股市表现',
            'country': 'China',
            'image_url': get_placeholder_image(),
            'fetched_at': datetime.now().isoformat(),
            'relevance_score': 5
        },
        {
            'id': 2,
            'title': 'WeChat Introduces New AI-Powered Features for Business Users',
            'description': 'Tencent\'s WeChat platform launches innovative AI features aimed at enhancing business communication and customer service.',
            'url': 'https://example.com/news2',
            'source': 'TechCrunch',
            'published_at': datetime.now().isoformat(),
            'category': 'AI技术',
            'country': 'Global',
            'image_url': get_placeholder_image(),
            'fetched_at': datetime.now().isoformat(),
            'relevance_score': 4
        },
        {
            'id': 3,
            'title': 'Tencent Cloud Expands International Presence with New Data Centers',
            'description': 'Tencent Cloud announces expansion plans with new data centers in Southeast Asia and Europe to compete with AWS and Azure.',
            'url': 'https://example.com/news3',
            'source': 'Bloomberg',
            'published_at': datetime.now().isoformat(),
            'category': '云服务',
            'country': 'Global',
            'image_url': get_placeholder_image(),
            'fetched_at': datetime.now().isoformat(),
            'relevance_score': 4
        },
        {
            'id': 4,
            'title': 'Chinese Regulators Approve New Tencent Game Titles',
            'description': 'China\'s gaming regulator approves several new game titles from Tencent, signaling a more favorable regulatory environment.',
            'url': 'https://example.com/news4',
            'source': 'CNBC',
            'published_at': datetime.now().isoformat(),
            'category': '政策监管',
            'country': 'China',
            'image_url': get_placeholder_image(),
            'fetched_at': datetime.now().isoformat(),
            'relevance_score': 5
        },
        {
            'id': 5,
            'title': 'Tencent Music Entertainment Sees User Growth Amid Competition',
            'description': 'Despite fierce competition, Tencent Music reports steady user growth and improved monetization strategies.',
            'url': 'https://example.com/news5',
            'source': 'Financial Times',
            'published_at': datetime.now().isoformat(),
            'category': '数字内容',
            'country': 'China',
            'image_url': get_placeholder_image(),
            'fetched_at': datetime.now().isoformat(),
            'relevance_score': 3
        },
        {
            'id': 6,
            'title': 'Tencent Invests in Metaverse Startups, Eyes Future Growth',
            'description': 'Tencent announces strategic investments in several metaverse and VR technology startups as part of its long-term growth strategy.',
            'url': 'https://example.com/news6',
            'source': 'TechNode',
            'published_at': datetime.now().isoformat(),
            'category': '元宇宙',
            'country': 'Global',
            'image_url': get_placeholder_image(),
            'fetched_at': datetime.now().isoformat(),
            'relevance_score': 4
        }
    ]
    return mock_news

if __name__ == '__main__':
    main()

