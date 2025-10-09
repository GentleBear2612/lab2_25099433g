# Vercel 部署快速诊断脚本
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "Vercel 部署诊断工具" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan

$vercelUrl = Read-Host "`n请输入你的 Vercel 项目 URL (例如: https://your-project.vercel.app)"

if ([string]::IsNullOrWhiteSpace($vercelUrl)) {
    Write-Host "`n❌ 错误: 未提供 URL" -ForegroundColor Red
    exit 1
}

# 移除尾部的斜杠
$vercelUrl = $vercelUrl.TrimEnd('/')

Write-Host "`n测试 URL: $vercelUrl" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# 测试 1: 健康检查
Write-Host "`n[1/4] 测试健康检查端点: /api/health" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$vercelUrl/api/health" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content)" -ForegroundColor Cyan
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ 健康检查通过" -ForegroundColor Green
    }
} catch {
    Write-Host "  ✗ 请求失败: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  详细信息: $($_.Exception)" -ForegroundColor Gray
}

# 测试 2: 获取笔记列表
Write-Host "`n[2/4] 测试获取笔记列表: /api/notes" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$vercelUrl/api/notes" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  状态码: $($response.StatusCode)" -ForegroundColor Green
    $content = $response.Content
    if ($content.Length -gt 200) {
        $content = $content.Substring(0, 200) + "..."
    }
    Write-Host "  响应: $content" -ForegroundColor Cyan
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✓ API 正常工作" -ForegroundColor Green
    }
} catch {
    Write-Host "  ✗ 请求失败: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "  错误响应: $responseBody" -ForegroundColor Gray
    }
}

# 测试 3: 前端页面
Write-Host "`n[3/4] 测试前端页面: /" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $vercelUrl -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  状态码: $($response.StatusCode)" -ForegroundColor Green
    if ($response.StatusCode -eq 200 -and $response.Content -like "*NoteTaker*") {
        Write-Host "  ✓ 前端页面加载成功" -ForegroundColor Green
    } else {
        Write-Host "  ✗ 前端页面内容异常" -ForegroundColor Red
    }
} catch {
    Write-Host "  ✗ 请求失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 测试 4: 创建测试笔记
Write-Host "`n[4/4] 测试创建笔记: POST /api/notes" -ForegroundColor Yellow
try {
    $testData = @{
        title = "测试笔记"
        content = "这是一个测试笔记，用于验证 API 功能"
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$vercelUrl/api/notes" -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 10 -UseBasicParsing
    Write-Host "  状态码: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content)" -ForegroundColor Cyan
    if ($response.StatusCode -eq 201) {
        Write-Host "  ✓ 创建笔记成功" -ForegroundColor Green
        
        # 尝试删除测试笔记
        $data = $response.Content | ConvertFrom-Json
        if ($data.id) {
            $deleteResponse = Invoke-WebRequest -Uri "$vercelUrl/api/notes/$($data.id)" -Method DELETE -TimeoutSec 10 -UseBasicParsing
            if ($deleteResponse.StatusCode -eq 200) {
                Write-Host "  ✓ 测试笔记已清理" -ForegroundColor Green
            }
        }
    }
} catch {
    Write-Host "  ✗ 请求失败: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        try {
            $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "  错误响应: $responseBody" -ForegroundColor Gray
        } catch {
            # Ignore errors reading error response
        }
    }
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "诊断完成！" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "`n💡 提示:" -ForegroundColor Yellow
Write-Host "- 如果健康检查失败，说明 API 服务未启动或环境变量配置错误" -ForegroundColor White
Write-Host "- 如果健康检查通过但笔记列表失败，说明数据库连接有问题" -ForegroundColor White
Write-Host "- 检查 Vercel Dashboard -> Functions -> View Function Logs 查看详细错误" -ForegroundColor White
