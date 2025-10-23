# 全球经济新闻与投资温度评估系统

基于 **GitHub Actions** + **Vercel** + **GitHub Pages** 的全自动化经济新闻爬取与AI分析系统。

## 🌟 系统特点

- ✅ **完全免费**：使用GitHub Actions、Vercel、GitHub Pages等免费服务
- ✅ **无需API密钥**：使用RSS订阅源和网页爬取，无需注册任何API
- ✅ **自动化运行**：定时爬取新闻，自动AI分析，无需人工干预
- ✅ **实时更新**：每6小时自动更新一次数据
- ✅ **多源聚合**：整合Google News、Yahoo Finance、BBC、CNBC等多个新闻源
- 🤖 **真正的AI分析**：集成Groq、OpenRouter、DeepSeek等AI服务，智能分析新闻并生成专业投资建议
- ✅ **智能降级**：AI不可用时自动切换到规则分析，确保系统稳定运行
- ✅ **美观界面**：现代化响应式设计，支持移动端
- ✨ **腾讯专版**：专门针对腾讯控股的投资分析系统，提供详细的投资建议

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
│       ├── fetch-news.yml          # 全球经济新闻工作流
│       └── fetch-tencent-news.yml  # 腾讯新闻工作流
├── api/
│   └── index.py                    # Vercel Serverless函数
├── data/
│   ├── news.json                   # 全球经济新闻数据
│   ├── analysis.json               # 全球经济分析结果
│   ├── tencent_news.json           # 腾讯新闻数据
│   └── tencent_analysis.json       # 腾讯投资分析结果
├── docs/                           # GitHub Pages前端页面
│   ├── index.html                  # 全球经济新闻主页
│   ├── main.js                     # 主页脚本
│   ├── tencent.html                # 腾讯投资分析页面
│   ├── tencent.js                  # 腾讯页面脚本
│   └── health.html                 # 健康检查页面
├── scripts/
│   ├── fetch_news.py               # 全球经济新闻爬虫
│   └── fetch_tencent_news.py       # 腾讯新闻爬虫
├── vercel.json                     # Vercel配置文件
├── README.md                       # 项目说明文档
└── TENCENT_INVESTMENT_GUIDE.md     # 腾讯投资分析使用指南
```

## 🎯 双系统架构

本项目包含两个独立的分析系统：

### 1. 全球经济新闻分析系统
- 📊 **功能**：分析全球经济新闻，评估整体投资温度
- 🌐 **访问**：`https://your-username.github.io/your-repo/index.html`
- 📝 **说明**：适合宏观经济分析和全球市场趋势判断

### 2. 腾讯投资分析系统 ⭐ NEW
- 🎯 **功能**：专注腾讯控股及相关行业，提供详细投资建议
- 🔗 **访问**：`https://your-username.github.io/your-repo/tencent.html`
- 📖 **文档**：查看 [腾讯投资分析使用指南](./TENCENT_INVESTMENT_GUIDE.md)
- 💡 **特色**：
  - AI生成的详细投资建议（买入/持有/观望/减持）
  - 风险等级评估和具体行动指南
  - 关键投资机会和风险分析
  - 业务板块分类统计和趋势分析

## 🚀 部署指南

### 快速开始（3步完成）

1. **Fork本仓库** → 2. **启用GitHub Actions** → 3. **启用GitHub Pages**

就这么简单！系统会自动运行，无需任何配置。

详细步骤：

### 1. Fork 本仓库

点击右上角的 `Fork` 按钮，将本仓库复制到你的GitHub账号下。

### 2. 配置 GitHub Actions

#### 基础配置（无需API密钥）

系统使用免费的RSS订阅源和网页爬取，**无需任何配置即可运行**。

当前使用的免费新闻源：
- ✅ Google News RSS（经济类新闻）
- ✅ Yahoo Finance RSS（金融新闻）
- ✅ BBC Business RSS（商业新闻）
- ✅ CNBC RSS（财经新闻）
- ✅ Financial Times RSS（金融时报）
- ✅ Bloomberg RSS（彭博社）

#### AI分析配置（推荐，提升分析质量）🤖

**强烈推荐**配置AI分析功能，使用真正的大语言模型进行智能分析，替代简单的关键词规则。

**方式一：使用Groq（推荐，完全免费）**

1. 访问 [Groq Console](https://console.groq.com/) 注册账号（完全免费）
2. 获取API密钥：[API Keys页面](https://console.groq.com/keys)
3. 在GitHub仓库添加Secret：
   - Name: `GROQ_API_KEY`
   - Value: 你的API密钥

**方式二：使用OpenRouter（免费模型）**

1. 访问 [OpenRouter](https://openrouter.ai/) 注册账号
2. 获取API密钥
3. 在GitHub仓库添加Secrets：
   - Name: `OPENROUTER_API_KEY`，Value: 你的API密钥
   - Name: `AI_PROVIDER`，Value: `openrouter`

**方式三：使用DeepSeek（低成本，约0.001元/次）**

1. 访问 [DeepSeek](https://platform.deepseek.com/) 注册账号
2. 获取API密钥
3. 在GitHub仓库添加Secrets：
   - Name: `DEEPSEEK_API_KEY`，Value: 你的API密钥
   - Name: `AI_PROVIDER`，Value: `deepseek`

📖 **详细配置指南**：
- 🚀 [5分钟快速开始](./QUICK_START_AI.md) - 最简单的配置方式
- 📚 [完整使用指南](./AI_ANALYSIS_GUIDE.md) - 深入了解AI分析功能

**AI分析 vs 规则分析对比**：

| 特性 | 规则分析（默认） | AI分析（推荐） |
|------|----------------|---------------|
| 准确性 | 60-70% | 85-95% |
| 分析深度 | 关键词匹配 | 理解语义和上下文 |
| 投资建议 | 模板化 | 个性化、专业化 |
| 成本 | 免费 | 免费（Groq/OpenRouter）或极低成本（DeepSeek） |

**注意**：即使不配置AI，系统也会使用规则分析正常运行，只是分析质量会有所降低。

### 3. 启用 GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 点击 `I understand my workflows, go ahead and enable them`
3. 选择 `Fetch News and Analyze` 工作流
4. 点击 `Enable workflow`

**重要**：确保仓库的 Actions 权限设置正确：
- 进入仓库的 `Settings` → `Actions` → `General`
- 在 "Workflow permissions" 部分，选择 `Read and write permissions`
- 勾选 `Allow GitHub Actions to create and approve pull requests`
- 点击 `Save`

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

### 6. 更新前端API地址（可选）

**注意**：如果你只使用GitHub Pages，无需修改任何代码！系统会自动从数据文件读取。

如果你部署了Vercel API，可以编辑 `docs/main.js` 文件，将第2行的API地址替换为你的Vercel域名：

```javascript
const API_BASE = 'https://your-vercel-app.vercel.app/api';
```

提交更改后，GitHub Pages会自动更新。

**数据加载优先级**：
1. GitHub Pages环境：自动从 `data/` 目录读取JSON文件
2. 本地开发：自动从 `data/` 目录读取JSON文件
3. 配置了Vercel API：使用API接口
4. 以上都失败：使用内置演示数据

详细配置说明请查看 [部署配置指南](./DEPLOYMENT_GUIDE.md)

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

## 🔧 故障排查

遇到问题？查看 [故障排查指南](./TROUBLESHOOTING.md) 获取详细的解决方案。

常见问题：
- ❌ GitHub Actions 权限错误 (403)
- ❌ Vercel 部署失败
- ❌ 页面无法显示数据
- ❌ 新闻爬取失败

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
