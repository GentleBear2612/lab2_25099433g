# 🎯 Vercel 部署准备情况检查
# 快速检查是否准备好部署到 Vercel

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        Vercel 部署准备情况检查                              ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""

$ready = $true
$warnings = @()

# 检查 1: 必要文件
Write-Host "📁 检查必要文件..." -ForegroundColor Yellow
$files = @{
    "vercel.json" = "Vercel 配置文件"
    "api\index.py" = "API 入口文件"
    "requirements.txt" = "Python 依赖"
    "src\main.py" = "Flask 应用"
    ".env" = "环境变量文件"
}

foreach ($file in $files.Keys) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file 缺失" -ForegroundColor Red
        $ready = $false
    }
}

# 检查 2: 环境变量
Write-Host "`n🔐 检查环境变量..." -ForegroundColor Yellow
if (Test-Path .env) {
    $envContent = Get-Content .env -Raw
    
    # 检查 MONGODB_URI
    if ($envContent -match 'MONGODB_URI=mongodb\+srv://[^@]+@[^/]+') {
        Write-Host "  ✓ MONGODB_URI 已配置" -ForegroundColor Green
    } else {
        Write-Host "  ✗ MONGODB_URI 未正确配置" -ForegroundColor Red
        $ready = $false
    }
    
    # 检查 MONGO_DB_NAME
    if ($envContent -match 'MONGO_DB_NAME=\w+') {
        Write-Host "  ✓ MONGO_DB_NAME 已配置" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ MONGO_DB_NAME 未配置 (将使用默认值)" -ForegroundColor Yellow
        $warnings += "MONGO_DB_NAME 未配置"
    }
    
    # 检查 GITHUB_TOKEN
    if ($envContent -match 'GITHUB_TOKEN=\w+' -and $envContent -notmatch 'GITHUB_TOKEN=your_github_token_here') {
        Write-Host "  ✓ GITHUB_TOKEN 已配置" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ GITHUB_TOKEN 未配置 (翻译功能将不可用)" -ForegroundColor Yellow
        $warnings += "GITHUB_TOKEN 未配置，翻译功能将不可用"
    }
}

# 检查 3: Python 环境
Write-Host "`n🐍 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.") {
        Write-Host "  ✓ Python 版本: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Python 版本过低: $pythonVersion" -ForegroundColor Yellow
        $warnings += "建议使用 Python 3.8+"
    }
} catch {
    Write-Host "  ✗ Python 未安装" -ForegroundColor Red
    $ready = $false
}

# 检查 4: 关键 Python 包
Write-Host "`n📦 检查关键依赖..." -ForegroundColor Yellow
$packages = @("flask", "pymongo", "openai", "flask_cors")
$missingPackages = @()

foreach ($pkg in $packages) {
    $check = python -c "import $pkg" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $pkg" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $pkg 未安装" -ForegroundColor Red
        $missingPackages += $pkg
        $ready = $false
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "`n  运行以下命令安装缺失的包：" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Cyan
}

# 检查 5: MongoDB 连接（可选但推荐）
Write-Host "`n🔌 测试 MongoDB 连接..." -ForegroundColor Yellow
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            Set-Item -Path "env:$($matches[1])" -Value $matches[2] -ErrorAction SilentlyContinue
        }
    }
    
    $mongoTest = python -c @"
import os
from pymongo import MongoClient
try:
    uri = os.environ.get('MONGODB_URI')
    if uri:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print('OK')
    else:
        print('NO_URI')
except Exception as e:
    print(f'ERROR:{e}')
"@ 2>&1

    if ($mongoTest -eq 'OK') {
        Write-Host "  ✓ MongoDB Atlas 连接成功" -ForegroundColor Green
    } elseif ($mongoTest -eq 'NO_URI') {
        Write-Host "  ⚠ MONGODB_URI 未设置" -ForegroundColor Yellow
    } else {
        Write-Host "  ⚠ MongoDB 连接测试失败" -ForegroundColor Yellow
        Write-Host "    运行 .\test_mongodb_connection.ps1 查看详情" -ForegroundColor Cyan
        $warnings += "MongoDB 连接测试失败，但可以继续部署"
    }
}

# 检查 6: Vercel CLI（可选）
Write-Host "`n🚀 检查 Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "  ✓ Vercel CLI 已安装: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Vercel CLI 未安装" -ForegroundColor Yellow
    Write-Host "    运行: npm install -g vercel" -ForegroundColor Cyan
    $warnings += "Vercel CLI 未安装，建议安装后再部署"
}

# 总结
Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "📊 检查结果" -ForegroundColor Cyan -NoNewline
Write-Host (" "*20) -NoNewline
Write-Host ("="*60) -ForegroundColor Cyan

if ($ready -and $warnings.Count -eq 0) {
    Write-Host "`n✅ 完美！您已准备好部署到 Vercel！" -ForegroundColor Green
    Write-Host "`n下一步：" -ForegroundColor Cyan
    Write-Host "  1. 运行部署脚本：" -ForegroundColor White
    Write-Host "     .\deploy_to_vercel.ps1" -ForegroundColor Yellow
    Write-Host "`n  2. 配置 Vercel 环境变量：" -ForegroundColor White
    Write-Host "     - MONGODB_URI" -ForegroundColor Yellow
    Write-Host "     - MONGO_DB_NAME" -ForegroundColor Yellow
    Write-Host "     - GITHUB_TOKEN" -ForegroundColor Yellow
    Write-Host "`n  3. 验证部署：" -ForegroundColor White
    Write-Host "     .\test_vercel_deployment.ps1 <your-vercel-url>" -ForegroundColor Yellow
    
} elseif ($ready -and $warnings.Count -gt 0) {
    Write-Host "`n⚠️  可以部署，但有警告：" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "   • $warning" -ForegroundColor Yellow
    }
    Write-Host "`n您仍然可以继续部署，但建议先解决这些警告。" -ForegroundColor Cyan
    Write-Host "`n继续部署：" -ForegroundColor White
    Write-Host "  .\deploy_to_vercel.ps1" -ForegroundColor Yellow
    
} else {
    Write-Host "`n❌ 还未准备好部署" -ForegroundColor Red
    Write-Host "`n请先解决以上标记为 ✗ 的问题。" -ForegroundColor Yellow
    Write-Host "`n常见解决方法：" -ForegroundColor Cyan
    Write-Host "  • 安装 Python 依赖：" -ForegroundColor White
    Write-Host "    pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "`n  • 配置环境变量：" -ForegroundColor White
    Write-Host "    复制 .env.example 为 .env 并填写配置" -ForegroundColor Yellow
    Write-Host "`n  • 运行完整测试：" -ForegroundColor White
    Write-Host "    .\run_all_tests.ps1" -ForegroundColor Yellow
}

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "`n💡 提示：查看完整文档" -ForegroundColor Cyan
Write-Host "   • 快速开始: QUICK_START.md" -ForegroundColor White
Write-Host "   • 完整指南: VERCEL_DEPLOYMENT.md" -ForegroundColor White
Write-Host "   • 故障排查: TROUBLESHOOTING.md" -ForegroundColor White
Write-Host "   • 文档索引: DOCUMENTATION_INDEX.md" -ForegroundColor White
Write-Host ""
