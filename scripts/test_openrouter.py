#!/usr/bin/env python3
"""
OpenRouter API 连接测试脚本
用于诊断和修复 404 错误
"""

import requests
import os
import json
import sys

def test_openrouter_api():
    """测试 OpenRouter API 连接"""
    
    print("=" * 60)
    print("OpenRouter API 连接测试")
    print("=" * 60)
    print()
    
    # 步骤 1: 检查 API 密钥
    print("[1/5] 检查 API 密钥...")
    api_key = "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"
    
    if not api_key:
        print("❌ 未设置 OPENROUTER_API_KEY 环境变量")
        print()
        print("请设置环境变量：")
        print("  Linux/Mac: export OPENROUTER_API_KEY='your-key'")
        print("  Windows:   set OPENROUTER_API_KEY=your-key")
        print()
        print("获取 API 密钥：https://openrouter.ai/keys")
        return False
    
    # 验证密钥格式
    if not api_key.startswith('sk-or-v1-'):
        print(f"⚠️  警告: API 密钥格式可能不正确")
        print(f"   当前格式: {api_key[:10]}...")
        print(f"   正确格式应以 'sk-or-v1-' 开头")
        print()
    else:
        print(f"✓ API 密钥格式正确: {api_key[:20]}...")
        print()
    
    # 步骤 2: 准备请求
    print("[2/5] 准备 API 请求...")
    
    api_url = 'https://openrouter.ai/api/v1/chat/completions'
    model = 'deepseek/deepseek-r1:free'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://github.com',
        'X-Title': 'OpenRouter Connection Test'
    }
    
    payload = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': 'Say "Hello, OpenRouter is working!" in one sentence.'
            }
        ],
        'max_tokens': 50
    }
    
    print(f"  API URL: {api_url}")
    print(f"  Model: {model}")
    print(f"  Headers: {list(headers.keys())}")
    print()
    
    # 步骤 3: 发送请求
    print("[3/5] 发送 API 请求...")
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"  状态码: {response.status_code}")
        print()
        
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("   可能的原因：")
        print("   1. 网络连接问题")
        print("   2. OpenRouter 服务响应慢")
        print("   建议：稍后重试")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        print("   可能的原因：")
        print("   1. 无法访问 openrouter.ai")
        print("   2. 网络防火墙阻止")
        print("   3. DNS 解析失败")
        print("   建议：检查网络连接")
        return False
        
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False
    
    # 步骤 4: 分析响应
    print("[4/5] 分析响应...")
    
    if response.status_code == 200:
        print("✅ 请求成功！")
        print()
        
        try:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"  AI 响应: {content}")
            print()
            
            # 显示使用情况
            if 'usage' in result:
                usage = result['usage']
                print(f"  Token 使用:")
                print(f"    - Prompt: {usage.get('prompt_tokens', 0)}")
                print(f"    - Completion: {usage.get('completion_tokens', 0)}")
                print(f"    - Total: {usage.get('total_tokens', 0)}")
                print()
            
            return True
            
        except Exception as e:
            print(f"⚠️  响应解析失败: {str(e)}")
            print(f"  原始响应: {response.text[:200]}")
            return False
    
    elif response.status_code == 400:
        print("❌ 请求参数错误 (400)")
        print()
        print("  可能的原因：")
        print("  1. 模型名称错误")
        print("  2. 请求格式不正确")
        print("  3. 参数缺失或无效")
        print()
        print(f"  错误详情: {response.text[:300]}")
        return False
    
    elif response.status_code == 401:
        print("❌ 认证失败 (401)")
        print()
        print("  可能的原因：")
        print("  1. API 密钥无效或过期")
        print("  2. API 密钥格式错误")
        print()
        print("  解决方案：")
        print("  1. 访问 https://openrouter.ai/keys")
        print("  2. 删除旧密钥并创建新密钥")
        print("  3. 更新环境变量")
        print()
        print(f"  错误详情: {response.text[:300]}")
        return False
    
    elif response.status_code == 403:
        print("❌ 权限不足 (403)")
        print()
        print("  可能的原因：")
        print("  1. API 密钥权限不足")
        print("  2. 账户被限制")
        print()
        print(f"  错误详情: {response.text[:300]}")
        return False
    
    elif response.status_code == 404:
        print("❌ 端点不存在 (404)")
        print()
        print("  可能的原因：")
        print("  1. API URL 错误")
        print("  2. 模型名称错误或不存在")
        print("  3. 免费模型需要 ':free' 后缀")
        print()
        print("  当前配置：")
        print(f"    URL: {api_url}")
        print(f"    Model: {model}")
        print()
        print("  正确的免费模型示例：")
        print("    - meta-llama/llama-3.1-8b-instruct:free")
        print("    - google/gemini-flash-1.5:free")
        print("    - mistralai/mistral-7b-instruct:free")
        print()
        print(f"  错误详情: {response.text[:300]}")
        return False
    
    elif response.status_code == 429:
        print("❌ 请求过多 (429)")
        print()
        print("  可能的原因：")
        print("  1. 超过免费配额")
        print("  2. 请求频率过高")
        print()
        print("  解决方案：")
        print("  1. 等待一段时间后重试")
        print("  2. 检查 https://openrouter.ai/activity")
        print("  3. 考虑升级账户")
        print()
        print(f"  错误详情: {response.text[:300]}")
        return False
    
    elif response.status_code >= 500:
        print(f"❌ 服务器错误 ({response.status_code})")
        print()
        print("  OpenRouter 服务可能暂时不可用")
        print("  建议：")
        print("  1. 稍后重试")
        print("  2. 检查服务状态: https://status.openrouter.ai/")
        print("  3. 切换到其他 AI 服务（Groq、DeepSeek）")
        print()
        print(f"  错误详情: {response.text[:300]}")
        return False
    
    else:
        print(f"❌ 未知错误 ({response.status_code})")
        print(f"  响应: {response.text[:300]}")
        return False
    
    # 步骤 5: 总结
    print("[5/5] 测试总结")
    print()

def test_alternative_models():
    """测试其他可用的免费模型"""
    
    print()
    print("=" * 60)
    print("测试其他免费模型")
    print("=" * 60)
    print()
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return
    
    free_models = [
        'meta-llama/llama-3.1-8b-instruct:free',
        'google/gemini-flash-1.5:free',
        'mistralai/mistral-7b-instruct:free'
    ]
    
    for model in free_models:
        print(f"测试模型: {model}")
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com',
            'X-Title': 'Model Test'
        }
        
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': 'Hi'}],
            'max_tokens': 10
        }
        
        try:
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"  ✓ 可用")
            else:
                print(f"  ✗ 不可用 ({response.status_code})")
        except:
            print(f"  ✗ 请求失败")
        
        print()

def main():
    """主函数"""
    
    success = test_openrouter_api()
    
    if success:
        print("=" * 60)
        print("✅ OpenRouter API 连接正常！")
        print("=" * 60)
        print()
        print("下一步：")
        print("1. 运行完整测试: python scripts/test_ai_analysis.py")
        print("2. 运行新闻分析: python scripts/fetch_news.py")
        print("3. 查看文档: cat OPENROUTER_404_FIX.md")
        print()
        
        # 测试其他模型
        test_alternative_models()
        
        sys.exit(0)
    else:
        print("=" * 60)
        print("❌ OpenRouter API 连接失败")
        print("=" * 60)
        print()
        print("建议：")
        print("1. 查看详细修复指南: cat OPENROUTER_404_FIX.md")
        print("2. 切换到 Groq: export AI_PROVIDER='groq'")
        print("3. 查看故障排查: cat TROUBLESHOOTING.md")
        print()
        sys.exit(1)

if __name__ == '__main__':
    main()

