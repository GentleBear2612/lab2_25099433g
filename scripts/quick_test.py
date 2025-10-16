import requests

base_url = "https://lab2-25099433g-o7aptrrm8-gentlebears-projects-c14ff97f.vercel.app"

print("=" * 70)
print("测试 Vercel 部署的各个端点")
print("=" * 70)

# 测试 1: /api/test (纯 Python)
print("\n[1/4] 测试 /api/test (纯 Python - BaseHTTPRequestHandler)")
try:
    r = requests.get(f"{base_url}/api/test", timeout=10)
    print(f"  状态: {r.status_code}")
    print(f"  响应: {r.text[:200]}")
    if r.status_code == 200:
        print("  ✓ 成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")

# 测试 2: /api/health
print("\n[2/4] 测试 /api/health")
try:
    r = requests.get(f"{base_url}/api/health", timeout=10)
    print(f"  状态: {r.status_code}")
    print(f"  响应: {r.text[:200]}")
    if r.status_code == 200:
        print("  ✓ 成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")

# 测试 3: /api/simple
print("\n[3/4] 测试 /api/simple")
try:
    r = requests.get(f"{base_url}/api/simple", timeout=10)
    print(f"  状态: {r.status_code}")
    print(f"  响应: {r.text[:200]}")
    if r.status_code == 200:
        print("  ✓ 成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")

# 测试 4: /api/notes
print("\n[4/4] 测试 /api/notes")
try:
    r = requests.get(f"{base_url}/api/notes", timeout=10)
    print(f"  状态: {r.status_code}")
    print(f"  响应: {r.text[:200]}")
    if r.status_code == 200:
        print("  ✓ 成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
