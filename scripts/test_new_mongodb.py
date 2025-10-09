"""
测试新的 MongoDB Atlas 连接
"""
from pymongo import MongoClient
import sys

# 你的新连接字符串
MONGODB_URI = "mongodb+srv://Vercel-Admin-atlas-cyan-village:uJaf52qezykMdP8q@atlas-cyan-village.lsdtzn5.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME = "notetaker_db"

print("=" * 60)
print("测试 MongoDB Atlas 连接")
print("=" * 60)
print(f"\n连接字符串: {MONGODB_URI[:50]}...")
print(f"数据库名称: {MONGO_DB_NAME}")

try:
    print("\n[1/4] 正在连接到 MongoDB Atlas...")
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
    
    print("[2/4] 正在验证连接...")
    client.admin.command('ping')
    print("✓ 连接成功！")
    
    print(f"\n[3/4] 正在访问数据库 '{MONGO_DB_NAME}'...")
    db = client[MONGO_DB_NAME]
    print(f"✓ 数据库访问成功！")
    
    print("\n[4/4] 正在列出集合...")
    collections = db.list_collection_names()
    print(f"✓ 找到 {len(collections)} 个集合:")
    for coll_name in collections:
        count = db[coll_name].count_documents({})
        print(f"  - {coll_name}: {count} 个文档")
    
    if not collections:
        print("  (数据库是空的，这是正常的)")
    
    # 测试插入一条数据
    print("\n[测试] 尝试插入测试数据...")
    test_coll = db.test_connection
    result = test_coll.insert_one({"test": True, "message": "Vercel deployment test"})
    print(f"✓ 测试数据插入成功，ID: {result.inserted_id}")
    
    # 删除测试数据
    test_coll.delete_one({"_id": result.inserted_id})
    print("✓ 测试数据已清理")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！MongoDB Atlas 连接正常！")
    print("=" * 60)
    sys.exit(0)
    
except Exception as e:
    print("\n" + "=" * 60)
    print(f"❌ 连接失败: {e}")
    print("=" * 60)
    print("\n可能的原因:")
    print("1. 网络访问限制 - 检查 MongoDB Atlas 的 Network Access")
    print("2. 用户名或密码错误")
    print("3. 集群名称错误")
    print("4. 网络连接问题")
    sys.exit(1)
