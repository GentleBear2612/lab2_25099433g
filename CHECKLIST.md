# Vercel 部署检查清单

在部署到 Vercel 前，请确保完成以下所有步骤：

## ✅ 代码准备（已完成）

- [x] 修改 `api/notes.py` 使用 Flask Response
- [x] 修改 `api/note.py` 使用 Flask Response
- [x] 修改 `api/users.py` 使用 Flask Response
- [x] 修改 `api/user.py` 使用 Flask Response
- [x] 添加 CORS 头部到所有响应
- [x] 改进错误处理和日志
- [x] 创建辅助工具和文档

## 📋 部署前检查

### 1. MongoDB Atlas 配置

- [ ] 已创建 MongoDB Atlas 账号
- [ ] 已创建集群（免费层即可）
- [ ] 已创建数据库用户
- [ ] 已设置网络访问（允许 0.0.0.0/0）
- [ ] 已获取连接字符串

**获取连接字符串：**
1. MongoDB Atlas → Clusters → Connect
2. 选择 "Connect your application"
3. 复制连接字符串
4. 替换 `<password>` 为实际密码

**示例：**
```
mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 2. Vercel 项目设置

- [ ] 已创建 Vercel 账号
- [ ] 已导入 GitHub 仓库到 Vercel
- [ ] 已在 Vercel Dashboard 中找到项目

### 3. 环境变量配置（关键！）

- [ ] 在 Vercel 中设置 `MONGO_URI`
- [ ] 在 Vercel 中设置 `MONGO_DB_NAME`
- [ ] 环境变量应用到 Production 环境
- [ ] 环境变量应用到 Preview 环境（可选）

**设置位置：**
Vercel Dashboard → 选择项目 → Settings → Environment Variables

**必需的环境变量：**
```
MONGO_URI = mongodb+srv://user:pass@cluster.mongodb.net/...
MONGO_DB_NAME = notetaker_db
```

### 4. 本地测试（推荐）

- [ ] 设置本地环境变量
- [ ] 运行 `python scripts/check_vercel_env.py`
- [ ] 运行 `python scripts/test_api_response.py`
- [ ] 确保所有测试通过

**Windows PowerShell：**
```powershell
$env:MONGO_URI = "your-connection-string"
$env:MONGO_DB_NAME = "notetaker_db"
python scripts/test_api_response.py
```

## 🚀 部署步骤

### 方法 1：Git 推送（推荐）

- [ ] 提交所有代码更改
- [ ] 推送到 GitHub
- [ ] Vercel 自动部署

```bash
git add .
git commit -m "Fix: Update for Vercel compatibility"
git push
```

### 方法 2：Vercel CLI

- [ ] 安装 Vercel CLI: `npm install -g vercel`
- [ ] 登录: `vercel login`
- [ ] 部署: `vercel --prod`

### 方法 3：手动重新部署

- [ ] 访问 Vercel Dashboard
- [ ] 选择项目 → Deployments
- [ ] 点击最新部署旁的三个点
- [ ] 选择 "Redeploy"

## ✅ 部署后验证

### 1. 检查部署状态

- [ ] 在 Vercel Dashboard 中查看部署状态
- [ ] 确认部署成功（绿色勾号）
- [ ] 没有构建错误

### 2. 测试 API 端点

访问以下 URL（替换为您的实际域名）：

- [ ] `https://your-app.vercel.app/api/notes` → 返回 200，内容为 `[]` 或笔记数组
- [ ] `https://your-app.vercel.app/` → 显示前端页面

**不应该看到：**
- ❌ 500 Internal Server Error
- ❌ 503 Service Unavailable

### 3. 检查函数日志

- [ ] Vercel Dashboard → 项目 → 最新部署
- [ ] 点击 "Functions" 标签
- [ ] 查看 `/api/notes` 的日志
- [ ] 确认没有错误信息

**正常日志示例：**
```
✅ Using real MongoDB client
```

**问题日志示例：**
```
⚠️ WARNING: MONGO_URI not set — using in-memory fallback (ephemeral).
```
如果看到此警告，说明环境变量未正确设置。

### 4. 测试前端功能

- [ ] 可以创建新笔记
- [ ] 可以编辑笔记
- [ ] 可以删除笔记
- [ ] 可以搜索笔记
- [ ] 刷新页面后数据仍然存在

## 🔧 故障排除

### 问题 1：500 错误

**可能原因：**
- MONGO_URI 未设置或格式错误
- MongoDB 连接失败

**解决方法：**
1. 检查 Vercel 环境变量
2. 检查 MongoDB Atlas 网络访问
3. 查看 Vercel 函数日志
4. 运行 `python scripts/check_vercel_env.py`

### 问题 2：503 Service Unavailable

**可能原因：**
- MONGO_URI 未配置

**解决方法：**
1. 在 Vercel 中设置 MONGO_URI
2. 重新部署

### 问题 3：数据不持久化

**可能原因：**
- 使用了内存备用数据库

**解决方法：**
1. 在 Vercel 中设置 MONGO_URI
2. 重新部署

### 问题 4：连接超时

**可能原因：**
- MongoDB Atlas IP 白名单限制

**解决方法：**
1. MongoDB Atlas → Network Access
2. 添加 IP 地址 `0.0.0.0/0`

### 问题 5：Authentication Failed

**可能原因：**
- 密码包含特殊字符未编码
- 数据库用户不存在

**解决方法：**
1. 对密码进行 URL 编码
   - `@` → `%40`
   - `!` → `%21`
   - `#` → `%23`
2. 在 MongoDB Atlas 中验证用户存在

## 📚 参考文档

- [FIX_SUMMARY.md](FIX_SUMMARY.md) - 完整的修复总结
- [VERCEL_SETUP.md](VERCEL_SETUP.md) - 详细配置指南
- [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md) - 快速部署指南

## 🆘 需要帮助？

如果您遇到问题：

1. **查看文档**：
   - FIX_SUMMARY.md
   - VERCEL_SETUP.md

2. **运行诊断工具**：
   ```bash
   python scripts/check_vercel_env.py
   python scripts/test_api_response.py
   ```

3. **检查日志**：
   - Vercel Dashboard → Functions → 查看日志
   - 查找错误消息和堆栈跟踪

4. **常见问题**：
   - 环境变量拼写是否正确？
   - 是否应用到 Production 环境？
   - MongoDB 密码是否需要 URL 编码？
   - MongoDB Atlas 是否允许 0.0.0.0/0？

---

**完成所有检查后，您的应用应该可以在 Vercel 上正常运行！** 🎉
