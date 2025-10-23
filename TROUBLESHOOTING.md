# 故障排查指南

本文档列出了常见问题及其解决方案。

## 🔴 GitHub Actions 错误

### 错误 1: Permission denied (403)

**错误信息**：
```
remote: Permission to username/repo.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/username/repo/': The requested URL returned error: 403
```

**原因**：GitHub Actions 没有写入权限。

**解决方案**：

1. **方法一：修改仓库设置（推荐）**
   - 进入仓库的 `Settings` → `Actions` → `General`
   - 滚动到 "Workflow permissions" 部分
   - 选择 `Read and write permissions`
   - 勾选 `Allow GitHub Actions to create and approve pull requests`
   - 点击 `Save`

2. **方法二：使用 Personal Access Token**
   - 生成 PAT：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 `Generate new token (classic)`
   - 勾选 `repo` 权限
   - 复制生成的 token
   - 在仓库中添加 Secret：Settings → Secrets and variables → Actions → New repository secret
   - Name: `PAT_TOKEN`，Value: 粘贴你的 token
   - 修改 `.github/workflows/fetch-news.yml`：
     ```yaml
     - name: Checkout repository
       uses: actions/checkout@v3
       with:
         token: ${{ secrets.PAT_TOKEN }}
     ```

### 错误 2: Workflow 不执行

**原因**：
- 工作流未启用
- Cron 表达式错误
- 仓库长时间无活动被禁用

**解决方案**：
1. 检查 Actions 是否启用：`Settings` → `Actions` → `General`
2. 手动触发测试：`Actions` → `Fetch News and Analyze` → `Run workflow`
3. 如果仓库超过60天无活动，GitHub 会自动禁用定时任务，需要手动重新启用

### 错误 3: Python 依赖安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement xxx
```

**解决方案**：
- 检查 `requirements.txt` 文件格式是否正确
- 确保依赖包名称拼写正确
- 可以指定版本号：`requests==2.31.0`

---

## 🔴 Vercel 部署错误

### 错误 1: 路由配置冲突

**错误信息**：
```
If `rewrites`, `redirects`, `headers`, `cleanUrls` or `trailingSlash` are used, 
then `routes` cannot be present.
```

**解决方案**：
- 删除 `vercel.json` 中的 `routes` 配置
- 只使用 `rewrites` 和 `headers`
- 参考项目中的 `vercel.json` 文件

### 错误 2: API 返回 404

**原因**：
- API 路径配置错误
- 函数文件位置不正确

**解决方案**：
1. 确保 `api/index.py` 文件存在
2. 检查 `vercel.json` 中的路径配置
3. 重新部署：`Vercel Dashboard` → 你的项目 → `Redeploy`

### 错误 3: CORS 错误

**错误信息**：
```
Access to fetch at 'xxx' from origin 'xxx' has been blocked by CORS policy
```

**解决方案**：
- 确保 `vercel.json` 中配置了正确的 CORS 头
- 检查 `api/index.py` 中的响应头设置
- 参考项目中的配置文件

---

## 🔴 GitHub Pages 错误

### 错误 1: 页面 404

**原因**：
- GitHub Pages 未启用
- 分支或目录配置错误

**解决方案**：
1. 进入 `Settings` → `Pages`
2. Source 选择 `Deploy from a branch`
3. Branch 选择 `main`，目录选择 `/docs`
4. 点击 `Save`
5. 等待 2-3 分钟后访问

### 错误 2: 页面显示但无数据

**原因**：
- API 地址未更新
- 数据文件未生成

**解决方案**：
1. 检查 `docs/main.js` 中的 `API_BASE` 是否正确
2. 手动触发 GitHub Actions 生成数据
3. 检查 `data/news.json` 和 `data/analysis.json` 是否存在

### 错误 3: 样式错误或显示异常

**原因**：
- CDN 资源加载失败
- 浏览器缓存问题

**解决方案**：
1. 清除浏览器缓存（Ctrl+Shift+Delete）
2. 强制刷新页面（Ctrl+F5）
3. 检查浏览器控制台是否有错误信息

---

## 🔴 数据爬取错误

### 错误 1: 无法获取新闻

**错误信息**：
```
获取RSS订阅源失败: Connection timeout
```

**原因**：
- 网络连接问题
- RSS 源不可用
- 被反爬虫机制拦截

**解决方案**：
1. 检查 RSS 源是否可访问（在浏览器中打开 URL）
2. 更换其他新闻源
3. 添加更多 User-Agent 轮换
4. 增加请求间隔时间

### 错误 2: 解析 RSS 失败

**错误信息**：
```
解析RSS项目时出错: 'NoneType' object has no attribute 'text'
```

**原因**：
- RSS 格式不标准
- 必需字段缺失

**解决方案**：
- 在代码中添加更多的空值检查
- 使用 try-except 包裹解析逻辑
- 参考 `scripts/fetch_news.py` 中的错误处理

### 错误 3: 数据为空或使用模拟数据

**原因**：
- 所有新闻源都失败
- 网络限制

**解决方案**：
1. 检查 GitHub Actions 日志，查看具体错误
2. 尝试添加更多新闻源
3. 考虑使用付费 API（如 NewsAPI.org）

---

## 🔴 本地开发错误

### 错误 1: 无法读取数据文件

**错误信息**：
```
Failed to load resource: net::ERR_FILE_NOT_FOUND
```

**原因**：
- 数据文件不存在
- 路径配置错误

**解决方案**：
1. 先运行爬虫脚本生成数据：
   ```bash
   python scripts/fetch_news.py
   ```
2. 确保 `data/news.json` 和 `data/analysis.json` 存在
3. 使用本地服务器运行（不要直接打开 HTML 文件）：
   ```bash
   # Python
   cd docs
   python -m http.server 8000
   
   # Node.js
   npx serve docs
   ```

### 错误 2: Python 依赖缺失

**错误信息**：
```
ModuleNotFoundError: No module named 'requests'
```

**解决方案**：
```bash
pip install -r requirements.txt
```

---

## 📝 最佳实践

### 1. 定期检查

- 每周检查一次 GitHub Actions 运行状态
- 查看健康检查页面：`https://your-username.github.io/your-repo/health.html`
- 监控 Vercel 部署状态

### 2. 数据备份

- GitHub 自动保存所有历史数据
- 可以通过 Git 历史查看过往数据
- 建议定期导出重要数据

### 3. 性能优化

- 限制新闻数量（默认每源10-15条）
- 增加请求间隔避免被封禁
- 使用 CDN 加速静态资源

### 4. 安全建议

- 不要在代码中硬编码 API 密钥
- 使用 GitHub Secrets 存储敏感信息
- 定期更新依赖包版本

---

## 🆘 获取帮助

如果以上方案都无法解决你的问题：

1. **查看日志**：
   - GitHub Actions: `Actions` → 点击失败的运行 → 查看详细日志
   - Vercel: `Dashboard` → 你的项目 → `Deployments` → 点击部署 → `View Function Logs`
   - 浏览器: F12 打开开发者工具 → `Console` 标签

2. **搜索错误信息**：
   - 复制完整的错误信息
   - 在 Google 或 Stack Overflow 搜索

3. **提交 Issue**：
   - 在 GitHub 仓库提交 Issue
   - 包含完整的错误信息和日志
   - 说明你的操作步骤

4. **社区求助**：
   - GitHub Discussions
   - Stack Overflow
   - Reddit r/github

---

**最后更新**: 2025-10-23
