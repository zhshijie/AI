# 新闻源配置指南

本文档介绍如何添加和配置新的新闻源。

## 📰 当前使用的新闻源

### 1. Google News RSS
- **URL**: `https://news.google.com/rss/search?q=economy+OR+stock+market+OR+GDP+OR+inflation`
- **类型**: RSS 2.0
- **优点**: 聚合多个新闻源，内容丰富
- **限制**: 无
- **更新频率**: 实时

### 2. Yahoo Finance RSS
- **URL**: `https://finance.yahoo.com/news/rssindex`
- **类型**: RSS 2.0
- **优点**: 金融新闻专业，数据准确
- **限制**: 无
- **更新频率**: 实时

### 3. BBC Business RSS
- **URL**: `https://feeds.bbci.co.uk/news/business/rss.xml`
- **类型**: RSS 2.0
- **优点**: 权威媒体，国际视角
- **限制**: 无
- **更新频率**: 每小时

### 4. CNBC RSS
- **URL**: `https://www.cnbc.com/id/100003114/device/rss/rss.html`
- **类型**: RSS 2.0
- **优点**: 美国财经新闻，市场分析深入
- **限制**: 无
- **更新频率**: 实时

### 5. Financial Times RSS
- **URL**: `https://www.ft.com/?format=rss`
- **类型**: RSS 2.0
- **优点**: 高质量金融分析
- **限制**: 部分内容需要订阅
- **更新频率**: 每小时

### 6. Bloomberg RSS
- **URL**: `https://www.bloomberg.com/feed/podcast/etf-report.xml`
- **类型**: RSS 2.0
- **优点**: 专业金融数据
- **限制**: 无
- **更新频率**: 每小时

## 🔧 如何添加新的RSS新闻源

### 步骤1：找到RSS订阅地址

大多数新闻网站都提供RSS订阅，通常可以在页面底部找到RSS图标或链接。

**常见RSS订阅地址格式：**
- `https://example.com/rss`
- `https://example.com/feed`
- `https://example.com/rss.xml`
- `https://example.com/feed.xml`

### 步骤2：修改爬虫脚本

编辑 `scripts/fetch_news.py` 文件，在 `RSS_FEEDS` 列表中添加新的订阅源：

```python
RSS_FEEDS = [
    # ... 现有的订阅源 ...
    {
        'url': 'https://your-news-site.com/rss.xml',
        'source': '新闻源名称',
        'country': '国家/地区'
    }
]
```

### 步骤3：测试

在本地运行脚本测试：

```bash
python scripts/fetch_news.py
```

## 🌐 推荐的免费新闻源

### 经济类
- **Reuters Business**: `https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best`
- **MarketWatch**: `https://www.marketwatch.com/rss/`
- **The Economist**: `https://www.economist.com/rss`

### 科技类
- **TechCrunch**: `https://techcrunch.com/feed/`
- **The Verge**: `https://www.theverge.com/rss/index.xml`
- **Wired**: `https://www.wired.com/feed/rss`

### 加密货币
- **CoinDesk**: `https://www.coindesk.com/arc/outboundfeeds/rss/`
- **Cointelegraph**: `https://cointelegraph.com/rss`
- **Bitcoin Magazine**: `https://bitcoinmagazine.com/.rss/full/`

### 中文新闻源
- **新浪财经**: `https://finance.sina.com.cn/roll/index.d.html?format=rss`
- **财新网**: `http://www.caixin.com/rss/rss_index.xml`
- **华尔街见闻**: `https://wallstreetcn.com/rss`

## 🛠️ 使用其他免费API

### 1. NewsData.io
- **网站**: https://newsdata.io/
- **免费额度**: 每天200次请求
- **注册**: 需要邮箱注册

```python
import requests

API_KEY = 'your_api_key'
url = f'https://newsdata.io/api/1/news?apikey={API_KEY}&q=economy&language=en'
response = requests.get(url)
data = response.json()
```

### 2. Currents API
- **网站**: https://currentsapi.services/
- **免费额度**: 每天600次请求
- **注册**: 需要邮箱注册

```python
import requests

API_KEY = 'your_api_key'
url = f'https://api.currentsapi.services/v1/latest-news?apiKey={API_KEY}&category=business'
response = requests.get(url)
data = response.json()
```

### 3. GNews API
- **网站**: https://gnews.io/
- **免费额度**: 每天100次请求
- **注册**: 需要邮箱注册

```python
import requests

API_KEY = 'your_api_key'
url = f'https://gnews.io/api/v4/search?q=economy&token={API_KEY}&lang=en'
response = requests.get(url)
data = response.json()
```

## 🔍 网页爬取方案

如果RSS不可用，可以直接爬取网页内容：

```python
import requests
from bs4 import BeautifulSoup

def scrape_news_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 根据网站结构提取新闻
    articles = soup.find_all('article')
    
    news_list = []
    for article in articles:
        title = article.find('h2').text
        link = article.find('a')['href']
        description = article.find('p').text
        
        news_list.append({
            'title': title,
            'url': link,
            'description': description
        })
    
    return news_list
```

## ⚠️ 注意事项

1. **遵守robots.txt**: 检查网站的 `robots.txt` 文件，确保允许爬取
2. **请求频率**: 不要频繁请求，建议每次请求间隔1-2秒
3. **User-Agent**: 设置合理的User-Agent，避免被识别为机器人
4. **版权问题**: 仅用于个人学习和研究，不要商业使用
5. **反爬虫机制**: 某些网站可能有反爬虫机制，需要使用代理或其他方法

## 🔄 更新频率建议

- **实时新闻**: 每1-2小时更新一次
- **深度分析**: 每6-12小时更新一次
- **周报月报**: 每天更新一次

## 📊 数据质量优化

### 去重
```python
seen_urls = set()
unique_news = []
for news in all_news:
    if news['url'] not in seen_urls:
        seen_urls.add(news['url'])
        unique_news.append(news)
```

### 过滤
```python
# 过滤掉标题太短的新闻
filtered_news = [n for n in news_list if len(n['title']) > 20]

# 过滤掉特定关键词
excluded_keywords = ['advertisement', 'sponsored']
filtered_news = [n for n in news_list 
                 if not any(kw in n['title'].lower() for kw in excluded_keywords)]
```

### 排序
```python
# 按发布时间排序
sorted_news = sorted(news_list, key=lambda x: x['published_at'], reverse=True)

# 按相关性排序
def calculate_relevance(news):
    keywords = ['economy', 'market', 'stock', 'GDP']
    score = sum(1 for kw in keywords if kw in news['title'].lower())
    return score

sorted_news = sorted(news_list, key=calculate_relevance, reverse=True)
```

## 🤝 贡献

如果你发现了好用的新闻源，欢迎提交PR或Issue分享！

---

**最后更新**: 2025-10-23
