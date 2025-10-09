# Vercel 部署指南

本应用已配置为可在 Vercel 上部署，并使用 MongoDB Atlas 作为数据库。

## 部署步骤

### 1. 准备工作

确保您已经有：
- Vercel 账号（https://vercel.com）
- MongoDB Atlas 账号及连接字符串
- GitHub Token（用于 LLM API 调用）

### 2. MongoDB Atlas 设置

您提供的 MongoDB URI 是：
```
mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority
```

确保在 MongoDB Atlas 中：
1. 数据库访问白名单中添加了 `0.0.0.0/0`（允许所有 IP），因为 Vercel 的 IP 是动态的
2. 数据库用户有读写权限

### 3. 使用 Vercel CLI 部署（推荐）

```powershell
# 安装 Vercel CLI（如果还没安装）
npm install -g vercel

# 登录 Vercel
vercel login

# 在项目根目录执行部署
vercel

# 设置环境变量
vercel env add MONGODB_URI
# 粘贴您的 MongoDB URI：mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority

vercel env add MONGO_DB_NAME
# 输入：notetaker_db

vercel env add GITHUB_TOKEN
# 粘贴您的 GitHub Token

# 重新部署以应用环境变量
vercel --prod
```

### 4. 使用 Vercel 网页界面部署

1. 访问 https://vercel.com/new
2. 导入您的 Git 仓库
3. Vercel 会自动检测到 `vercel.json` 配置
4. 在项目设置 > Environment Variables 中添加：
   - `MONGODB_URI`: `mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority`
   - `MONGO_DB_NAME`: `notetaker_db`
   - `GITHUB_TOKEN`: 您的 GitHub Token
5. 点击 Deploy

### 5. 验证部署

部署完成后，访问 Vercel 提供的 URL：
- `https://your-project.vercel.app/` - 应该显示前端页面
- `https://your-project.vercel.app/api/notes` - 应该返回笔记列表（JSON）

### 6. 测试 API

```powershell
# 获取所有笔记
curl https://your-project.vercel.app/api/notes

# 创建新笔记
curl -X POST https://your-project.vercel.app/api/notes `
  -H "Content-Type: application/json" `
  -d '{"title":"测试笔记","content":"这是测试内容"}'

# 翻译笔记（将 note_id 替换为实际的笔记 ID）
curl -X POST https://your-project.vercel.app/api/notes/{note_id}/translate `
  -H "Content-Type: application/json" `
  -d '{"to":"Chinese"}'
```

## 项目结构说明

- `vercel.json`: Vercel 配置文件，定义了构建和路由规则
- `api/index.py`: Vercel serverless 函数入口点
- `src/main.py`: Flask 应用主文件
- `requirements.txt`: Python 依赖
- `.vercelignore`: 指定部署时忽略的文件

## 重要注意事项

1. **Serverless 限制**：Vercel 的免费计划有以下限制：
   - 函数执行时间：10 秒
   - 函数大小：50 MB
   - 如果翻译操作超时，考虑升级计划

2. **环境变量**：所有敏感信息都应该在 Vercel 的环境变量中配置，不要提交到代码仓库

3. **数据库连接**：MongoDB Atlas 的连接会在每次函数调用时建立，这是 serverless 的正常行为

4. **静态文件**：`src/static/` 目录中的文件会随应用一起部署

## 故障排查

如果遇到问题：

1. 检查 Vercel 的部署日志
2. 确保环境变量设置正确
3. 检查 MongoDB Atlas 网络访问设置
4. 使用 `vercel logs` 查看运行时日志

## 本地测试

在部署前，可以本地测试：

```powershell
# 设置环境变量
$env:MONGODB_URI="mongodb+srv://Vercel-Admin-NoteTaker_note:NsS9hY3femZtWLsW@notetaker-note.bqbvigx.mongodb.net/?retryWrites=true&w=majority"
$env:MONGO_DB_NAME="notetaker_db"
$env:GITHUB_TOKEN="your_token"

# 运行应用
python src/main.py
```
