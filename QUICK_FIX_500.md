# 🔥 500 错误 - 立即修复！

## 问题诊断

您看到的错误：
```
500: INTERNAL_SERVER_ERROR
Code: FUNCTION_INVOCATION_FAILED
```

**根本原因：** 环境变量未在 Vercel 中配置

## ⚡ 3 步快速修复

### 步骤 1：配置环境变量（必须！）

访问：**https://vercel.com/dashboard**

1. 选择您的项目
2. Settings > Environment Variables
3. 添加这 3 个变量：

| 变量名 | 值 | 环境 |
|--------|-----|------|
| `MONGODB_URI` | `mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority` | Production, Preview, Development |
| `MONGO_DB_NAME` | `notetaker_db` | Production, Preview, Development |
| `GITHUB_TOKEN` | 您的 token（可选） | Production, Preview, Development |

### 步骤 2：重新部署

**重要：** 配置环境变量后必须重新部署！

在 Vercel Dashboard 中：
- Deployments > 点击最新部署旁的 "..." > **Redeploy**

或使用命令行：
```powershell
npm install -g vercel
vercel login
vercel --prod
```

### 步骤 3：测试

访问您的应用：
```
https://your-project.vercel.app/api/notes
```

应该看到 JSON 响应（`[]` 或笔记列表）✅

## 🔍 如何验证环境变量已配置

```powershell
# 运行检查脚本
.\check_vercel_env.ps1
```

应该看到：
```
MONGODB_URI
MONGO_DB_NAME
GITHUB_TOKEN (optional)
```

## ❓ 仍然有问题？

查看详细指南：
```
打开文件: FIX_500_ERROR.md
```

或运行诊断：
```powershell
# 1. 检查本地连接
.\test_mongodb_connection.ps1

# 2. 检查 Vercel 环境变量
.\check_vercel_env.ps1
```

## 📋 完整检查清单

- [ ] 已在 Vercel 中添加 `MONGODB_URI`
- [ ] 已在 Vercel 中添加 `MONGO_DB_NAME`
- [ ] MongoDB Atlas Network Access 允许 `0.0.0.0/0`
- [ ] 已重新部署应用（重要！）
- [ ] 可以访问 `/api/notes` 不报错

## 🎯 成功标志

当修复成功时：
- ✅ 访问首页显示界面
- ✅ `/api/notes` 返回 JSON
- ✅ 可以创建和查看笔记

---

**记住：每次修改环境变量后都要重新部署！** 🔄

需要帮助？查看 `TROUBLESHOOTING.md`
