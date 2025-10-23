// API基础URL - 替换为你的Vercel部署URL
const API_BASE = 'https://ai-394y.vercel.app/api';

// 如果在本地开发，可以使用相对路径读取data目录
const USE_LOCAL_DATA = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

// 全局状态
let currentCategory = '';
let temperatureChart = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initApp();
    setupEventListeners();
});

// 初始化应用
async function initApp() {
    await loadStats();
    await loadCategories();
    await loadNews();
    await loadAnalysis();
    initTemperatureChart();
}

// 设置事件监听器
function setupEventListeners() {
    document.getElementById('refreshBtn').addEventListener('click', () => {
        location.reload();
    });
}

// 加载统计数据
async function loadStats() {
    try {
        let data;
        
        if (USE_LOCAL_DATA) {
            // 本地开发模式：直接读取JSON文件
            const newsResponse = await fetch('../data/news.json');
            const newsData = await newsResponse.json();
            const analysisResponse = await fetch('../data/analysis.json');
            const analysisData = await analysisResponse.json();
            
            const today = new Date().toISOString().split('T')[0];
            const newsToday = newsData.news.filter(n => 
                n.published_at.startsWith(today)
            ).length;
            
            data = {
                news_total: newsData.total_count,
                news_today: newsToday,
                latest_temperature: {
                    temperature_score: analysisData.temperature_score,
                    sentiment: analysisData.sentiment
                },
                updated_at: newsData.updated_at
            };
        } else {
            // 生产模式：调用Vercel API
            const response = await fetch(`${API_BASE}/stats/overview`);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error);
            }
            
            data = result.data;
        }
        
        document.getElementById('newsTotal').textContent = data.news_total || 0;
        document.getElementById('newsToday').textContent = data.news_today || 0;
        
        if (data.latest_temperature) {
            document.getElementById('tempScore').textContent = 
                data.latest_temperature.temperature_score.toFixed(1);
            document.getElementById('sentiment').textContent = 
                data.latest_temperature.sentiment;
        }
        
        if (data.updated_at) {
            const updateTime = new Date(data.updated_at);
            document.getElementById('updateTime').textContent = 
                `更新于: ${updateTime.toLocaleString('zh-CN')}`;
        }
    } catch (error) {
        console.error('加载统计数据失败:', error);
        showNotification('加载统计数据失败', 'error');
    }
}

// 加载新闻分类
async function loadCategories() {
    try {
        let categories;
        
        if (USE_LOCAL_DATA) {
            const response = await fetch('../data/news.json');
            const newsData = await response.json();
            
            const categoryCount = {};
            newsData.news.forEach(news => {
                const cat = news.category || '其他';
                categoryCount[cat] = (categoryCount[cat] || 0) + 1;
            });
            
            categories = Object.entries(categoryCount)
                .map(([category, count]) => ({ category, count }))
                .sort((a, b) => b.count - a.count);
        } else {
            const response = await fetch(`${API_BASE}/news/categories`);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error);
            }
            
            categories = result.data;
        }
        
        if (categories && categories.length > 0) {
            const container = document.getElementById('categoryFilter');
            
            categories.forEach(cat => {
                const btn = document.createElement('button');
                btn.className = 'category-btn';
                btn.dataset.category = cat.category;
                btn.innerHTML = `
                    <i class="fas fa-tag mr-2"></i>
                    ${cat.category} (${cat.count})
                `;
                btn.addEventListener('click', () => filterByCategory(cat.category, btn));
                container.appendChild(btn);
            });
        }
    } catch (error) {
        console.error('加载分类失败:', error);
    }
}

// 按分类筛选
function filterByCategory(category, btn) {
    currentCategory = category;
    
    // 更新按钮状态
    document.querySelectorAll('.category-btn').forEach(b => {
        b.classList.remove('active');
    });
    btn.classList.add('active');
    
    // 重新加载新闻
    loadNews();
}

// 加载新闻列表
async function loadNews() {
    const container = document.getElementById('newsList');
    const loading = document.getElementById('loading');
    
    loading.classList.remove('hidden');
    container.innerHTML = '';
    
    try {
        let newsList;
        
        if (USE_LOCAL_DATA) {
            const response = await fetch('../data/news.json');
            const newsData = await response.json();
            newsList = newsData.news;
            
            if (currentCategory) {
                newsList = newsList.filter(n => n.category === currentCategory);
            }
            
            newsList = newsList.slice(0, 20);
        } else {
            let url = `${API_BASE}/news/latest?limit=20`;
            if (currentCategory) {
                url += `&category=${encodeURIComponent(currentCategory)}`;
            }
            
            const response = await fetch(url);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error);
            }
            
            newsList = result.data;
        }
        
        if (newsList && newsList.length > 0) {
            newsList.forEach((news, index) => {
                const card = createNewsCard(news, index);
                container.appendChild(card);
            });
        } else {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <i class="fas fa-inbox text-6xl text-gray-300 mb-4"></i>
                    <p class="text-gray-500 text-lg">暂无新闻数据</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('加载新闻失败:', error);
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
        <img src="${news.image_url || 'https://via.placeholder.com/400x200?text=News'}" 
             alt="${news.title}" 
             class="news-card-image"
             onerror="this.src='https://via.placeholder.com/400x200?text=News'">
        <div class="news-card-content">
            <h3 class="news-card-title">${news.title}</h3>
            <p class="news-card-description">${news.description || '暂无描述'}</p>
            <div class="news-card-meta">
                <div class="flex items-center space-x-2">
                    <span class="news-card-badge">${news.category}</span>
                    <span><i class="fas fa-map-marker-alt mr-1"></i>${news.country}</span>
                </div>
                <div class="flex items-center space-x-3">
                    <span><i class="fas fa-newspaper mr-1"></i>${news.source}</span>
                    <span><i class="fas fa-clock mr-1"></i>${timeAgo}</span>
                </div>
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

// 加载分析结果
async function loadAnalysis() {
    try {
        let analysisData;
        
        if (USE_LOCAL_DATA) {
            const response = await fetch('../data/analysis.json');
            analysisData = await response.json();
        } else {
            const response = await fetch(`${API_BASE}/temperature/latest`);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error);
            }
            
            analysisData = result.data;
        }
        
        if (analysisData) {
            // 更新温度计
            if (temperatureChart) {
                temperatureChart.setOption({
                    series: [{
                        data: [{
                            value: analysisData.temperature_score,
                            name: '投资温度'
                        }],
                        itemStyle: {
                            color: getTemperatureColor(analysisData.temperature_score)
                        },
                        anchor: {
                            itemStyle: {
                                borderColor: getTemperatureColor(analysisData.temperature_score)
                            }
                        }
                    }]
                });
            }
            
            // 更新分析文本
            document.getElementById('analysisText').textContent = analysisData.analysis_text;
            
            // 更新关键因素
            const factorsList = document.getElementById('keyFactors');
            if (analysisData.key_factors && analysisData.key_factors.length > 0) {
                factorsList.innerHTML = analysisData.key_factors.map(factor => `
                    <li class="flex items-start fade-in">
                        <i class="fas fa-circle text-xs ${factor.startsWith('✓') ? 'text-green-500' : 'text-red-500'} mt-1.5 mr-2"></i>
                        <span>${factor}</span>
                    </li>
                `).join('');
            }
            
            // 更新积极/消极计数
            document.getElementById('positiveCount').textContent = analysisData.positive_count || 0;
            document.getElementById('negativeCount').textContent = analysisData.negative_count || 0;
        }
    } catch (error) {
        console.error('加载分析结果失败:', error);
    }
}

// 初始化温度计图表
function initTemperatureChart() {
    const chartDom = document.getElementById('temperatureGauge');
    temperatureChart = echarts.init(chartDom);
    
    const option = {
        series: [
            {
                type: 'gauge',
                startAngle: 180,
                endAngle: 0,
                min: 0,
                max: 100,
                splitNumber: 10,
                itemStyle: {
                    color: '#FF6B6B'
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
                            [0.3, '#FF6B6B'],
                            [0.7, '#FFD93D'],
                            [1, '#6BCF7F']
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
                        borderColor: '#FF6B6B'
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
                data: [
                    {
                        value: 50,
                        name: '投资温度'
                    }
                ]
            }
        ]
    };
    
    temperatureChart.setOption(option);
    
    // 响应式
    window.addEventListener('resize', () => {
        temperatureChart.resize();
    });
}

// 根据温度获取颜色
function getTemperatureColor(temp) {
    if (temp >= 70) return '#6BCF7F';
    if (temp >= 50) return '#FFD93D';
    return '#FF6B6B';
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
    }, 3000);
}
