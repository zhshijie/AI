// ETF投资助手 - 主要逻辑

// 检测环境
const USE_LOCAL_DATA = window.location.hostname === 'localhost' || 
                       window.location.hostname === '127.0.0.1' ||
                       window.location.protocol === 'file:';

const USE_VERCEL_API = window.location.hostname.includes('vercel.app') ||
                       window.location.hostname.includes('github.io');

console.log('🚀 ETF投资助手初始化...');
console.log('📍 当前环境:', window.location.hostname);
console.log('📂 使用本地数据:', USE_LOCAL_DATA);
console.log('🌐 使用Vercel API:', USE_VERCEL_API);

// 加载数据
async function loadData() {
    try {
        console.log('📂 开始加载数据...');
                // 优先尝试从 Vercel API 获取
         try {
                console.log('  尝试从 Vercel API 获取数据...');
                const apiBase = window.location.origin;
                
                const [strategyResponse, dataResponse] = await Promise.all([
                    fetch(`${apiBase}/api/etf/strategy`),
                    fetch(`${apiBase}/api/etf/data`)
                ]);
                
                if (strategyResponse.ok && dataResponse.ok) {
                    const strategyResult = await strategyResponse.json();
                    const dataResult = await dataResponse.json();
                    
                    if (strategyResult.success && dataResult.success) {
                        console.log('✅ 成功从 Vercel API 加载数据');
                        return { 
                            strategy: strategyResult.data, 
                            etfData: dataResult.data 
                        };
                    }
                }
                
                console.log('  ⚠️ Vercel API 响应异常，尝试本地文件...');
            } catch (e) {
                console.log(`  ⚠️ Vercel API 失败: ${e.message}，尝试本地文件...`);
            }
        
    } catch (error) {
        console.error('❌ 数据加载失败:', error);
        return null;
    }
}

// 渲染ETF卡片
function renderETFCard(analysis, etfData) {
    const { code, name, sentiment, signal, risks, realtime, indicators } = analysis;
    
    // 确定涨跌颜色
    const priceClass = realtime.change_percent >= 0 ? 'price-up' : 'price-down';
    const priceSymbol = realtime.change_percent >= 0 ? '+' : '';
    
    // 确定信号样式
    let signalClass = 'signal-hold';
    if (signal.action_code === 'buy' || signal.action_code === 'strong_buy') {
        signalClass = 'signal-buy';
    } else if (signal.action_code === 'sell' || signal.action_code === 'reduce') {
        signalClass = 'signal-sell';
    }
    
    // 找到对应的完整ETF数据
    const fullData = etfData.etfs.find(e => e.code === code);
    const historical = fullData ? fullData.historical : [];
    
    const card = document.createElement('div');
    card.className = 'card p-6';
    card.innerHTML = `
        <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
                <h3 class="text-2xl font-bold text-gray-800">${name}</h3>
                <span class="text-sm text-gray-500">${code}</span>
            </div>
            <div class="flex items-end gap-4">
                <div class="text-4xl font-bold ${priceClass}">
                    ¥${realtime.current.toFixed(3)}
                </div>
                <div class="text-xl ${priceClass} mb-1">
                    ${priceSymbol}${realtime.change_percent.toFixed(2)}%
                </div>
            </div>
        </div>

        <!-- 市场情绪 -->
        <div class="mb-4 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg">
            <div class="flex items-center justify-between">
                <div>
                    <div class="text-sm text-gray-600 mb-1">市场情绪</div>
                    <div class="text-2xl font-bold text-gray-800">
                        ${sentiment.emoji} ${sentiment.sentiment}
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-sm text-gray-600 mb-1">情绪评分</div>
                    <div class="text-3xl font-bold text-purple-600">${sentiment.score}</div>
                </div>
            </div>
            <div class="mt-2 bg-gray-200 rounded-full h-2">
                <div class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500" 
                     style="width: ${sentiment.score}%"></div>
            </div>
        </div>

        <!-- 投资建议 -->
        <div class="mb-4 p-4 ${signalClass} rounded-lg">
            <div class="flex items-center justify-between">
                <div>
                    <div class="text-sm opacity-90 mb-1">投资建议</div>
                    <div class="text-2xl font-bold">${signal.action}</div>
                </div>
                <div class="text-right">
                    <div class="text-sm opacity-90 mb-1">置信度</div>
                    <div class="text-3xl font-bold">${signal.confidence}%</div>
                </div>
            </div>
            <div class="mt-2 text-sm opacity-90">
                买入信号: ${signal.buy_signals} | 卖出信号: ${signal.sell_signals}
            </div>
        </div>

        <!-- 技术指标 -->
        <div class="mb-4">
            <h4 class="text-lg font-bold text-gray-800 mb-3">📊 技术指标</h4>
            <div class="grid grid-cols-2 gap-3">
                <div class="p-3 bg-gray-50 rounded-lg">
                    <div class="text-xs text-gray-600 mb-1">RSI(14)</div>
                    <div class="text-lg font-bold text-gray-800">${indicators.rsi.toFixed(1)}</div>
                    <div class="text-xs ${indicators.rsi > 70 ? 'text-red-600' : indicators.rsi < 30 ? 'text-green-600' : 'text-gray-500'}">
                        ${indicators.rsi > 70 ? '超买' : indicators.rsi < 30 ? '超卖' : '正常'}
                    </div>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                    <div class="text-xs text-gray-600 mb-1">MACD</div>
                    <div class="text-lg font-bold text-gray-800">${indicators.macd.macd.toFixed(4)}</div>
                    <div class="text-xs ${indicators.macd.macd > 0 ? 'text-red-600' : 'text-green-600'}">
                        ${indicators.macd.dif > indicators.macd.dea ? '金叉' : '死叉'}
                    </div>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                    <div class="text-xs text-gray-600 mb-1">MA5</div>
                    <div class="text-lg font-bold text-gray-800">${indicators.ma5.toFixed(3)}</div>
                </div>
                <div class="p-3 bg-gray-50 rounded-lg">
                    <div class="text-xs text-gray-600 mb-1">MA20</div>
                    <div class="text-lg font-bold text-gray-800">${indicators.ma20.toFixed(3)}</div>
                </div>
            </div>
        </div>

        <!-- K线图 -->
        <div class="mb-4">
            <h4 class="text-lg font-bold text-gray-800 mb-3">📈 价格走势</h4>
            <div id="chart-${code}" style="height: 250px;"></div>
        </div>

        <!-- 风险提示 -->
        <div>
            <h4 class="text-lg font-bold text-gray-800 mb-3">⚠️ 风险提示</h4>
            <div class="space-y-2">
                ${risks.slice(0, 3).map(risk => `
                    <div class="p-3 rounded-lg risk-${risk.level}">
                        <div class="font-bold text-sm mb-1">${risk.type}</div>
                        <div class="text-sm text-gray-700">${risk.description}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    return { card, chartId: `chart-${code}`, historical };
}

// 渲染K线图
function renderChart(chartId, historical) {
    const chartDom = document.getElementById(chartId);
    if (!chartDom || !historical || historical.length === 0) return;
    
    const chart = echarts.init(chartDom);
    
    const dates = historical.map(item => item.date);
    const data = historical.map(item => [item.open, item.close, item.low, item.high]);
    const volumes = historical.map(item => item.volume);
    
    const option = {
        grid: [
            { left: '10%', right: '8%', top: '10%', height: '50%' },
            { left: '10%', right: '8%', top: '70%', height: '15%' }
        ],
        xAxis: [
            { type: 'category', data: dates, gridIndex: 0, show: false },
            { type: 'category', data: dates, gridIndex: 1 }
        ],
        yAxis: [
            { scale: true, gridIndex: 0, splitLine: { show: false } },
            { scale: true, gridIndex: 1, splitLine: { show: false } }
        ],
        series: [
            {
                type: 'candlestick',
                data: data,
                xAxisIndex: 0,
                yAxisIndex: 0,
                itemStyle: {
                    color: '#ef4444',
                    color0: '#10b981',
                    borderColor: '#ef4444',
                    borderColor0: '#10b981'
                }
            },
            {
                type: 'bar',
                data: volumes,
                xAxisIndex: 1,
                yAxisIndex: 1,
                itemStyle: {
                    color: function(params) {
                        const index = params.dataIndex;
                        if (index === 0) return '#999';
                        return data[index][1] >= data[index][0] ? '#ef4444' : '#10b981';
                    }
                }
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'cross' }
        }
    };
    
    chart.setOption(option);
    
    // 响应式
    window.addEventListener('resize', () => chart.resize());
}

// 初始化页面
async function init() {
    const data = await loadData();
    
    if (!data) {
        document.getElementById('etfContainer').innerHTML = `
            <div class="col-span-2 card p-8 text-center">
                <div class="text-6xl mb-4">📊</div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">暂无数据</h3>
                <p class="text-gray-600 mb-4">请等待系统自动更新数据，或手动触发GitHub Actions</p>
                <a href="https://github.com" target="_blank" 
                   class="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition">
                    前往GitHub
                </a>
            </div>
        `;
        return;
    }
    
    const { strategy, etfData } = data;
    
    // 更新时间
    const updateTime = new Date(strategy.updated_at);
    document.getElementById('updateTime').textContent = 
        updateTime.toLocaleString('zh-CN', { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit',
            hour: '2-digit', 
            minute: '2-digit' 
        });
    
    // 更新市场概览
    document.getElementById('buyCount').textContent = strategy.summary.buy_count;
    document.getElementById('holdCount').textContent = strategy.summary.hold_count;
    document.getElementById('sellCount').textContent = strategy.summary.sell_count;
    
    // 渲染ETF卡片
    const container = document.getElementById('etfContainer');
    container.innerHTML = '';
    
    const charts = [];
    
    strategy.analysis.forEach(analysis => {
        const { card, chartId, historical } = renderETFCard(analysis, etfData);
        container.appendChild(card);
        charts.push({ chartId, historical });
    });
    
    // 渲染图表（延迟以确保DOM已渲染）
    setTimeout(() => {
        charts.forEach(({ chartId, historical }) => {
            renderChart(chartId, historical);
        });
    }, 100);
    
    // 显示AI分析
    if (strategy.ai_analysis) {
        document.getElementById('aiAnalysisSection').style.display = 'block';
        document.getElementById('aiAnalysisContent').textContent = strategy.ai_analysis;
    }
    
    console.log('✅ 页面渲染完成');
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
