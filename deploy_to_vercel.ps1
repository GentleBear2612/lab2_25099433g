# Vercel 部署脚本
# 使用方法: .\deploy_to_vercel.ps1

Write-Host "开始部署到 Vercel..." -ForegroundColor Green

# 检查是否安装了 Vercel CLI
if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "未检测到 Vercel CLI，正在安装..." -ForegroundColor Yellow
    npm install -g vercel
}

# 检查是否已登录
Write-Host "检查 Vercel 登录状态..." -ForegroundColor Cyan
vercel whoami

if ($LASTEXITCODE -ne 0) {
    Write-Host "请先登录 Vercel..." -ForegroundColor Yellow
    vercel login
}

# 部署到生产环境
Write-Host "`n开始部署到生产环境..." -ForegroundColor Green
vercel --prod

Write-Host "`n部署完成！" -ForegroundColor Green
Write-Host "请确保已在 Vercel 项目设置中配置以下环境变量：" -ForegroundColor Yellow
Write-Host "  - MONGODB_URI" -ForegroundColor Cyan
Write-Host "  - MONGO_DB_NAME" -ForegroundColor Cyan
Write-Host "  - GITHUB_TOKEN" -ForegroundColor Cyan
Write-Host "`n查看部署日志: vercel logs" -ForegroundColor Cyan
