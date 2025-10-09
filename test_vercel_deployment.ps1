# Vercel 部署后 API 测试脚本
# 使用方法: .\test_vercel_deployment.ps1 <your-vercel-url>

param(
    [Parameter(Mandatory=$false)]
    [string]$VercelUrl = ""
)

if (-not $VercelUrl) {
    Write-Host "请提供 Vercel 部署 URL" -ForegroundColor Yellow
    Write-Host "使用方法: .\test_vercel_deployment.ps1 https://your-project.vercel.app" -ForegroundColor Cyan
    $VercelUrl = Read-Host "请输入 Vercel URL"
}

# 移除末尾的斜杠
$VercelUrl = $VercelUrl.TrimEnd('/')

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   测试 Vercel 部署" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "URL: $VercelUrl" -ForegroundColor Green
Write-Host ""

$allPassed = $true

# 测试 1: 前端页面
Write-Host "测试 1: 访问前端页面..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $VercelUrl -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ 前端页面加载成功 (200 OK)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ 状态码: $($response.StatusCode)" -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host "  ✗ 无法访问前端页面: $($_.Exception.Message)" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# 测试 2: 获取笔记列表
Write-Host "测试 2: GET /api/notes - 获取笔记列表..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$VercelUrl/api/notes" -Method GET -TimeoutSec 10
    Write-Host "  ✓ API 响应成功" -ForegroundColor Green
    Write-Host "  当前笔记数量: $($response.Count)" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 请求失败: $($_.Exception.Message)" -ForegroundColor Red
    $allPassed = $false
}
Write-Host ""

# 测试 3: 创建新笔记
Write-Host "测试 3: POST /api/notes - 创建新笔记..." -ForegroundColor Yellow
try {
    $noteData = @{
        title = "测试笔记 - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        content = "这是一个从 Vercel 部署测试脚本创建的测试笔记。"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$VercelUrl/api/notes" `
        -Method POST `
        -ContentType "application/json" `
        -Body $noteData `
        -TimeoutSec 10
    
    $testNoteId = $response.id
    Write-Host "  ✓ 笔记创建成功" -ForegroundColor Green
    Write-Host "  笔记 ID: $testNoteId" -ForegroundColor Cyan
    Write-Host "  标题: $($response.title)" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 创建失败: $($_.Exception.Message)" -ForegroundColor Red
    $allPassed = $false
    $testNoteId = $null
}
Write-Host ""

# 测试 4: 获取单个笔记
if ($testNoteId) {
    Write-Host "测试 4: GET /api/notes/{id} - 获取单个笔记..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$VercelUrl/api/notes/$testNoteId" -Method GET -TimeoutSec 10
        Write-Host "  ✓ 笔记获取成功" -ForegroundColor Green
        Write-Host "  标题: $($response.title)" -ForegroundColor Cyan
    } catch {
        Write-Host "  ✗ 获取失败: $($_.Exception.Message)" -ForegroundColor Red
        $allPassed = $false
    }
    Write-Host ""

    # 测试 5: 更新笔记
    Write-Host "测试 5: PUT /api/notes/{id} - 更新笔记..." -ForegroundColor Yellow
    try {
        $updateData = @{
            title = "更新的测试笔记 - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            content = "这个笔记已被更新。"
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "$VercelUrl/api/notes/$testNoteId" `
            -Method PUT `
            -ContentType "application/json" `
            -Body $updateData `
            -TimeoutSec 10
        
        Write-Host "  ✓ 笔记更新成功" -ForegroundColor Green
        Write-Host "  新标题: $($response.title)" -ForegroundColor Cyan
    } catch {
        Write-Host "  ✗ 更新失败: $($_.Exception.Message)" -ForegroundColor Red
        $allPassed = $false
    }
    Write-Host ""

    # 测试 6: 搜索笔记
    Write-Host "测试 6: GET /api/notes/search?q=测试 - 搜索笔记..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$VercelUrl/api/notes/search?q=测试" -Method GET -TimeoutSec 10
        Write-Host "  ✓ 搜索成功" -ForegroundColor Green
        Write-Host "  找到 $($response.Count) 条笔记" -ForegroundColor Cyan
    } catch {
        Write-Host "  ✗ 搜索失败: $($_.Exception.Message)" -ForegroundColor Red
        $allPassed = $false
    }
    Write-Host ""

    # 测试 7: 翻译笔记
    Write-Host "测试 7: POST /api/notes/{id}/translate - 翻译笔记..." -ForegroundColor Yellow
    try {
        $translateData = @{
            to = "English"
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "$VercelUrl/api/notes/$testNoteId/translate" `
            -Method POST `
            -ContentType "application/json" `
            -Body $translateData `
            -TimeoutSec 15
        
        Write-Host "  ✓ 翻译成功" -ForegroundColor Green
        Write-Host "  翻译内容: $($response.translated_content.Substring(0, [Math]::Min(50, $response.translated_content.Length)))..." -ForegroundColor Cyan
    } catch {
        Write-Host "  ⚠ 翻译失败: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "    (可能是 GITHUB_TOKEN 未配置)" -ForegroundColor Yellow
    }
    Write-Host ""

    # 测试 8: 删除笔记
    Write-Host "测试 8: DELETE /api/notes/{id} - 删除笔记..." -ForegroundColor Yellow
    try {
        Invoke-RestMethod -Uri "$VercelUrl/api/notes/$testNoteId" -Method DELETE -TimeoutSec 10
        Write-Host "  ✓ 笔记删除成功" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ 删除失败: $($_.Exception.Message)" -ForegroundColor Red
        $allPassed = $false
    }
    Write-Host ""
}

# 总结
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   测试结果" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

if ($allPassed) {
    Write-Host "✓ 所有核心功能测试通过！" -ForegroundColor Green
    Write-Host ""
    Write-Host "您的 Vercel 部署运行正常！" -ForegroundColor Green
    Write-Host "访问应用: $VercelUrl" -ForegroundColor Cyan
} else {
    Write-Host "✗ 部分测试失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "请检查：" -ForegroundColor Yellow
    Write-Host "  1. Vercel 环境变量是否正确配置" -ForegroundColor Cyan
    Write-Host "  2. MongoDB Atlas 网络访问是否允许所有 IP (0.0.0.0/0)" -ForegroundColor Cyan
    Write-Host "  3. 查看 Vercel 日志: vercel logs" -ForegroundColor Cyan
}

Write-Host ""
