# MongoDB Atlas 连接测试脚本
# 使用方法: .\test_mongodb_connection.ps1

Write-Host "测试 MongoDB Atlas 连接..." -ForegroundColor Green

# 加载环境变量
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $name = $matches[1]
            $value = $matches[2]
            Set-Item -Path "env:$name" -Value $value
        }
    }
    Write-Host "已加载 .env 文件" -ForegroundColor Cyan
} else {
    Write-Host "警告：.env 文件不存在" -ForegroundColor Yellow
}

# 检查 MONGODB_URI
if (-not $env:MONGODB_URI) {
    Write-Host "错误：未设置 MONGODB_URI 环境变量！" -ForegroundColor Red
    Write-Host "请在 .env 文件中设置 MONGODB_URI" -ForegroundColor Yellow
    exit 1
}

Write-Host "MongoDB URI: $($env:MONGODB_URI.Substring(0, 40))..." -ForegroundColor Cyan
Write-Host "正在测试连接..." -ForegroundColor Yellow

# 使用 Python 测试连接
python -c @"
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

try:
    # 获取连接信息
    uri = os.environ.get('MONGODB_URI')
    db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
    
    print(f'正在连接到数据库: {db_name}')
    
    # 创建客户端并测试连接
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # 尝试获取服务器信息
    client.admin.command('ping')
    
    # 获取数据库
    db = client[db_name]
    
    # 列出集合
    collections = db.list_collection_names()
    print(f'\n✓ 连接成功！')
    print(f'数据库名称: {db_name}')
    print(f'集合列表: {collections if collections else "（无集合）"}')
    
    # 测试插入和读取
    test_collection = db.test_connection
    test_doc = {'test': 'connection', 'timestamp': '2025-10-09'}
    result = test_collection.insert_one(test_doc)
    print(f'\n✓ 测试写入成功！插入 ID: {result.inserted_id}')
    
    # 读取测试文档
    found_doc = test_collection.find_one({'_id': result.inserted_id})
    print(f'✓ 测试读取成功！文档: {found_doc}')
    
    # 删除测试文档
    test_collection.delete_one({'_id': result.inserted_id})
    print(f'✓ 测试清理成功！')
    
    # 检查 notes 集合
    notes_count = db.notes.count_documents({})
    print(f'\n当前笔记数量: {notes_count}')
    
    client.close()
    print(f'\n✓ MongoDB Atlas 连接测试完成！')
    
except ConnectionFailure as e:
    print(f'\n✗ 连接失败: {e}')
    print('请检查：')
    print('1. MongoDB Atlas 网络访问设置（允许 0.0.0.0/0）')
    print('2. 用户名和密码是否正确')
    print('3. 集群是否在运行')
    exit(1)
    
except ServerSelectionTimeoutError as e:
    print(f'\n✗ 服务器选择超时: {e}')
    print('请检查网络连接和 MongoDB Atlas 状态')
    exit(1)
    
except Exception as e:
    print(f'\n✗ 发生错误: {e}')
    exit(1)
"@

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ 所有测试通过！可以继续部署到 Vercel" -ForegroundColor Green
} else {
    Write-Host "`n✗ 测试失败，请检查配置" -ForegroundColor Red
}
