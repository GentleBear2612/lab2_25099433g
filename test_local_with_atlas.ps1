# 本地测试脚本（使用 MongoDB Atlas）
# 使用方法: .\test_local_with_atlas.ps1

Write-Host "启动本地服务器（连接 MongoDB Atlas）..." -ForegroundColor Green

# 检查 .env 文件是否存在
if (-not (Test-Path .env)) {
    Write-Host "错误：.env 文件不存在！" -ForegroundColor Red
    Write-Host "请先创建 .env 文件，参考 .env.example" -ForegroundColor Yellow
    exit 1
}

# 加载环境变量
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "env:$name" -Value $value
        Write-Host "已加载环境变量: $name" -ForegroundColor Cyan
    }
}

# 检查必要的环境变量
if (-not $env:MONGODB_URI) {
    Write-Host "错误：未设置 MONGODB_URI 环境变量！" -ForegroundColor Red
    exit 1
}

if (-not $env:GITHUB_TOKEN) {
    Write-Host "警告：未设置 GITHUB_TOKEN 环境变量，翻译功能可能无法使用" -ForegroundColor Yellow
}

Write-Host "`n正在启动 Flask 应用..." -ForegroundColor Green
Write-Host "MongoDB URI: $($env:MONGODB_URI.Substring(0, 40))..." -ForegroundColor Cyan
Write-Host "访问地址: http://localhost:5001" -ForegroundColor Green
Write-Host "`n按 Ctrl+C 停止服务器`n" -ForegroundColor Yellow

# 运行 Flask 应用
python src/main.py
