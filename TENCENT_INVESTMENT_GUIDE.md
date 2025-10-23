# 腾讯投资分析系统使用指南

## 🎯 系统简介

腾讯投资分析系统是一个基于AI的智能投资决策辅助工具，专门针对腾讯控股（00700.HK / TCEHY）及其相关行业进行新闻收集、数据分析和投资建议生成。

## ✨ 核心功能

### 1. 智能新闻聚合
- 🔍 **多源爬取**：从Google News、BBC、CNBC、Reuters等权威媒体获取腾讯相关新闻
- 🎯 **精准筛选**：基于关键词和相关性算法，只保留高质量的腾讯相关新闻
- 📊 **自动分类**：将新闻自动分类为游戏业务、社交平台、云服务、金融科技等10大类别

### 2. AI投资分析
- 🤖 **情感分析**：基于NLP技术分析新闻情感倾向（积极/消极/中性）
- 🌡️ **投资温度**：计算0-100的投资温度指数，直观反映投资价值
- 📈 **趋势预测**：结合历史数据和当前新闻，预测短期投资趋势

### 3. 智能投资建议
- 💡 **综合评级**：强烈看好/谨慎看好/中性观望/谨慎看空四级评级
- ⚠️ **风险评估**：低风险/中等风险/中高风险/高风险四级风险评估
- 📋 **具体建议**：提供明确的买入/持有/观望/减持建议
- 🎯 **行动指南**：给出具体的仓位配置、止盈止损点位等操作建议

### 4. 可视化展示
- 📊 **温度计图表**：直观展示投资温度
- 🥧 **分类饼图**：展示各业务板块新闻分布
- 📰 **新闻卡片**：美观的新闻展示界面
- 🎨 **响应式设计**：完美支持PC和移动端

## 🚀 快速开始

### 方式一：查看演示数据（最快）

1. 直接访问页面：`https://your-username.github.io/your-repo/tencent.html`
2. 系统会自动加载演示数据
3. 可以立即查看完整的分析报告和投资建议

### 方式二：获取真实数据（推荐）

#### 步骤1：手动运行爬虫

```bash
# 克隆仓库
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 安装依赖
pip install -r requirements.txt

# 运行腾讯新闻爬虫
python scripts/fetch_tencent_news.py

# 查看生成的数据
cat data/tencent_news.json
cat data/tencent_analysis.json
```

#### 步骤2：提交数据到GitHub

```bash
git add data/tencent_news.json data/tencent_analysis.json
git commit -m "Add Tencent news data"
git push
```

#### 步骤3：访问页面

等待1-2分钟后，访问 `https://your-username.github.io/your-repo/tencent.html`

### 方式三：自动化更新（最佳）

#### 启用GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 找到 `Fetch Tencent News and Analyze` 工作流
3. 点击 `Enable workflow`
4. 点击 `Run workflow` 手动触发一次

#### 配置自动运行

工作流会每6小时自动运行一次，无需人工干预。

## 📊 数据说明

### 新闻数据结构 (tencent_news.json)

```json
{
  "updated_at": "2025-10-23T17:00:00Z",
  "total_count": 20,
  "news": [
    {
      "id": 1,
      "title": "新闻标题",
      "description": "新闻描述",
      "url": "新闻链接",
      "source": "新闻来源",
      "published_at": "发布时间",
      "category": "新闻分类",
      "country": "国家/地区",
      "image_url": "图片链接",
      "fetched_at": "爬取时间",
      "relevance_score": 5
    }
  ]
}
```

### 分析结果结构 (tencent_analysis.json)

```json
{
  "temperature_score": 72.5,
  "sentiment": "乐观",
  "sentiment_emoji": "😊",
  "investment_advice": {
    "overall_rating": "强烈看好",
    "risk_level": "中等风险",
    "recommendation": "建议增持",
    "detailed_analysis": "详细分析文本...",
    "key_opportunities": ["机会1", "机会2"],
    "key_risks": ["风险1", "风险2"],
    "action_items": ["行动1", "行动2"]
  },
  "key_factors": [
    {
      "type": "positive",
      "category": "游戏业务",
      "title": "关键因素标题"
    }
  ],
  "positive_count": 15,
  "negative_count": 3,
  "neutral_count": 2,
  "analyzed_news_count": 20,
  "analyzed_at": "2025-10-23T17:00:00Z",
  "categories_distribution": {
    "游戏业务": 5,
    "云服务": 3
  }
}
```

## 🎨 页面功能详解

### 1. 顶部统计卡片
- **相关新闻**：显示爬取到的腾讯相关新闻总数
- **投资温度**：0-100的温度指数，越高越看好
- **市场情绪**：乐观/中性/谨慎三种情绪
- **投资评级**：强烈看好/谨慎看好/中性观望/谨慎看空

### 2. AI投资建议卡片
- **综合评估**：投资建议、风险等级、积极/消极因素统计
- **详细分析**：AI生成的详细投资分析文本
- **投资建议**：明确的买入/持有/观望/减持建议

### 3. 投资温度可视化
- **温度计图表**：仪表盘样式，直观展示投资温度
- **分类饼图**：展示各业务板块的新闻分布情况

### 4. 关键机会与风险
- **投资机会**：列出当前的主要投资机会点
- **投资风险**：列出需要注意的主要风险点

### 5. 具体行动建议
- **仓位配置**：建议的持仓比例
- **止盈止损**：具体的止盈止损点位
- **关注重点**：需要重点关注的指标和事件
- **操作时机**：建议的买入/卖出时机

### 6. 关键影响因素
- 列出影响投资决策的关键新闻
- 区分积极因素（绿色）和消极因素（红色）
- 显示新闻分类和标题

### 7. 新闻列表
- 展示所有腾讯相关新闻
- 点击卡片可跳转到原文
- 显示新闻分类、来源、发布时间

## 🔧 自定义配置

### 修改新闻源

编辑 `scripts/fetch_tencent_news.py` 文件：

```python
# 添加新的RSS订阅源
RSS_FEEDS = [
    {
        'url': 'https://your-rss-feed.com/rss.xml',
        'source': '新闻源名称',
        'country': '国家/地区'
    }
]
```

### 修改关键词

```python
# 添加腾讯相关关键词
TENCENT_KEYWORDS = [
    'Tencent', '腾讯', 'WeChat', '微信',
    # 添加更多关键词...
]

# 添加行业关键词
INDUSTRY_KEYWORDS = [
    'gaming', 'cloud computing', 'AI',
    # 添加更多关键词...
]
```

### 修改更新频率

编辑 `.github/workflows/fetch-tencent-news.yml` 文件：

```yaml
schedule:
  - cron: '0 */6 * * *'  # 每6小时
  # 改为每12小时：'0 */12 * * *'
  # 改为每天一次：'0 0 * * *'
```

## 📈 投资建议解读

### 温度指数含义

| 温度范围 | 投资建议 | 风险等级 | 操作建议 |
|---------|---------|---------|---------|
| 75-100 | 强烈看好 | 中等风险 | 建议增持 |
| 60-74 | 谨慎看好 | 中等风险 | 建议持有 |
| 45-59 | 中性观望 | 中高风险 | 建议观望 |
| 0-44 | 谨慎看空 | 高风险 | 建议减持 |

### 情绪指标

- **乐观 😊**：积极新闻占比 > 60%，市场情绪良好
- **中性 😐**：积极新闻占比 40-60%，市场情绪平稳
- **谨慎 😟**：积极新闻占比 < 40%，市场情绪悲观

### 风险等级

- **低风险**：基本面稳固，短期波动小
- **中等风险**：基本面良好，存在一定不确定性
- **中高风险**：面临较多挑战，波动较大
- **高风险**：负面因素较多，不确定性高

## ⚠️ 重要声明

1. **仅供参考**：本系统提供的分析和建议仅供参考，不构成投资建议
2. **投资有风险**：股市有风险，投资需谨慎，请根据自身情况做出决策
3. **数据延迟**：新闻数据可能存在延迟，请结合实时行情判断
4. **算法局限**：AI分析基于历史数据和新闻文本，可能存在偏差
5. **自负盈亏**：投资决策由您自己做出，盈亏自负

## 🔍 故障排查

### 问题1：页面显示"使用演示数据"

**原因**：数据文件不存在或加载失败

**解决方案**：
1. 运行爬虫脚本生成数据：`python scripts/fetch_tencent_news.py`
2. 或手动触发GitHub Actions工作流
3. 确认 `data/tencent_news.json` 和 `data/tencent_analysis.json` 存在

### 问题2：新闻数量很少

**原因**：
- 相关性筛选过于严格
- 新闻源暂时没有腾讯相关新闻

**解决方案**：
1. 降低相关性阈值（修改 `calculate_relevance` 函数）
2. 添加更多新闻源
3. 扩展关键词列表

### 问题3：GitHub Actions运行失败

**原因**：权限不足或网络问题

**解决方案**：
1. 检查仓库权限设置：`Settings` → `Actions` → `General`
2. 选择 `Read and write permissions`
3. 查看Actions日志，定位具体错误

## 📚 相关资源

### 腾讯官方
- [腾讯控股官网](https://www.tencent.com/)
- [腾讯投资者关系](https://www.tencent.com/zh-cn/investors.html)
- [腾讯财报](https://www.tencent.com/zh-cn/investors/financial-reports.html)

### 新闻源
- [Google News - Tencent](https://news.google.com/search?q=Tencent)
- [Reuters - Tencent](https://www.reuters.com/companies/0700.HK)
- [Bloomberg - Tencent](https://www.bloomberg.com/quote/700:HK)

### 技术文档
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [BeautifulSoup文档](https://www.crummy.com/software/BeautifulSoup/)
- [ECharts文档](https://echarts.apache.org/)

## 🤝 贡献

欢迎提交Issue和Pull Request！

如果你有好的建议或发现了bug，请：
1. 提交Issue描述问题
2. Fork仓库并修改
3. 提交Pull Request

## 📄 许可证

MIT License

---

**最后更新**: 2025-10-23

**Made with ❤️ by AI + GitHub Actions**

