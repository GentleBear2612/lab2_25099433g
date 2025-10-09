# 🔥 Vercel 500 错误快速修复指南

## 问题：FUNCTION_INVOCATION_FAILED

您看到的 500 错误通常是因为 **环境变量未在 Vercel 中配置**。

## 🚨 紧急修复步骤

### 步骤 1：立即配置环境变量

**方法 A：使用 Vercel 网页界面（最快）**

1. 访问：https://vercel.com/dashboard
2. 选择您的项目
3. 点击 **Settings** > **Environment Variables**
4. 添加以下三个变量（点击 "Add" 按钮）：

   **变量 1: MONGODB_URI**
   ```
   mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority
   ```
   - 选择环境：✅ Production ✅ Preview ✅ Development

   **变量 2: MONGO_DB_NAME**
   ```
   notetaker_db
   ```
   - 选择环境：✅ Production ✅ Preview ✅ Development

   **变量 3: GITHUB_TOKEN**（可选，用于翻译功能）
   ```
   your_actual_github_token_here
   ```
   - 选择环境：✅ Production ✅ Preview ✅ Development

5. **保存后必须重新部署！**

**方法 B：使用 Vercel CLI**

```powershell
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 添加环境变量
vercel env add MONGODB_URI production
# 粘贴：mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority

vercel env add MONGO_DB_NAME production
# 输入：notetaker_db

vercel env add GITHUB_TOKEN production
# 输入您的 GitHub token

# 4. 重新部署
vercel --prod
```

### 步骤 2：验证 MongoDB Atlas 网络访问

1. 登录 MongoDB Atlas：https://cloud.mongodb.com/
2. 选择您的集群（notetaker-note）
3. 点击左侧菜单 **Network Access**
4. 确保有一条规则：
   - IP Address: `0.0.0.0/0`
   - Comment: "Allow from anywhere"
5. 如果没有，点击 **ADD IP ADDRESS** > **ALLOW ACCESS FROM ANYWHERE** > **Confirm**

### 步骤 3：重新部署

配置好环境变量后，**必须重新部署**：

```powershell
# 方法 1：使用 Vercel CLI
vercel --prod

# 方法 2：在 Vercel Dashboard 中
# 进入 Deployments > 点击右上角的 "..." > Redeploy
```

### 步骤 4：测试部署

部署完成后，再次访问您的 URL：

```
https://your-project.vercel.app/api/notes
```

应该能看到 JSON 响应（即使是空数组 `[]` 也表示成功）。

## 🔍 如何确认问题已解决

### 检查清单：

- [ ] 已在 Vercel 中添加 `MONGODB_URI` 环境变量
- [ ] 已在 Vercel 中添加 `MONGO_DB_NAME` 环境变量
- [ ] MongoDB Atlas Network Access 允许 0.0.0.0/0
- [ ] 已重新部署应用
- [ ] 可以访问 `/api/notes` 端点

## 📊 查看详细错误日志

如果问题仍然存在，查看详细日志：

```powershell
# 1. 安装 Vercel CLI（如果还没安装）
npm install -g vercel

# 2. 查看实时日志
vercel logs --follow

# 3. 查看最近的错误
vercel logs
```

## 🐛 常见错误和解决方案

### 错误 1：仍然看到 500 错误

**原因：** 环境变量配置后没有重新部署

**解决：**
```powershell
vercel --prod --force
```

### 错误 2：MongoDB 连接超时

**原因：** Network Access 未配置

**解决：**
1. MongoDB Atlas > Network Access
2. 添加 IP: 0.0.0.0/0

### 错误 3：认证失败

**原因：** 数据库用户名或密码错误

**解决：**
1. 检查 MONGODB_URI 中的用户名和密码
2. 在 MongoDB Atlas > Database Access 中重置密码
3. 更新 Vercel 环境变量中的 MONGODB_URI

## 🎯 快速测试脚本

创建一个测试文件 `test-env.ps1`：

```powershell
# 测试环境变量是否在 Vercel 中配置
Write-Host "检查 Vercel 环境变量..." -ForegroundColor Cyan

vercel env ls

Write-Host "`n如果看不到 MONGODB_URI 和 MONGO_DB_NAME，" -ForegroundColor Yellow
Write-Host "请立即配置它们！" -ForegroundColor Yellow
```

## 📞 仍然需要帮助？

### 检查这些地方：

1. **Vercel Dashboard**
   - Settings > Environment Variables
   - 确保所有变量都已添加

2. **MongoDB Atlas**
   - Network Access > 0.0.0.0/0 已添加
   - Database Access > 用户权限正确

3. **代码日志**
   ```powershell
   vercel logs --follow
   ```

## ✅ 成功标志

当一切正常时，您应该看到：

1. **访问首页**
   ```
   https://your-project.vercel.app/
   ```
   显示前端界面 ✅

2. **访问 API**
   ```
   https://your-project.vercel.app/api/notes
   ```
   返回 JSON 数据（`[]` 或笔记列表）✅

3. **Vercel 日志**
   ```
   ✓ Successfully connected to MongoDB: notetaker_db
   ```

## 🚀 下一步

修复后：
1. 运行完整测试：`.\test_vercel_deployment.ps1 https://your-project.vercel.app`
2. 查看完整文档：`TROUBLESHOOTING.md`
3. 如有问题：查看 Vercel 日志

---

**记住：每次修改环境变量后都要重新部署！** 🔄
