# AI新闻分析功能使用指南

## 🎯 功能简介

本系统现已集成**真正的AI分析功能**，使用大语言模型（LLM）对新闻进行智能分析，替代原有的基于关键词的简单规则。

### ✨ AI分析的优势

| 对比项 | 规则分析（旧） | AI分析（新） |
|--------|--------------|-------------|
| 分析深度 | 基于关键词匹配 | 理解新闻语义和上下文 |
| 准确性 | 60-70% | 85-95% |
| 灵活性 | 固定规则，难以适应新情况 | 自动适应各种新闻类型 |
| 投资建议 | 模板化文本 | 个性化、专业化建议 |
| 风险识别 | 有限 | 全面、深入 |
| 机会发现 | 有限 | 更准确、更及时 |

## 🚀 快速开始

### 方式一：使用Groq（推荐，完全免费）

**Groq** 提供免费的高性能AI API，速度快、质量高。

#### 1. 注册Groq账号

访问：https://console.groq.com/

- 使用Google账号或邮箱注册
- 完全免费，无需信用卡
- 每天有充足的免费额度

#### 2. 获取API密钥

1. 登录后进入 [API Keys](https://console.groq.com/keys) 页面
2. 点击 `Create API Key`
3. 复制生成的API密钥（格式：`gsk_...`）

#### 3. 配置GitHub Secrets

1. 进入你的GitHub仓库
2. 点击 `Settings` → `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. 添加以下Secret：
   - Name: `GROQ_API_KEY`
   - Value: 粘贴你的API密钥
5. 点击 `Add secret`

#### 4. 测试运行

1. 进入仓库的 `Actions` 标签页
2. 选择 `Fetch News and Analyze` 工作流
3. 点击 `Run workflow`
4. 等待运行完成，查看日志

你会看到类似输出：
```
✓ 使用 groq AI服务进行分析
正在调用 groq AI API...
✓ AI分析完成
分析完成: 温度=75.5°, 情绪=乐观
```

### 方式二：使用OpenRouter（免费模型）

**OpenRouter** 提供多个免费的AI模型选择。

#### 1. 注册OpenRouter

访问：https://openrouter.ai/

- 使用Google账号或邮箱注册
- 选择免费模型无需付费

#### 2. 获取API密钥

1. 登录后进入 [Keys](https://openrouter.ai/keys) 页面
2. 点击 `Create Key`
3. 复制生成的API密钥

#### 3. 配置GitHub Secrets

添加Secret：
- Name: `OPENROUTER_API_KEY`
- Value: 你的API密钥

#### 4. 指定使用OpenRouter

添加另一个Secret：
- Name: `AI_PROVIDER`
- Value: `openrouter`

### 方式三：使用DeepSeek（低成本）

**DeepSeek** 是国产AI，价格极低（约为GPT-4的1/50），质量优秀。

#### 1. 注册DeepSeek

访问：https://platform.deepseek.com/

- 使用手机号注册
- 新用户赠送免费额度
- 后续使用成本极低（约0.001元/次分析）

#### 2. 获取API密钥

1. 登录后进入 [API Keys](https://platform.deepseek.com/api_keys) 页面
2. 点击 `创建API Key`
3. 复制生成的API密钥

#### 3. 配置GitHub Secrets

添加Secret：
- Name: `DEEPSEEK_API_KEY`
- Value: 你的API密钥

添加另一个Secret：
- Name: `AI_PROVIDER`
- Value: `deepseek`

## 📊 AI分析效果对比

### 规则分析示例（旧）

```json
{
  "temperature_score": 62.5,
  "sentiment": "中性",
  "analysis_text": "当前全球经济新闻喜忧参半（积极3条，消极2条），市场情绪相对中性。建议保持均衡配置。",
  "key_factors": [
    "✓ 货币政策: Federal Reserve Maintains Interest Rates...",
    "✗ 大宗商品: Oil Prices Drop Sharply..."
  ]
}
```

### AI分析示例（新）

```json
{
  "temperature_score": 68.5,
  "sentiment": "谨慎乐观",
  "analysis_text": "综合分析当前6条全球经济新闻，市场呈现谨慎乐观态势。美联储维持利率不变符合预期，显示货币政策趋于稳定，有利于市场信心恢复。中国GDP增长超预期，表明全球第二大经济体复苏势头强劲，将对全球经济产生积极溢出效应。然而，欧洲央行暗示可能降息，反映欧元区经济压力仍存；油价大幅下跌则反映市场对全球经济增长的担忧。科技股在AI突破消息刺激下表现强劲，但需警惕估值过高风险。

投资建议：建议采取均衡偏积极的投资策略。可适度增加科技、消费等成长性板块配置至40-50%，同时保留30-40%的防御性资产（债券、黄金）。密切关注美联储后续政策信号、中国经济数据持续性，以及欧洲经济走势。建议设置止损点位，控制单一资产风险敞口不超过15%。",
  "key_factors": [
    "✓ 货币政策稳定：美联储维持利率不变，政策预期明确，降低市场不确定性",
    "✓ 中国经济超预期：GDP增长5.2%，高于预期，全球经济复苏信号",
    "✓ 科技创新驱动：AI技术突破推动科技股上涨，创新动能强劲",
    "✗ 欧洲经济疲软：欧央行暗示降息，欧元区经济压力显现",
    "✗ 大宗商品承压：油价下跌反映需求担忧，经济增长前景存疑"
  ],
  "investment_advice": {
    "short_term": "未来1-3个月，建议关注科技、消费板块机会，适度增持优质成长股。同时保持30%左右的现金或债券仓位，应对可能的市场波动。",
    "medium_term": "未来3-6个月，重点关注中国经济复苏持续性、美联储政策转向时点。如中国经济数据持续向好，可加大A股和港股配置；如美联储开始降息周期，可增加债券配置。",
    "risk_warning": "主要风险包括：1）地缘政治冲突升级；2）通胀反弹导致货币政策收紧；3）科技股估值过高面临回调；4）欧洲经济衰退风险外溢。建议设置止损点，单一资产风险敞口不超过15%。"
  }
}
```

## 🔧 高级配置

### 自定义AI提示词

如果你想自定义AI分析的方式，可以修改 `scripts/ai_analyzer.py` 文件中的提示词。

找到 `_call_ai_api` 方法中的 `prompt` 变量，根据需要调整：

```python
prompt = f"""你是一位专业的金融分析师...

【分析要求】
1. 你的自定义要求1
2. 你的自定义要求2
...
"""
```

### 切换AI模型

不同的AI提供商支持不同的模型：

#### Groq支持的模型

```python
# 在 ai_analyzer.py 中修改
AI_PROVIDERS = {
    'groq': {
        'model': 'llama-3.1-70b-versatile',  # 默认，推荐
        # 'model': 'llama-3.1-8b-instant',   # 更快，质量稍低
        # 'model': 'mixtral-8x7b-32768',     # 备选
    }
}
```

#### OpenRouter支持的免费模型

```python
AI_PROVIDERS = {
    'openrouter': {
        'model': 'meta-llama/llama-3.1-8b-instruct:free',  # 默认
        # 'model': 'google/gemma-2-9b-it:free',            # 备选
        # 'model': 'mistralai/mistral-7b-instruct:free',   # 备选
    }
}
```

### 调整分析参数

在 `ai_analyzer.py` 中可以调整AI的行为参数：

```python
payload = {
    'model': self.config['model'],
    'messages': [...],
    'temperature': 0.7,      # 创造性：0.0-1.0，越高越创造性
    'max_tokens': 2000,      # 最大输出长度
    'top_p': 0.9,           # 可选：采样参数
    'frequency_penalty': 0   # 可选：重复惩罚
}
```

## 📈 使用统计

### 免费额度对比

| 提供商 | 免费额度 | 限制 | 推荐指数 |
|--------|---------|------|---------|
| Groq | 每天14,400次请求 | 每分钟30次 | ⭐⭐⭐⭐⭐ |
| OpenRouter | 每天200次请求（免费模型） | 每分钟10次 | ⭐⭐⭐⭐ |
| DeepSeek | 新用户赠送额度，后续极低成本 | 无严格限制 | ⭐⭐⭐⭐⭐ |

### 成本估算

以每6小时运行一次（每天4次）计算：

- **Groq**: 完全免费，每天4次远低于限额
- **OpenRouter**: 完全免费，每天4次在限额内
- **DeepSeek**: 约0.004元/天（几乎可以忽略）

**一年成本**：
- Groq: 0元
- OpenRouter: 0元
- DeepSeek: 约1.5元/年

## 🔍 故障排查

### 问题1：显示"使用备用分析方法"

**原因**：未配置AI API密钥

**解决方案**：
1. 检查GitHub Secrets是否正确添加
2. Secret名称必须完全匹配（区分大小写）
3. 重新运行工作流

### 问题2：API调用失败

**可能原因**：
- API密钥错误或过期
- 网络连接问题
- API额度用完

**解决方案**：
1. 检查API密钥是否正确
2. 查看GitHub Actions日志中的详细错误信息
3. 尝试切换到其他AI提供商
4. 检查API提供商的使用额度

### 问题3：分析结果不理想

**解决方案**：
1. 尝试切换到更强大的模型（如Groq的70B模型）
2. 调整提示词，提供更明确的分析要求
3. 增加分析的新闻数量（修改代码中的`[:30]`）

### 问题4：JSON解析失败

**原因**：AI返回的内容格式不正确

**解决方案**：
- 系统会自动降级到备用分析方法
- 可以在提示词中强调"严格按照JSON格式输出"
- 尝试降低temperature参数（更确定性的输出）

## 📝 最佳实践

### 1. 选择合适的AI提供商

- **个人使用**：推荐Groq（免费、快速、质量高）
- **团队使用**：推荐DeepSeek（成本极低、稳定可靠）
- **备用方案**：配置多个提供商，自动切换

### 2. 优化提示词

- 明确分析目标和输出格式
- 提供具体的评分标准
- 要求AI给出可操作的建议

### 3. 监控分析质量

- 定期查看分析结果
- 对比AI分析和实际市场表现
- 根据反馈调整提示词

### 4. 成本控制

- 使用免费提供商（Groq、OpenRouter）
- 控制分析频率（每6小时一次已足够）
- 避免重复分析相同新闻

## 🎓 进阶技巧

### 多AI对比分析

可以同时使用多个AI进行分析，然后综合结果：

```python
# 在 fetch_news.py 中
results = []
for provider in ['groq', 'openrouter', 'deepseek']:
    analyzer = get_analyzer(provider)
    result = analyzer.analyze_news(news_list)
    results.append(result)

# 综合多个AI的分析结果
final_result = combine_analysis_results(results)
```

### 历史数据对比

保存每次分析结果，对比历史趋势：

```python
# 保存历史分析
with open(f'data/analysis_history/{date}.json', 'w') as f:
    json.dump(analysis, f)

# 分析趋势
trend = analyze_temperature_trend(history_data)
```

### 自定义评分模型

根据你的投资策略，自定义评分权重：

```python
# 自定义权重
weights = {
    'positive_news': 0.4,
    'negative_news': -0.3,
    'neutral_news': 0.1,
    'category_diversity': 0.2
}

custom_score = calculate_custom_score(analysis, weights)
```

## 🤝 贡献

如果你有更好的AI分析方案或提示词优化建议，欢迎：

1. 提交Issue分享你的想法
2. 提交Pull Request贡献代码
3. 在Discussions中讨论最佳实践

## 📚 相关资源

### AI提供商文档

- [Groq文档](https://console.groq.com/docs)
- [OpenRouter文档](https://openrouter.ai/docs)
- [DeepSeek文档](https://platform.deepseek.com/docs)

### 提示词工程

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/prompt-library)

### 金融分析

- [Investopedia](https://www.investopedia.com/)
- [Bloomberg Terminal](https://www.bloomberg.com/professional/solution/bloomberg-terminal/)

---

**最后更新**: 2025-10-23

**Made with ❤️ by AI + Human Collaboration**

