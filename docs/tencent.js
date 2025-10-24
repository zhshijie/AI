// API基础URL - 替换为你的Vercel部署URL
const API_BASE = 'https://ai-394y.vercel.app/api';


// 全局变量
let temperatureChart = null;
let categoryChart = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
});

// 初始化应用
async function initApp() {
    await loadData();
    initCharts();
}

// 设置事件监听器
function setupEventListeners() {
    document.getElementById('refreshBtn').addEventListener('click', () => {
        location.reload();
    });
}

// 加载数据
async function loadData() {
    try {
        let newsData, analysisData;

        // 尝试加载数据
        try {
            // 生产环境：调用Vercel API
            // 注意：需要在 api/index.py 中添加腾讯新闻相关的API端点
            const newsResponse = await fetch(`${API_BASE}/tencent/news`);
            const analysisResponse = await fetch(`${API_BASE}/tencent/analysis`);

            if (!newsResponse.ok || !analysisResponse.ok) {
                throw new Error('API请求失败');
            }

            const newsResult = await newsResponse.json();
            const analysisResult = await analysisResponse.json();

            if (!newsResult.success || !analysisResult.success) {
                throw new Error(newsResult.error || analysisResult.error || 'API返回错误');
            }

            newsData = newsResult.data;
            analysisData = analysisResult.data;
        } catch (fetchError) {
            console.warn('数据加载失败，使用演示数据:', fetchError);
            // 使用演示数据
            const demoData = generateDemoData();
            newsData = demoData.news;
            analysisData = demoData.analysis;
            showNotification('使用演示数据，请运行爬虫脚本获取真实数据', 'info');
        }

        // 更新UI
        updateStats(newsData, analysisData);
        updateAdvice(analysisData);
        updateCharts(analysisData);
        updateNewsList(newsData);

    } catch (error) {
        console.error('加载数据失败:', error);
        showNotification('加载数据失败: ' + error.message, 'error');
    }
}

// 更新统计数据
function updateStats(newsData, analysisData) {
    document.getElementById('newsTotal').textContent = newsData.total_count || 0;
    document.getElementById('tempScore').textContent = analysisData.temperature_score.toFixed(1) + '°';
    document.getElementById('sentiment').textContent = analysisData.sentiment + ' ' + analysisData.sentiment_emoji;
    document.getElementById('rating').textContent = analysisData.investment_advice.overall_rating;

    if (newsData.updated_at) {
        const updateTime = new Date(newsData.updated_at);
        document.getElementById('updateTime').textContent =
            `更新于: ${updateTime.toLocaleString('zh-CN')}`;
    }
}

// 更新投资建议
function updateAdvice(analysisData) {
    const advice = analysisData.investment_advice;

    // 更新风险等级徽章
    const riskBadge = document.getElementById('riskBadge');
    riskBadge.textContent = advice.risk_level;
    riskBadge.className = 'risk-badge ' + getRiskClass(advice.risk_level);

    // 更新综合评估
    document.getElementById('recommendation').textContent = advice.recommendation;
    document.getElementById('riskLevel').textContent = advice.risk_level;
    document.getElementById('positiveCount').textContent = analysisData.positive_count;
    document.getElementById('negativeCount').textContent = analysisData.negative_count;
    document.getElementById('detailedAnalysis').textContent = advice.detailed_analysis;

    // 更新投资机会
    const opportunitiesList = document.getElementById('opportunities');
    opportunitiesList.innerHTML = advice.key_opportunities.map(item => `
        <li class="flex items-start fade-in">
            <i class="fas fa-check-circle text-green-500 mt-1 mr-2"></i>
            <span class="text-gray-700">${item}</span>
        </li>
    `).join('');

    // 更新投资风险
    const risksList = document.getElementById('risks');
    risksList.innerHTML = advice.key_risks.map(item => `
        <li class="flex items-start fade-in">
            <i class="fas fa-times-circle text-red-500 mt-1 mr-2"></i>
            <span class="text-gray-700">${item}</span>
        </li>
    `).join('');

    // 更新行动建议
    const actionItems = document.getElementById('actionItems');
    actionItems.innerHTML = advice.action_items.map((item, index) => `
        <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 fade-in" style="animation-delay: ${index * 0.1}s;">
            <div class="flex items-start">
                <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold mr-3">
                    ${index + 1}
                </div>
                <p class="text-gray-700 flex-1">${item}</p>
            </div>
        </div>
    `).join('');

    // 更新关键因素
    const keyFactors = document.getElementById('keyFactors');
    keyFactors.innerHTML = analysisData.key_factors.map(factor => {
        const isPositive = factor.type === 'positive';
        return `
            <div class="flex items-start fade-in bg-${isPositive ? 'green' : 'red'}-50 rounded-lg p-4">
                <i class="fas fa-circle text-xs text-${isPositive ? 'green' : 'red'}-500 mt-2 mr-3"></i>
                <div class="flex-1">
                    <span class="category-badge mb-2">${factor.category}</span>
                    <p class="text-gray-700 mt-2">${factor.title}</p>
                </div>
            </div>
        `;
    }).join('');
}

// 获取风险等级样式类
function getRiskClass(riskLevel) {
    if (riskLevel.includes('低')) return 'risk-low';
    if (riskLevel.includes('高')) return 'risk-high';
    return 'risk-medium';
}

// 初始化图表
function initCharts() {
    // 温度计图表
    const tempDom = document.getElementById('temperatureGauge');
    temperatureChart = echarts.init(tempDom);

    const tempOption = {
        series: [{
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 100,
            splitNumber: 10,
            itemStyle: {
                color: '#667eea'
            },
            progress: {
                show: true,
                width: 18
            },
            pointer: {
                show: true,
                length: '70%',
                width: 8
            },
            axisLine: {
                lineStyle: {
                    width: 18,
                    color: [
                        [0.3, '#ef4444'],
                        [0.7, '#f59e0b'],
                        [1, '#10b981']
                    ]
                }
            },
            axisTick: {
                distance: -25,
                splitNumber: 5,
                lineStyle: {
                    width: 2,
                    color: '#999'
                }
            },
            splitLine: {
                distance: -30,
                length: 14,
                lineStyle: {
                    width: 3,
                    color: '#999'
                }
            },
            axisLabel: {
                distance: -50,
                color: '#999',
                fontSize: 14
            },
            anchor: {
                show: true,
                showAbove: true,
                size: 20,
                itemStyle: {
                    borderWidth: 8,
                    borderColor: '#667eea'
                }
            },
            title: {
                show: true,
                offsetCenter: [0, '80%'],
                fontSize: 16,
                color: '#666'
            },
            detail: {
                valueAnimation: true,
                fontSize: 40,
                offsetCenter: [0, '50%'],
                formatter: '{value}°',
                color: 'auto'
            },
            data: [{
                value: 50,
                name: '投资温度'
            }]
        }]
    };

    temperatureChart.setOption(tempOption);

    // 分类图表
    const catDom = document.getElementById('categoryChart');
    categoryChart = echarts.init(catDom);

    const catOption = {
        title: {
            text: '新闻分类分布',
            left: 'center',
            textStyle: {
                fontSize: 16,
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            top: 'middle'
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 20,
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: []
        }]
    };

    categoryChart.setOption(catOption);

    // 响应式
    window.addEventListener('resize', () => {
        temperatureChart.resize();
        categoryChart.resize();
    });
}

// 更新图表
function updateCharts(analysisData) {
    // 更新温度计
    if (temperatureChart) {
        temperatureChart.setOption({
            series: [{
                data: [{
                    value: analysisData.temperature_score,
                    name: '投资温度'
                }]
            }]
        });
    }

    // 更新分类图表
    if (categoryChart && analysisData.categories_distribution) {
        const categoryData = Object.entries(analysisData.categories_distribution).map(([name, value]) => ({
            name,
            value
        }));

        categoryChart.setOption({
            series: [{
                data: categoryData
            }]
        });
    }
}

// 更新新闻列表
function updateNewsList(newsData) {
    const container = document.getElementById('newsList');
    const loading = document.getElementById('loading');

    loading.classList.remove('hidden');
    container.innerHTML = '';

    try {
        const newsList = newsData.news || [];

        if (newsList.length > 0) {
            newsList.forEach((news, index) => {
                const card = createNewsCard(news, index);
                container.appendChild(card);
            });
        } else {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="fas fa-inbox text-6xl text-gray-300 mb-4"></i>
                    <p class="text-gray-500 text-lg">暂无新闻数据</p>
                    <p class="text-gray-400 text-sm mt-2">请运行爬虫脚本获取最新数据</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('更新新闻列表失败:', error);
        container.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-exclamation-circle text-6xl text-red-300 mb-4"></i>
                <p class="text-red-500 text-lg">加载失败: ${error.message}</p>
            </div>
        `;
    } finally {
        loading.classList.add('hidden');
    }
}

// 创建新闻卡片
function createNewsCard(news, index) {
    const card = document.createElement('div');
    card.className = 'news-card fade-in';
    card.style.animationDelay = `${index * 0.05}s`;

    const publishedDate = new Date(news.published_at);
    const timeAgo = getTimeAgo(publishedDate);

    card.innerHTML = `
        <img src="${news.image_url || 'https://via.placeholder.com/400x200?text=Tencent+News'}" 
             alt="${news.title}" 
             class="news-card-image"
             onerror="this.src='https://via.placeholder.com/400x200?text=Tencent+News'">
        <div class="p-4 flex-1 flex flex-direction-column">
            <h3 class="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">${news.title}</h3>
            <p class="text-gray-600 text-sm mb-4 line-clamp-3 flex-1">${news.description || '暂无描述'}</p>
            <div class="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
                <div class="flex items-center space-x-2">
                    <span class="category-badge">${news.category}</span>
                    <span><i class="fas fa-newspaper mr-1"></i>${news.source}</span>
                </div>
                <span><i class="fas fa-clock mr-1"></i>${timeAgo}</span>
            </div>
        </div>
    `;

    if (news.url) {
        card.addEventListener('click', () => {
            window.open(news.url, '_blank');
        });
    }

    return card;
}

// 计算时间差
function getTimeAgo(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return '刚刚';
    if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`;
    if (diff < 2592000) return `${Math.floor(diff / 86400)}天前`;
    return date.toLocaleDateString('zh-CN');
}

// 显示通知
function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500'
    };

    const notification = document.createElement('div');
    notification.className = `fixed top-20 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 fade-in`;
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        notification.style.transition = 'all 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// 生成演示数据
function generateDemoData() {
    const now = new Date().toISOString();

    return {
        news: {
            updated_at: now,
            total_count: 6,
            news: [
                {
                    id: 1,
                    title: '腾讯Q3财报超预期，游戏收入同比增长20%',
                    description: '腾讯控股公布第三季度财报，游戏业务收入实现强劲增长，超出市场预期。《王者荣耀》和《和平精英》继续保持领先地位。',
                    url: 'https://example.com/news1',
                    source: 'Reuters',
                    published_at: now,
                    category: '股市表现',
                    country: 'China',
                    image_url: 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/c114dc3c-72a6-44d4-93a8-b97d0608ad58/image_1761210122_4_1.png',
                    fetched_at: now,
                    relevance_score: 5
                },
                {
                    id: 2,
                    title: '微信推出AI驱动的企业服务新功能',
                    description: '腾讯微信平台推出创新AI功能，旨在增强企业通信和客户服务能力，助力企业数字化转型。',
                    url: 'https://example.com/news2',
                    source: 'TechCrunch',
                    published_at: now,
                    category: 'AI技术',
                    country: 'Global',
                    image_url: 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/5f2cdbe0-ff90-4dd6-847d-f845db12d841/image_1761210122_6_1.jpg',
                    fetched_at: now,
                    relevance_score: 4
                },
                {
                    id: 3,
                    title: '腾讯云扩大国际布局，新增东南亚和欧洲数据中心',
                    description: '腾讯云宣布扩张计划，在东南亚和欧洲新建数据中心，与AWS和Azure展开竞争。',
                    url: 'https://example.com/news3',
                    source: 'Bloomberg',
                    published_at: now,
                    category: '云服务',
                    country: 'Global',
                    image_url: 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/d73313bb-1da1-4247-8ca6-de693c674018/image_1761210124_5_1.png',
                    fetched_at: now,
                    relevance_score: 4
                },
                {
                    id: 4,
                    title: '中国监管机构批准腾讯多款新游戏',
                    description: '中国游戏监管机构批准腾讯多款新游戏上线，显示监管环境趋于友好。',
                    url: 'https://example.com/news4',
                    source: 'CNBC',
                    published_at: now,
                    category: '政策监管',
                    country: 'China',
                    image_url: 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/e21eb98a-5751-440c-8dc6-b04471809fc8/image_1761210124_7_1.png',
                    fetched_at: now,
                    relevance_score: 5
                },
                {
                    id: 5,
                    title: '腾讯音乐在竞争中实现用户增长',
                    description: '尽管面临激烈竞争，腾讯音乐娱乐报告用户稳定增长和改进的变现策略。',
                    url: 'https://example.com/news5',
                    source: 'Financial Times',
                    published_at: now,
                    category: '数字内容',
                    country: 'China',
                    image_url: 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/c114dc3c-72a6-44d4-93a8-b97d0608ad58/image_1761210122_4_1.png',
                    fetched_at: now,
                    relevance_score: 3
                },
                {
                    id: 6,
                    title: '腾讯投资元宇宙初创企业，着眼未来增长',
                    description: '腾讯宣布对多家元宇宙和VR技术初创企业进行战略投资，作为长期增长战略的一部分。',
                    url: 'https://example.com/news6',
                    source: 'TechNode',
                    published_at: now,
                    category: '元宇宙',
                    country: 'Global',
                    image_url: 'https://zhiyan-ai-agent-with-1258344702.cos.ap-guangzhou.tencentcos.cn/with/5f2cdbe0-ff90-4dd6-847d-f845db12d841/image_1761210122_6_1.jpg',
                    fetched_at: now,
                    relevance_score: 4
                }
            ]
        },
        analysis: {
            temperature_score: 72.5,
            sentiment: '乐观',
            sentiment_emoji: '😊',
            investment_advice: {
                overall_rating: '强烈看好',
                risk_level: '中等风险',
                recommendation: '建议增持',
                detailed_analysis: '基于最新6条新闻分析，腾讯整体表现积极（积极新闻4条，占比66.7%）。多项业务板块展现强劲增长势头，市场情绪乐观，投资价值凸显。游戏业务持续增长，云服务扩张顺利，监管环境改善，为未来发展奠定良好基础。',
                key_opportunities: [
                    '游戏业务持续增长，新游戏上线表现强劲',
                    '云服务市场份额扩大，企业数字化转型需求旺盛',
                    '社交平台用户活跃度提升，广告收入增长潜力大',
                    'AI技术应用落地，为各业务线赋能',
                    '监管环境改善，政策风险降低'
                ],
                key_risks: [
                    '市场竞争加剧需要持续创新投入',
                    '国际业务扩张面临地缘政治风险'
                ],
                action_items: [
                    '建议在当前价位适度增持，目标仓位可提升至15-20%',
                    '重点关注季度财报，特别是游戏和云服务收入',
                    '设置止盈点，建议在上涨20%后分批获利了结',
                    '长期持有，关注3-6个月的业绩表现'
                ]
            },
            key_factors: [
                {
                    type: 'positive',
                    category: '股市表现',
                    title: '腾讯Q3财报超预期，游戏收入同比增长20%'
                },
                {
                    type: 'positive',
                    category: 'AI技术',
                    title: '微信推出AI驱动的企业服务新功能'
                },
                {
                    type: 'positive',
                    category: '云服务',
                    title: '腾讯云扩大国际布局，新增东南亚和欧洲数据中心'
                },
                {
                    type: 'positive',
                    category: '政策监管',
                    title: '中国监管机构批准腾讯多款新游戏'
                },
                {
                    type: 'positive',
                    category: '数字内容',
                    title: '腾讯音乐在竞争中实现用户增长'
                },
                {
                    type: 'positive',
                    category: '元宇宙',
                    title: '腾讯投资元宇宙初创企业，着眼未来增长'
                }
            ],
            positive_count: 5,
            negative_count: 1,
            neutral_count: 0,
            analyzed_news_count: 6,
            analyzed_at: now,
            categories_distribution: {
                '股市表现': 1,
                'AI技术': 1,
                '云服务': 1,
                '政策监管': 1,
                '数字内容': 1,
                '元宇宙': 1
            },
            category_sentiment: {
                '股市表现': { positive: 1, negative: 0, neutral: 0 },
                'AI技术': { positive: 1, negative: 0, neutral: 0 },
                '云服务': { positive: 1, negative: 0, neutral: 0 },
                '政策监管': { positive: 1, negative: 0, neutral: 0 },
                '数字内容': { positive: 1, negative: 0, neutral: 0 },
                '元宇宙': { positive: 1, negative: 0, neutral: 0 }
            }
        }
    };
}
