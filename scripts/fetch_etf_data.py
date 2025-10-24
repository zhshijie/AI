#!/usr/bin/env python3
"""
ETF数据爬取脚本
爬取机器人ETF(159770)和信创ETF(515860)的实时数据
"""

import requests
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time

def fetch_etf_realtime_data(etf_code):
    """
    获取ETF实时行情数据
    使用新浪财经API
    """
    try:
        # 新浪财经API
        if etf_code.startswith('1'):
            # 深圳ETF
            api_url = f'https://hq.sinajs.cn/list=sz{etf_code}'
        else:
            # 上海ETF
            api_url = f'https://hq.sinajs.cn/list=sh{etf_code}'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://finance.sina.com.cn/'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        response.encoding = 'gbk'
        
        if response.status_code == 200:
            data_str = response.text.split('="')[1].split('";')[0]
            data_parts = data_str.split(',')
            
            if len(data_parts) > 30:
                return {
                    'code': etf_code,
                    'name': data_parts[0],
                    'open': float(data_parts[1]) if data_parts[1] else 0,
                    'pre_close': float(data_parts[2]) if data_parts[2] else 0,
                    'current': float(data_parts[3]) if data_parts[3] else 0,
                    'high': float(data_parts[4]) if data_parts[4] else 0,
                    'low': float(data_parts[5]) if data_parts[5] else 0,
                    'volume': int(data_parts[8]) if data_parts[8] else 0,
                    'amount': float(data_parts[9]) if data_parts[9] else 0,
                    'date': data_parts[30],
                    'time': data_parts[31],
                    'change': round(float(data_parts[3]) - float(data_parts[2]), 4) if data_parts[3] and data_parts[2] else 0,
                    'change_percent': round((float(data_parts[3]) - float(data_parts[2])) / float(data_parts[2]) * 100, 2) if data_parts[2] and float(data_parts[2]) > 0 else 0
                }
    except Exception as e:
        print(f"获取{etf_code}实时数据失败: {e}")
    
    return None

def fetch_etf_historical_data(etf_code, days=30):
    """
    获取ETF历史数据
    使用东方财富API
    """
    try:
        # 东方财富历史数据API
        market = '0' if etf_code.startswith('1') else '1'
        api_url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        
        params = {
            'secid': f'{market}.{etf_code}',
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',  # 日K线
            'fqt': '1',    # 前复权
            'end': '20500101',
            'lmt': days
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://quote.eastmoney.com/'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and data['data'].get('klines'):
                klines = data['data']['klines']
                historical_data = []
                
                for kline in klines:
                    parts = kline.split(',')
                    historical_data.append({
                        'date': parts[0],
                        'open': float(parts[1]),
                        'close': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'volume': int(parts[5]),
                        'amount': float(parts[6]),
                        'change_percent': float(parts[8])
                    })
                
                return historical_data
    except Exception as e:
        print(f"获取{etf_code}历史数据失败: {e}")
    
    return []

def fetch_etf_news(etf_name, limit=10):
    """
    获取ETF相关新闻
    """
    try:
        # 使用百度新闻搜索
        search_url = f'https://www.baidu.com/s?tn=news&word={etf_name}'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []
            
            # 解析新闻结果
            results = soup.find_all('div', class_='result')[:limit]
            
            for result in results:
                try:
                    title_elem = result.find('h3')
                    if title_elem:
                        title = title_elem.get_text().strip()
                        link_elem = title_elem.find('a')
                        link = link_elem.get('href') if link_elem else ''
                        
                        desc_elem = result.find('div', class_='c-abstract')
                        description = desc_elem.get_text().strip() if desc_elem else ''
                        
                        time_elem = result.find('span', class_='c-color-gray2')
                        pub_time = time_elem.get_text().strip() if time_elem else ''
                        
                        news_items.append({
                            'title': title,
                            'description': description,
                            'url': link,
                            'published_at': pub_time,
                            'source': '百度新闻'
                        })
                except Exception as e:
                    continue
            
            return news_items
    except Exception as e:
        print(f"获取{etf_name}新闻失败: {e}")
    
    return []

def calculate_technical_indicators(historical_data):
    """
    计算技术指标
    """
    if not historical_data or len(historical_data) < 20:
        return {}
    
    closes = [item['close'] for item in historical_data]
    volumes = [item['volume'] for item in historical_data]
    
    # MA5, MA10, MA20
    ma5 = sum(closes[-5:]) / 5 if len(closes) >= 5 else closes[-1]
    ma10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else closes[-1]
    ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else closes[-1]
    
    # RSI (14日)
    rsi = calculate_rsi(closes, 14)
    
    # MACD
    macd_data = calculate_macd(closes)
    
    # 布林带
    bollinger = calculate_bollinger_bands(closes, 20)
    
    # 成交量变化
    volume_change = ((volumes[-1] - volumes[-2]) / volumes[-2] * 100) if len(volumes) >= 2 and volumes[-2] > 0 else 0
    
    return {
        'ma5': round(ma5, 3),
        'ma10': round(ma10, 3),
        'ma20': round(ma20, 3),
        'rsi': round(rsi, 2),
        'macd': macd_data,
        'bollinger': bollinger,
        'volume_change': round(volume_change, 2)
    }

def calculate_rsi(prices, period=14):
    """计算RSI指标"""
    if len(prices) < period + 1:
        return 50
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    if len(prices) < slow:
        return {'dif': 0, 'dea': 0, 'macd': 0}
    
    # 计算EMA
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    dif = ema_fast - ema_slow
    
    # 简化DEA计算
    dea = dif * 0.8
    macd = (dif - dea) * 2
    
    return {
        'dif': round(dif, 4),
        'dea': round(dea, 4),
        'macd': round(macd, 4)
    }

def calculate_ema(prices, period):
    """计算EMA"""
    if len(prices) < period:
        return prices[-1]
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """计算布林带"""
    if len(prices) < period:
        return {'upper': 0, 'middle': 0, 'lower': 0}
    
    recent_prices = prices[-period:]
    middle = sum(recent_prices) / period
    
    variance = sum((p - middle) ** 2 for p in recent_prices) / period
    std = variance ** 0.5
    
    upper = middle + (std_dev * std)
    lower = middle - (std_dev * std)
    
    return {
        'upper': round(upper, 3),
        'middle': round(middle, 3),
        'lower': round(lower, 3)
    }

def main():
    print("=" * 60)
    print("ETF数据爬取任务")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # ETF配置
    etfs = [
        {'code': '159770', 'name': '机器人ETF', 'full_name': '国泰中证机器人ETF'},
        {'code': '515860', 'name': '信创ETF', 'full_name': '华夏中证信创ETF'}
    ]
    
    all_etf_data = []
    
    for etf in etfs:
        print(f"
正在获取 {etf['name']}({etf['code']}) 数据...")
        
        # 获取实时数据
        realtime_data = fetch_etf_realtime_data(etf['code'])
        if not realtime_data:
            print(f"  ❌ 获取实时数据失败")
            continue
        
        print(f"  ✓ 实时数据: 当前价 {realtime_data['current']}, 涨跌幅 {realtime_data['change_percent']}%")
        
        # 获取历史数据
        time.sleep(1)  # 避免请求过快
        historical_data = fetch_etf_historical_data(etf['code'], 30)
        print(f"  ✓ 历史数据: {len(historical_data)} 条")
        
        # 计算技术指标
        indicators = calculate_technical_indicators(historical_data)
        print(f"  ✓ 技术指标: RSI={indicators.get('rsi', 0)}, MA5={indicators.get('ma5', 0)}")
        
        # 获取相关新闻
        time.sleep(1)
        news = fetch_etf_news(etf['name'], 10)
        print(f"  ✓ 相关新闻: {len(news)} 条")
        
        # 汇总数据
        etf_data = {
            'code': etf['code'],
            'name': etf['name'],
            'full_name': etf['full_name'],
            'realtime': realtime_data,
            'historical': historical_data[-10:],  # 只保留最近10天
            'indicators': indicators,
            'news': news,
            'updated_at': datetime.now().isoformat()
        }
        
        all_etf_data.append(etf_data)
    
    # 保存数据
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'etf_data.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': datetime.now().isoformat(),
            'etfs': all_etf_data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"
✅ 数据已保存到 {output_file}")
    print(f"   共获取 {len(all_etf_data)} 只ETF数据")
    print("=" * 60)

if __name__ == '__main__':
    main()

