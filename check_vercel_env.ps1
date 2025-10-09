# Vercel 环境变量检查脚本
# 使用方法: .\check_vercel_env.ps1

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        Vercel 环境变量检查                                  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""

# 检查 Vercel CLI
Write-Host "🔍 检查 Vercel CLI..." -ForegroundColor Yellow
if (Get-Command vercel -ErrorAction SilentlyContinue) {
    $version = vercel --version 2>&1
    Write-Host "  ✓ Vercel CLI 已安装: $version" -ForegroundColor Green
    
    Write-Host "`n📋 当前 Vercel 环境变量：" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        vercel env ls
        
        Write-Host "`n⚠️  请确认以上列表包含：" -ForegroundColor Yellow
        Write-Host "   • MONGODB_URI" -ForegroundColor White
        Write-Host "   • MONGO_DB_NAME" -ForegroundColor White
        Write-Host "   • GITHUB_TOKEN (可选)" -ForegroundColor White
        
        Write-Host "`n如果缺少，立即添加：" -ForegroundColor Cyan
        Write-Host "   vercel env add MONGODB_URI production" -ForegroundColor Yellow
        Write-Host "   vercel env add MONGO_DB_NAME production" -ForegroundColor Yellow
        Write-Host "   vercel env add GITHUB_TOKEN production" -ForegroundColor Yellow
        
    } catch {
        Write-Host "  ⚠️  无法获取环境变量列表" -ForegroundColor Yellow
        Write-Host "     可能需要先登录: vercel login" -ForegroundColor Cyan
    }
    
} else {
    Write-Host "  ✗ Vercel CLI 未安装" -ForegroundColor Red
    Write-Host "`n请先安装 Vercel CLI：" -ForegroundColor Yellow
    Write-Host "   npm install -g vercel" -ForegroundColor Cyan
    Write-Host "`n然后重新运行此脚本" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n" + ("="*60) -ForegroundColor Cyan
Write-Host "💡 修复 500 错误的步骤：" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 确保上面列出了所有需要的环境变量" -ForegroundColor White
Write-Host "2. 如果缺少，使用 'vercel env add' 添加" -ForegroundColor White
Write-Host "3. 重新部署：vercel --prod" -ForegroundColor White
Write-Host "4. 测试：访问 https://your-project.vercel.app/api/notes" -ForegroundColor White
Write-Host ""
Write-Host "📖 详细说明：查看 FIX_500_ERROR.md" -ForegroundColor Cyan
Write-Host ""
