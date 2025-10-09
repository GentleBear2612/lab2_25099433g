# 测试 Vercel 部署的各个端点

Write-Host "正在测试 Vercel 部署..." -ForegroundColor Cyan
Write-Host ""

$baseUrl = "https://lab2-25099433g-o7aptrrm8-gentlebears-projects-c14ff97f.vercel.app"

# 测试 1: 纯 Python 端点
Write-Host "[1/5] 测试纯 Python 端点: /api/test" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/test" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  ✓ 状态: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content.Substring(0, [Math]::Min(100, $response.Content.Length)))" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 错误: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 测试 2: Health 端点
Write-Host "[2/5] 测试健康检查: /api/health" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/health" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  ✓ 状态: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 错误: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 测试 3: Simple 端点
Write-Host "[3/5] 测试简化端点: /api/simple" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/simple" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  ✓ 状态: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 错误: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 测试 4: Debug 端点
Write-Host "[4/5] 测试调试端点: /api/debug" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/debug" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  ✓ 状态: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content.Substring(0, [Math]::Min(200, $response.Content.Length)))" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 错误: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 测试 5: Notes 端点（已知会失败）
Write-Host "[5/5] 测试笔记端点: /api/notes" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/notes" -Method GET -TimeoutSec 10 -UseBasicParsing
    Write-Host "  ✓ 状态: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "  响应: $($response.Content)" -ForegroundColor Cyan
} catch {
    Write-Host "  ✗ 错误: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        try {
            $reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
            $errorBody = $reader.ReadToEnd()
            Write-Host "  错误详情: $errorBody" -ForegroundColor Gray
        } catch {}
    }
}

Write-Host ""
Write-Host "测试完成！" -ForegroundColor Green
Write-Host ""
Write-Host "💡 提示: 如果某些端点成功，说明 Vercel 工作正常，问题在特定代码中" -ForegroundColor Yellow
