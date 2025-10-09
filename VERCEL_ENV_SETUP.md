# Vercel 环境变量配置快速指南

## 方法 1：使用 Vercel CLI（推荐）

```powershell
# 添加 MONGODB_URI
vercel env add MONGODB_URI production
# 粘贴: mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority

# 添加 MONGO_DB_NAME
vercel env add MONGO_DB_NAME production
# 输入: notetaker_db

# 添加 GITHUB_TOKEN
vercel env add GITHUB_TOKEN production
# 粘贴您的 GitHub Token
```

## 方法 2：使用 Vercel 网页界面

1. 访问您的项目：https://vercel.com/dashboard
2. 选择您的项目
3. 进入 **Settings** > **Environment Variables**
4. 添加以下变量：

### MONGODB_URI
```
mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority
```
- Environment: Production, Preview, Development（全选）

### MONGO_DB_NAME
```
notetaker_db
```
- Environment: Production, Preview, Development（全选）

### GITHUB_TOKEN
```
your_github_token_here
```
- Environment: Production, Preview, Development（全选）

## 验证环境变量

部署后，您可以通过以下方式验证环境变量是否正确配置：

1. 访问您的应用 URL
2. 尝试访问 `/api/notes` 端点
3. 如果能正常返回数据，说明 MongoDB 连接成功
4. 尝试翻译功能，如果能正常工作，说明 GITHUB_TOKEN 配置正确

## 注意事项

⚠️ **安全提示**：
- 不要将这些凭证提交到 Git 仓库
- 定期更换数据库密码和 API 密钥
- 在 MongoDB Atlas 中，确保网络访问设置允许 Vercel 的 IP（0.0.0.0/0）

## MongoDB Atlas 网络配置

确保在 MongoDB Atlas 中配置了正确的网络访问：

1. 登录 MongoDB Atlas
2. 进入您的集群
3. 点击 **Network Access**
4. 添加 IP 地址：`0.0.0.0/0`（允许所有 IP）
   - 或者使用 Vercel 的 IP 范围（需要专业版）

## 常见问题

### 1. 连接超时
- 检查 MongoDB Atlas 网络访问设置
- 确保 MONGODB_URI 正确无误

### 2. 认证失败
- 检查用户名和密码是否正确
- 确保数据库用户有正确的权限

### 3. 翻译功能不工作
- 检查 GITHUB_TOKEN 是否有效
- 确保 token 有访问 GitHub Models API 的权限
