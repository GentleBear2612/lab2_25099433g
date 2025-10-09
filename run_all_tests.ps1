# 完整测试套件
# 运行所有测试以验证配置

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   NoteTaker 部署前测试套件" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$allPassed = $true

# 测试 1: 检查必要文件
Write-Host "测试 1: 检查必要文件..." -ForegroundColor Yellow
$requiredFiles = @(
    "vercel.json",
    "api\index.py",
    ".vercelignore",
    "requirements.txt",
    "src\main.py",
    ".env"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file 不存在" -ForegroundColor Red
        $allPassed = $false
    }
}
Write-Host ""

# 测试 2: 检查 .env 文件配置
Write-Host "测试 2: 检查环境变量配置..." -ForegroundColor Yellow
if (Test-Path .env) {
    $envContent = Get-Content .env -Raw
    
    if ($envContent -match 'MONGODB_URI=.+') {
        Write-Host "  ✓ MONGODB_URI 已配置" -ForegroundColor Green
    } else {
        Write-Host "  ✗ MONGODB_URI 未配置" -ForegroundColor Red
        $allPassed = $false
    }
    
    if ($envContent -match 'MONGO_DB_NAME=.+') {
        Write-Host "  ✓ MONGO_DB_NAME 已配置" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ MONGO_DB_NAME 未配置（将使用默认值）" -ForegroundColor Yellow
    }
    
    if ($envContent -match 'GITHUB_TOKEN=.+' -and $envContent -notmatch 'GITHUB_TOKEN=your_github_token_here') {
        Write-Host "  ✓ GITHUB_TOKEN 已配置" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ GITHUB_TOKEN 未配置（翻译功能将不可用）" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✗ .env 文件不存在" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# 测试 3: 检查 Python 依赖
Write-Host "测试 3: 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python 未安装" -ForegroundColor Red
    $allPassed = $false
}

# 检查关键包
$packages = @("flask", "pymongo", "openai")
foreach ($pkg in $packages) {
    $installed = python -c "import $pkg; print('OK')" 2>&1
    if ($installed -match "OK") {
        Write-Host "  ✓ $pkg 已安装" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $pkg 未安装 - 运行: pip install -r requirements.txt" -ForegroundColor Red
        $allPassed = $false
    }
}
Write-Host ""

# 测试 4: MongoDB 连接测试
Write-Host "测试 4: MongoDB 连接测试..." -ForegroundColor Yellow
Write-Host "  运行连接测试脚本..." -ForegroundColor Cyan

# 加载环境变量
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            Set-Item -Path "env:$($matches[1])" -Value $matches[2] -ErrorAction SilentlyContinue
        }
    }
}

# 运行 MongoDB 测试
$mongoTest = python -c @"
import os
from pymongo import MongoClient
try:
    uri = os.environ.get('MONGODB_URI')
    if not uri:
        print('ERROR: MONGODB_URI not set')
        exit(1)
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('OK')
    exit(0)
except Exception as e:
    print(f'ERROR: {e}')
    exit(1)
"@ 2>&1

if ($mongoTest -match "OK") {
    Write-Host "  ✓ MongoDB Atlas 连接成功" -ForegroundColor Green
} else {
    Write-Host "  ✗ MongoDB 连接失败: $mongoTest" -ForegroundColor Red
    Write-Host "    运行 .\test_mongodb_connection.ps1 查看详细信息" -ForegroundColor Yellow
    $allPassed = $false
}
Write-Host ""

# 测试 5: 检查 Vercel CLI
Write-Host "测试 5: 检查 Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "  ✓ Vercel CLI: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Vercel CLI 未安装" -ForegroundColor Yellow
    Write-Host "    运行: npm install -g vercel" -ForegroundColor Cyan
}
Write-Host ""

# 总结
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   测试结果" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

if ($allPassed) {
    Write-Host "✓ 所有测试通过！" -ForegroundColor Green
    Write-Host ""
    Write-Host "您可以继续部署了：" -ForegroundColor Green
    Write-Host "  1. 运行: .\deploy_to_vercel.ps1" -ForegroundColor Cyan
    Write-Host "  2. 或查看: QUICK_START.md" -ForegroundColor Cyan
} else {
    Write-Host "✗ 部分测试失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先解决以上问题，然后重新运行此测试" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "常见解决方法：" -ForegroundColor Yellow
    Write-Host "  - 安装依赖: pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host "  - 检查 .env 文件配置" -ForegroundColor Cyan
    Write-Host "  - 运行详细的 MongoDB 测试: .\test_mongodb_connection.ps1" -ForegroundColor Cyan
}

Write-Host ""
