# 检查 Vercel 部署日志
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Vercel 部署日志检查工具" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan

Write-Host "`n请按照以下步骤查看详细错误信息：`n" -ForegroundColor Green

Write-Host "1. 访问 Vercel Dashboard:" -ForegroundColor Yellow
Write-Host "   https://vercel.com/dashboard`n"

Write-Host "2. 选择你的项目，然后点击 'Deployments'`n" -ForegroundColor Yellow

Write-Host "3. 点击最新的部署（顶部的那个）`n" -ForegroundColor Yellow

Write-Host "4. 查看以下信息：" -ForegroundColor Yellow
Write-Host "   a) 'Building' 标签 - 查看构建日志" -ForegroundColor Cyan
Write-Host "   b) 'Functions' 标签 - 查看函数日志" -ForegroundColor Cyan
Write-Host "   c) 点击 'View Function Logs' 查看运行时错误`n" -ForegroundColor Cyan

Write-Host "5. 常见错误类型：" -ForegroundColor Yellow
Write-Host "   - ModuleNotFoundError: 缺少依赖包" -ForegroundColor Red
Write-Host "   - ImportError: 导入路径错误" -ForegroundColor Red
Write-Host "   - ValueError: 环境变量未设置" -ForegroundColor Red
Write-Host "   - pymongo.errors: MongoDB 连接失败`n" -ForegroundColor Red

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "需要查看的关键信息：" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "1. Build Output (构建输出)" -ForegroundColor Yellow
Write-Host "2. Function Logs (函数日志 - 最重要)" -ForegroundColor Yellow
Write-Host "3. Environment Variables (环境变量)" -ForegroundColor Yellow
Write-Host "`n将日志中的错误信息复制出来，我可以帮你分析！`n" -ForegroundColor Green
