"""
测试 Vercel 部署的 API 端点
"""
import requests
import sys

# 提示用户输入 Vercel URL
print("=" * 70)
print("Vercel API 测试工具")
print("=" * 70)

vercel_url = input("\n请输入你的 Vercel 项目 URL (例如: https://your-project.vercel.app): ").strip()

if not vercel_url:
    print("❌ 错误: 未提供 URL")
    sys.exit(1)

# 确保 URL 不以 / 结尾
vercel_url = vercel_url.rstrip('/')

print(f"\n测试 URL: {vercel_url}")
print("=" * 70)

# 测试 1: 健康检查
print("\n[1/4] 测试健康检查端点: /api/health")
try:
    response = requests.get(f"{vercel_url}/api/health", timeout=10)
    print(f"  状态码: {response.status_code}")
    print(f"  响应: {response.text}")
    if response.status_code == 200:
        print("  ✓ 健康检查通过")
    else:
        print(f"  ✗ 健康检查失败")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

# 测试 2: 获取笔记列表
print("\n[2/4] 测试获取笔记列表: /api/notes")
try:
    response = requests.get(f"{vercel_url}/api/notes", timeout=10)
    print(f"  状态码: {response.status_code}")
    print(f"  响应: {response.text[:500]}")  # 只显示前500字符
    if response.status_code == 200:
        print("  ✓ API 正常工作")
    else:
        print(f"  ✗ API 返回错误")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

# 测试 3: 前端页面
print("\n[3/4] 测试前端页面: /")
try:
    response = requests.get(vercel_url, timeout=10)
    print(f"  状态码: {response.status_code}")
    if response.status_code == 200 and "NoteTaker" in response.text:
        print("  ✓ 前端页面加载成功")
    else:
        print(f"  ✗ 前端页面加载失败")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

# 测试 4: 创建测试笔记
print("\n[4/4] 测试创建笔记: POST /api/notes")
try:
    test_data = {
        "title": "测试笔记",
        "content": "这是一个测试笔记，用于验证 API 功能"
    }
    response = requests.post(f"{vercel_url}/api/notes", json=test_data, timeout=10)
    print(f"  状态码: {response.status_code}")
    print(f"  响应: {response.text[:500]}")
    if response.status_code == 201:
        print("  ✓ 创建笔记成功")
        # 尝试删除测试笔记
        data = response.json()
        if 'id' in data:
            note_id = data['id']
            delete_response = requests.delete(f"{vercel_url}/api/notes/{note_id}", timeout=10)
            if delete_response.status_code == 200:
                print("  ✓ 测试笔记已清理")
    else:
        print(f"  ✗ 创建笔记失败")
except Exception as e:
    print(f"  ✗ 请求失败: {e}")

print("\n" + "=" * 70)
print("测试完成！")
print("=" * 70)
