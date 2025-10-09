# Vercel 部署检查清单

在部署之前，请确保完成以下步骤：

## ✅ 准备工作

- [ ] 已安装 Vercel CLI (`npm install -g vercel`)
- [ ] 已登录 Vercel (`vercel login`)
- [ ] 已创建或登录 MongoDB Atlas 账号
- [ ] 已获取 GitHub Token（用于 LLM API）

## ✅ MongoDB Atlas 配置

- [ ] 已创建 MongoDB 集群
- [ ] 已创建数据库用户：`Vercel-Admin-NoteTaker_note`
- [ ] 已配置网络访问：允许 `0.0.0.0/0`（所有 IP）
- [ ] 已测试 MongoDB 连接（运行 `.\test_mongodb_connection.ps1`）

## ✅ 项目文件检查

- [ ] `vercel.json` 文件已创建 ✓
- [ ] `api/index.py` 文件已创建 ✓
- [ ] `.vercelignore` 文件已创建 ✓
- [ ] `requirements.txt` 已更新（移除 SQLAlchemy，使用 python-dotenv）✓
- [ ] `src/main.py` 已更新（支持 MONGODB_URI）✓
- [ ] `.env` 文件包含正确的 MongoDB URI ✓

## ✅ 本地测试

- [ ] 运行 `.\test_mongodb_connection.ps1` - MongoDB 连接测试通过
- [ ] 运行 `.\test_local_with_atlas.ps1` - 本地服务器启动成功
- [ ] 访问 `http://localhost:5001` - 前端页面正常显示
- [ ] 访问 `http://localhost:5001/api/notes` - API 响应正常
- [ ] 测试创建笔记功能
- [ ] 测试翻译功能（需要 GITHUB_TOKEN）

## ✅ 部署到 Vercel

### 方法 1：使用 PowerShell 脚本
```powershell
.\deploy_to_vercel.ps1
```

### 方法 2：手动部署
```powershell
# 首次部署
vercel

# 部署到生产环境
vercel --prod
```

## ✅ 配置环境变量

选择一种方法配置环境变量：

### 方法 A：使用 CLI
```powershell
vercel env add MONGODB_URI production
# 粘贴: mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority

vercel env add MONGO_DB_NAME production
# 输入: notetaker_db

vercel env add GITHUB_TOKEN production
# 粘贴您的 GitHub Token

# 重新部署以应用环境变量
vercel --prod
```

### 方法 B：使用 Web 界面
1. 访问 Vercel Dashboard
2. 选择项目 > Settings > Environment Variables
3. 添加上述三个环境变量
4. 选择所有环境（Production, Preview, Development）
5. 触发重新部署

## ✅ 部署后验证

- [ ] 访问 Vercel 提供的 URL（例如：`https://your-project.vercel.app`）
- [ ] 检查前端页面是否正常加载
- [ ] 测试 API 端点：
  - [ ] GET `/api/notes` - 获取笔记列表
  - [ ] POST `/api/notes` - 创建新笔记
  - [ ] GET `/api/notes/{id}` - 获取单个笔记
  - [ ] PUT `/api/notes/{id}` - 更新笔记
  - [ ] DELETE `/api/notes/{id}` - 删除笔记
  - [ ] POST `/api/notes/{id}/translate` - 翻译笔记
- [ ] 检查 Vercel 日志（`vercel logs`）查看是否有错误

## ✅ API 测试示例

### 获取所有笔记
```powershell
curl https://your-project.vercel.app/api/notes
```

### 创建笔记
```powershell
$body = @{
    title = "测试笔记"
    content = "这是从 Vercel 部署的测试"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-project.vercel.app/api/notes" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### 翻译笔记
```powershell
$body = @{
    to = "Chinese"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-project.vercel.app/api/notes/{note_id}/translate" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

## ✅ 故障排查

如果遇到问题：

1. **查看部署日志**
   ```powershell
   vercel logs
   ```

2. **检查环境变量**
   ```powershell
   vercel env ls
   ```

3. **常见问题**
   - ❌ 500 错误 → 检查 MongoDB 连接字符串
   - ❌ 502 错误 → 函数超时或崩溃，查看日志
   - ❌ 404 错误 → 检查路由配置
   - ❌ CORS 错误 → 已配置 flask-cors，应该不会出现
   - ❌ 翻译失败 → 检查 GITHUB_TOKEN 是否正确

4. **MongoDB Atlas 问题**
   - 确保网络访问允许 0.0.0.0/0
   - 确保数据库用户密码正确
   - 确保集群在运行状态

5. **重新部署**
   ```powershell
   vercel --prod --force
   ```

## 📝 重要提示

1. **免费计划限制**
   - 函数执行时间：10 秒
   - 带宽：100 GB/月
   - 函数调用：100,000 次/天

2. **安全建议**
   - 不要将 `.env` 文件提交到 Git
   - 定期更换数据库密码
   - 考虑为生产和开发使用不同的数据库

3. **性能优化**
   - MongoDB Atlas 建议使用 M2 或更高级别的集群
   - 考虑添加数据库索引以提高查询性能
   - 监控函数执行时间

## 🎉 完成

部署成功后，您的应用将可以通过 Vercel 提供的 URL 访问！

记住：
- 生产 URL：`https://your-project.vercel.app`
- API 基础路径：`/api`
- 可以在 Vercel Dashboard 中查看分析和日志
