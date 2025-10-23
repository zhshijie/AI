# 全球经济新闻与投资温度评估系统

基于 **GitHub Actions** + **Vercel** + **GitHub Pages** 的全自动化经济新闻爬取与AI分析系统。

## 🌟 系统特点

- ✅ **完全免费**：使用GitHub Actions、Vercel、GitHub Pages等免费服务
- ✅ **无需API密钥**：使用RSS订阅源和网页爬取，无需注册任何API
- ✅ **自动化运行**：定时爬取新闻，自动AI分析，无需人工干预
- ✅ **实时更新**：每6小时自动更新一次数据
- ✅ **多源聚合**：整合Google News、Yahoo Finance、BBC、CNBC等多个新闻源
- ✅ **智能分析**：基于关键词的情感分析，评估投资温度
- ✅ **美观界面**：现代化响应式设计，支持移动端

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Actions                        │
│  (定时执行爬虫 + AI分析，每6小时运行一次)                  │
│  - 爬取全球经济新闻                                       │
│  - AI情感分析与投资温度评估                               │
│  - 自动提交数据到GitHub仓库                               │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                    GitHub Repository                     │
│  - 存储新闻数据 (data/news.json)                         │
│  - 存储分析结果 (data/analysis.json)                     │
│  - 前端页面代码 (docs/)                                  │
└─────────────┬───────────────────┬───────────────────────┘
              │                   │
              ▼                   ▼
┌─────────────────────┐  ┌──────────────────────┐
│   GitHub Pages      │  │      Vercel          │
│  (前端页面展示)      │  │  (API服务托管)        │
│  - 展示新闻列表      │  │  - 提供REST API      │
│  - 投资温度可视化    │  │  - 读取JSON数据      │
│  - 数据统计分析      │  │  - 跨域支持          │
└─────────────────────┘  └──────────────────────┘
```

## 📦 项目结构

```
.
├── .github/
│   └── workflows/
│       └── fetch-news.yml          # GitHub Actions工作流配置
├── api/
│   └── index.py                    # Vercel Serverless函数
├── data/
│   ├── news.json                   # 新闻数据
│   └── analysis.json               # 分析结果
├── docs/                           # GitHub Pages前端页面
│   ├── index.html
│   └── main.js
├── scripts/
│   └── fetch_news.py               # 新闻爬取与分析脚本
├── vercel.json                     # Vercel配置文件
└── README.md                       # 项目说明文档
```

## 🚀 部署指南

### 1. Fork 本仓库

点击右上角的 `Fork` 按钮，将本仓库复制到你的GitHub账号下。

### 2. 配置 GitHub Actions

**无需配置任何API密钥！** 系统使用免费的RSS订阅源和网页爬取。

如果你想使用额外的新闻源，可以在仓库中设置以下 Secrets（Settings → Secrets and variables → Actions）：

- `NEWS_API_KEY`（可选）：NewsAPI.org的API密钥
  - 注册地址：https://newsapi.org/register
  - 免费版每天100次请求

当前系统使用的免费新闻源：
- ✅ Google News RSS（经济类新闻）
- ✅ Yahoo Finance RSS（金融新闻）
- ✅ BBC Business RSS（商业新闻）
- ✅ CNBC RSS（财经新闻）
- ✅ Financial Times RSS（金融时报）
- ✅ Bloomberg RSS（彭博社）

### 3. 启用 GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 点击 `I understand my workflows, go ahead and enable them`
3. 选择 `Fetch News and Analyze` 工作流
4. 点击 `Enable workflow`

### 4. 部署到 Vercel

1. 访问 [Vercel](https://vercel.com)，使用GitHub账号登录
2. 点击 `New Project`
3. 导入你Fork的仓库
4. Vercel会自动检测配置，直接点击 `Deploy`
5. 部署完成后，复制你的Vercel域名（如：`https://your-app.vercel.app`）

### 5. 配置 GitHub Pages

1. 进入仓库的 `Settings` → `Pages`
2. Source 选择 `Deploy from a branch`
3. Branch 选择 `main`，文件夹选择 `/docs`
4. 点击 `Save`
5. 等待几分钟，访问 `https://your-username.github.io/your-repo-name`

### 6. 更新前端API地址

编辑 `docs/main.js` 文件，将第2行的API地址替换为你的Vercel域名：

```javascript
const API_BASE = 'https://your-vercel-app.vercel.app/api';
```

提交更改后，GitHub Pages会自动更新。

## 🔧 配置说明

### 修改更新频率

编辑 `.github/workflows/fetch-news.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '0 */6 * * *'  # 每6小时执行一次
```

常用的cron表达式：
- `0 */6 * * *` - 每6小时
- `0 */12 * * *` - 每12小时
- `0 0 * * *` - 每天0点
- `0 0,12 * * *` - 每天0点和12点

### 手动触发更新

1. 进入仓库的 `Actions` 标签页
2. 选择 `Fetch News and Analyze` 工作流
3. 点击 `Run workflow` → `Run workflow`

## 📊 数据说明

### news.json 结构

```json
{
  "updated_at": "2025-10-23T17:00:00Z",
  "total_count": 6,
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
      "fetched_at": "爬取时间"
    }
  ]
}
```

### analysis.json 结构

```json
{
  "temperature_score": 62.5,
  "sentiment": "中性",
  "sentiment_emoji": "😐",
  "analysis_text": "分析结论",
  "key_factors": ["关键因素1", "关键因素2"],
  "positive_count": 3,
  "negative_count": 2,
  "neutral_count": 1,
  "analyzed_news_count": 6,
  "analyzed_at": "2025-10-23T17:00:00Z",
  "categories_distribution": {
    "货币政策": 2,
    "经济数据": 2
  }
}
```

## 🔌 API 接口

### 获取最新新闻

```
GET /api/news/latest?limit=20&category=货币政策
```

### 获取新闻分类

```
GET /api/news/categories
```

### 获取最新投资温度

```
GET /api/temperature/latest
```

### 获取统计概览

```
GET /api/stats/overview
```

## 🎨 自定义样式

前端页面使用 Tailwind CSS，你可以直接修改 `docs/index.html` 中的样式类来自定义外观。

## 📝 注意事项

1. **RSS订阅源**：完全免费，无请求次数限制，但部分网站可能有反爬虫机制
2. **GitHub Actions限制**：每月2000分钟免费额度，本项目每次运行约2-3分钟
3. **Vercel限制**：免费版每月100GB流量，足够个人使用
4. **数据存储**：所有数据存储在GitHub仓库中，注意仓库大小限制（建议定期清理旧数据）
5. **网络访问**：如果GitHub Actions无法访问某些新闻网站，可以考虑使用代理或更换新闻源

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

### 新闻源
- [Google News](https://news.google.com/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [BBC Business](https://www.bbc.com/news/business)
- [CNBC](https://www.cnbc.com/)
- [Financial Times](https://www.ft.com/)
- [Bloomberg](https://www.bloomberg.com/)

### 技术文档
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [Vercel文档](https://vercel.com/docs)
- [GitHub Pages文档](https://docs.github.com/en/pages)
- [RSS 2.0规范](https://www.rssboard.org/rss-specification)
- [BeautifulSoup文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Made with ❤️ by GitHub Actions + Vercel + GitHub Pages**
