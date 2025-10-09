# 🚀 快速部署到 Vercel

## 前提条件
- ✅ 已安装 Node.js 和 npm
- ✅ 有 Vercel 账号
- ✅ 有 MongoDB Atlas 账号和连接字符串
- ✅ 有 GitHub Token（用于 LLM API）

## 三步部署

### 步骤 1：安装 Vercel CLI
```powershell
npm install -g vercel
vercel login
```

### 步骤 2：部署应用
```powershell
# 在项目根目录执行
vercel --prod
```

### 步骤 3：配置环境变量
```powershell
# 添加 MongoDB URI
vercel env add MONGODB_URI production
# 粘贴: mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority

# 添加数据库名称
vercel env add MONGO_DB_NAME production
# 输入: notetaker_db

# 添加 GitHub Token
vercel env add GITHUB_TOKEN production
# 粘贴您的 token

# 重新部署以应用环境变量
vercel --prod
```

## 完成！🎉

访问 Vercel 提供的 URL 即可使用您的应用。

## 本地测试（可选）

在部署前，可以先在本地测试 MongoDB Atlas 连接：

```powershell
# 测试 MongoDB 连接
.\test_mongodb_connection.ps1

# 启动本地服务器（使用 Atlas）
.\test_local_with_atlas.ps1
```

## 需要详细说明？

查看完整文档：
- 📖 [完整部署指南](VERCEL_DEPLOYMENT.md)
- ✅ [部署检查清单](DEPLOYMENT_CHECKLIST.md)
- 🔧 [环境变量配置](VERCEL_ENV_SETUP.md)
- 📝 [修改总结](SUMMARY_OF_CHANGES.md)

## 问题排查

如果遇到问题：
```powershell
# 查看部署日志
vercel logs

# 查看环境变量
vercel env ls

# 强制重新部署
vercel --prod --force
```
