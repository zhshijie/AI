from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)
        
        # 设置CORS头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            if path == '/api/news/latest':
                response = self.get_latest_news(query)
            elif path == '/api/news/categories':
                response = self.get_categories()
            elif path == '/api/temperature/latest':
                response = self.get_latest_temperature()
            elif path == '/api/stats/overview':
                response = self.get_stats_overview()
            elif path == '/api/tencent/news':
                response = self.get_tencent_news(query)
            elif path == '/api/tencent/analysis':
                response = self.get_tencent_analysis()
            else:
                response = {'success': False, 'error': 'Endpoint not found'}
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # POST请求直接返回最新分析结果
        try:
            response = self.get_latest_temperature()
        except Exception as e:
            response = {'success': False, 'error': str(e)}
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_latest_news(self, query):
        """获取最新新闻"""
        try:
            # 读取新闻数据
            news_data = self.load_json_file('data/news.json')
            
            if not news_data:
                return {'success': False, 'error': 'No news data available'}
            
            news_list = news_data.get('news', [])
            
            # 分类筛选
            category = query.get('category', [''])[0]
            if category:
                news_list = [n for n in news_list if n.get('category') == category]
            
            # 限制数量
            limit = int(query.get('limit', ['20'])[0])
            news_list = news_list[:limit]
            
            return {
                'success': True,
                'data': news_list,
                'count': len(news_list),
                'updated_at': news_data.get('updated_at')
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_categories(self):
        """获取新闻分类统计"""
        try:
            news_data = self.load_json_file('data/news.json')
            
            if not news_data:
                return {'success': False, 'error': 'No news data available'}
            
            news_list = news_data.get('news', [])
            
            # 统计分类
            category_count = {}
            for news in news_list:
                category = news.get('category', '其他')
                category_count[category] = category_count.get(category, 0) + 1
            
            categories = [
                {'category': cat, 'count': count}
                for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True)
            ]
            
            return {'success': True, 'data': categories}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_latest_temperature(self):
        """获取最新投资温度分析"""
        try:
            analysis_data = self.load_json_file('data/analysis.json')
            
            if not analysis_data:
                return {'success': False, 'error': 'No analysis data available'}
            
            return {'success': True, 'data': analysis_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_stats_overview(self):
        """获取统计概览"""
        try:
            news_data = self.load_json_file('data/news.json')
            analysis_data = self.load_json_file('data/analysis.json')
            
            if not news_data:
                return {'success': False, 'error': 'No data available'}
            
            news_list = news_data.get('news', [])
            
            # 统计今日新闻
            today = datetime.now().date()
            news_today = sum(
                1 for news in news_list
                if datetime.fromisoformat(news.get('published_at', '')).date() == today
            )
            
            # 分类统计
            category_count = {}
            for news in news_list:
                category = news.get('category', '其他')
                category_count[category] = category_count.get(category, 0) + 1
            
            category_stats = [
                {'category': cat, 'count': count}
                for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True)[:5]
            ]
            
            return {
                'success': True,
                'data': {
                    'news_total': len(news_list),
                    'news_today': news_today,
                    'category_stats': category_stats,
                    'latest_temperature': {
                        'temperature_score': analysis_data.get('temperature_score', 50),
                        'sentiment': analysis_data.get('sentiment', '中性')
                    } if analysis_data else None,
                    'updated_at': news_data.get('updated_at')
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_tencent_news(self, query):
        """获取腾讯相关新闻"""
        try:
            # 读取腾讯新闻数据
            news_data = self.load_json_file('data/tencent_news.json')
            
            if not news_data:
                return {'success': False, 'error': 'No Tencent news data available'}
            
            return {
                'success': True,
                'data': news_data
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_tencent_analysis(self):
        """获取腾讯投资分析"""
        try:
            analysis_data = self.load_json_file('data/tencent_analysis.json')
            
            if not analysis_data:
                return {'success': False, 'error': 'No Tencent analysis data available'}
            
            return {'success': True, 'data': analysis_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def load_json_file(self, filepath):
        """加载JSON文件"""
        try:
            # 尝试从当前目录读取
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # 尝试从上级目录读取
            parent_path = os.path.join('..', filepath)
            if os.path.exists(parent_path):
                with open(parent_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # 尝试从根目录读取
            root_path = os.path.join('/', filepath)
            if os.path.exists(root_path):
                with open(root_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
        except Exception as e:
            print(f"Error loading {filepath}: {str(e)}")
            return None
