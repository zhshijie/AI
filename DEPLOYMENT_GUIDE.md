# 部署配置指南

## 🚀 快速开始

本系统已经优化了数据加载逻辑，支持多种部署方式，无需复杂配置即可运行。

## 📋 部署方式

### 方式一：GitHub Pages（推荐）

**优点**：完全免费，自动部署，无需配置API

**步骤**：

1. **启用GitHub Pages**
   - 进入仓库 `Settings` → `Pages`
   - Source 选择 `Deploy from a branch`
   - Branch 选择 `main`，目录选择 `/docs`
   - 点击 `Save`

2. **等待部署完成**
   - 通常需要2-3分钟
   - 访问 `https://your-username.github.io/your-repo-name`

3. **无需修改代码**
   - 系统会自动检测GitHub Pages环境
   - 自动从 `../data/` 目录读取数据
   - 如果数据文件不存在，会显示演示数据

### 方式二：本地开发

**步骤**：

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **生成数据**
   ```bash
   pip install -r requirements.txt
   python scripts/fetch_news.py
   ```

3. **启动本地服务器**
   ```bash
   cd docs
   python -m http.server 8000
   ```

4. **访问页面**
   - 打开浏览器访问 `http://localhost:8000`
   - 系统会自动从 `../data/` 读取数据

### 方式三：Vercel + GitHub Pages（完整方案）

**优点**：支持API接口，可以实现更复杂的功能

**步骤**：

1. **部署到Vercel**
   - 访问 [Vercel](https://vercel.com)
   - 导入你的GitHub仓库
   - 点击 `Deploy`
   - 复制你的Vercel域名（如：`https://your-app.vercel.app`）

2. **配置API地址**
   - 编辑 `docs/main.js` 文件
   - 修改第2行：
     ```javascript
     const API_BASE = 'https://your-app.vercel.app/api';
     ```
   - 替换为你的实际Vercel域名

3. **提交更改**
   ```bash
   git add docs/main.js
   git commit -m "Update API base URL"
   git push
   ```

4. **访问页面**
   - GitHub Pages会自动更新
   - 系统会优先使用Vercel API

## 🔧 配置说明

### 数据源优先级

系统会按以下顺序尝试加载数据：

1. **GitHub Pages环境**：自动从 `../data/` 读取JSON文件
2. **本地开发环境**：自动从 `../data/` 读取JSON文件
3. **Vercel API**：如果配置了正确的API地址
4. **演示数据**：如果以上都失败，使用内置演示数据

### 环境检测逻辑

```javascript
const USE_LOCAL_DATA = window.location.hostname === 'localhost' || 
                       window.location.hostname === '127.0.0.1' ||
                       window.location.hostname.includes('github.io');
```

- `localhost` 或 `127.0.0.1`：本地开发环境
- 包含 `github.io`：GitHub Pages环境
- 其他：生产环境（使用Vercel API）

## 📊 数据文件说明

### 必需的数据文件

- `data/news.json`：新闻数据
- `data/analysis.json`：分析结果

### 数据生成方式

1. **GitHub Actions自动生成**（推荐）
   - 每6小时自动运行
   - 自动提交到仓库
   - 无需手动操作

2. **手动生成**
   ```bash
   python scripts/fetch_news.py
   ```

3. **手动触发GitHub Actions**
   - 进入仓库 `Actions` 标签
   - 选择 `Fetch News and Analyze`
   - 点击 `Run workflow`

## ⚠️ 常见问题

### 问题1：页面显示"加载统计数据失败"

**原因**：
- 数据文件不存在
- API地址配置错误
- 网络连接问题

**解决方案**：
1. 检查 `data/` 目录是否有 `news.json` 和 `analysis.json`
2. 如果没有，运行 `python scripts/fetch_news.py` 生成
3. 或者手动触发GitHub Actions
4. 系统会自动使用演示数据，不影响基本功能

### 问题2：GitHub Pages显示404

**原因**：
- GitHub Pages未启用
- 分支或目录配置错误

**解决方案**：
1. 确认 `Settings` → `Pages` 中的配置
2. Branch: `main`，目录: `/docs`
3. 等待2-3分钟后重试

### 问题3：数据不更新

**原因**：
- GitHub Actions未运行
- 权限配置错误

**解决方案**：
1. 检查 `Actions` 标签页的运行记录
2. 确认权限设置：`Settings` → `Actions` → `General`
3. 选择 `Read and write permissions`
4. 手动触发一次工作流测试

### 问题4：Vercel API无法访问

**原因**：
- API地址配置错误
- CORS问题
- Vercel部署失败

**解决方案**：
1. 检查 `docs/main.js` 中的 `API_BASE` 配置
2. 访问 Vercel Dashboard 查看部署状态
3. 检查 `vercel.json` 配置是否正确
4. 系统会自动降级到本地数据，不影响使用

## 🎯 推荐配置

### 个人使用（最简单）

```
GitHub Pages + GitHub Actions
```

- ✅ 完全免费
- ✅ 自动更新
- ✅ 无需配置
- ✅ 稳定可靠

### 团队使用（功能完整）

```
GitHub Pages + Vercel API + GitHub Actions
```

- ✅ 支持API接口
- ✅ 可扩展性强
- ✅ 性能更好
- ⚠️ 需要配置API地址

## 📝 检查清单

部署前请确认：

- [ ] GitHub Actions已启用
- [ ] 工作流权限设置为 `Read and write permissions`
- [ ] GitHub Pages已启用（Branch: main, 目录: /docs）
- [ ] 数据文件已生成（data/news.json, data/analysis.json）
- [ ] （可选）Vercel已部署
- [ ] （可选）API地址已配置

## 🔗 相关链接

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitHub Pages文档](https://docs.github.com/en/pages)
- [Vercel文档](https://vercel.com/docs)
- [故障排查指南](./TROUBLESHOOTING.md)

---

**最后更新**: 2025-10-23

