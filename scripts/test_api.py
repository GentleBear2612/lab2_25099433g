import requests

# 使用你的实际 Vercel URL
base_url = input("请输入你的 Vercel URL (例如: https://lab2-25099433g.vercel.app): ").strip().rstrip('/')

print("\n" + "=" * 70)
print("测试 NoteTaker API")
print("=" * 70)

# 测试 1: GET /api/notes (获取笔记列表)
print("\n[1/3] GET /api/notes - 获取笔记列表")
try:
    r = requests.get(f"{base_url}/api/notes", timeout=10)
    print(f"  状态: {r.status_code}")
    if r.status_code == 200:
        print(f"  ✓ 成功！")
        print(f"  响应: {r.json()}")
    else:
        print(f"  响应: {r.text[:300]}")
except Exception as e:
    print(f"  ✗ 错误: {e}")

# 测试 2: POST /api/notes (创建笔记)
print("\n[2/3] POST /api/notes - 创建笔记")
try:
    data = {
        "title": "测试笔记",
        "content": "这是通过 API 创建的测试笔记"
    }
    r = requests.post(f"{base_url}/api/notes", json=data, timeout=10)
    print(f"  状态: {r.status_code}")
    if r.status_code == 201:
        print(f"  ✓ 创建成功！")
        note = r.json()
        print(f"  笔记 ID: {note.get('id')}")
        note_id = note.get('id')
    else:
        print(f"  响应: {r.text[:300]}")
        note_id = None
except Exception as e:
    print(f"  ✗ 错误: {e}")
    note_id = None

# 测试 3: GET /api/health
print("\n[3/3] GET /api/health - 健康检查")
try:
    r = requests.get(f"{base_url}/api/health", timeout=10)
    print(f"  状态: {r.status_code}")
    if r.status_code == 200:
        print(f"  ✓ 健康检查通过")
        print(f"  响应: {r.json()}")
    else:
        print(f"  响应: {r.text[:300]}")
except Exception as e:
    print(f"  ✗ 错误: {e}")

print("\n" + "=" * 70)
print("测试完成！")
print("=" * 70)

if note_id:
    print(f"\n💡 提示: 创建了测试笔记 (ID: {note_id})")
    print(f"   你可以访问 {base_url} 查看界面")
