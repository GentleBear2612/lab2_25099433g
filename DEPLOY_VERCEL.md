# 部署到 Vercel（快速指南）

下面说明如何把仓库部署到 Vercel（后端作为 serverless Python 函数，前端静态文件由 Vercel 托管）。

## 先决条件
- 有一个 Vercel 账号
- 安装并登录 Vercel CLI（可选）
- MongoDB Atlas 帐号与 cluster，以及能用于连接的 `MONGO_URI`（示例：mongodb+srv://user:pass@cluster0.example.net/?retryWrites=true&w=majority）

## 仓库中关键文件
- `vercel.json`：Vercel 构建与路由配置
- `api/*.py`：serverless endpoints（例如 `api/notes.py`, `api/note.py`, `api/users.py`, `api/user.py`）
- `api/_mongo.py`：共享的 Mongo 连接逻辑，使用 certifi 作为 CA

## ⚠️ 重要：解决 500 错误

如果您遇到 `/api/notes` 返回 500 错误，请按以下步骤操作：

### 第一步：配置环境变量（必需）

在 Vercel Dashboard 中添加以下环境变量：

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择您的项目
3. 进入 **Settings** → **Environment Variables**
4. 添加以下变量：

```
MONGO_URI = mongodb+srv://your-username:your-password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME = notetaker_db
```

**⚠️ 重要提示：**
- `MONGO_URI` 是必需的！如果不设置，将使用内存数据库（数据不持久化）
- 确保密码中的特殊字符已进行 URL 编码
- 示例：如果密码是 `p@ss!word`，应该编码为 `p%40ss%21word`

### 第二步：配置 MongoDB Atlas 网络访问

1. 登录 [MongoDB Atlas](https://cloud.mongodb.com/)
2. 选择您的集群
3. 进入 **Network Access**
4. 点击 **Add IP Address**
5. 选择 **Allow Access from Anywhere** (0.0.0.0/0)
   - 注意：这对于 Vercel 是必需的，因为 Vercel 没有固定的出站 IP

### 第三步：重新部署

设置环境变量后，需要重新部署：

#### 方法 1：通过 Git 推送
```bash
git add .
git commit -m "Configure for Vercel"
git push
```

#### 方法 2：手动重新部署
1. 在 Vercel Dashboard 中进入 **Deployments**
2. 找到最新的部署
3. 点击三个点菜单
4. 选择 **Redeploy**

### 第四步：验证部署

部署完成后，访问：
```
https://your-app.vercel.app/api/notes
```

您应该看到：
- ✅ `[]`（空数组，表示没有笔记）
- ✅ 或包含笔记数据的 JSON 数组

如果仍然看到 500 错误，查看函数日志：
1. Vercel Dashboard → 选择项目
2. 点击最新部署
3. 查看 **Functions** 标签

## 必要的环境变量（在 Vercel Dashboard -> Settings -> Environment Variables 中添加）
- `MONGO_URI` = 你的 Atlas 连接字符串（含用户名/密码）**【必需】**
- `MONGO_DB_NAME` = notetaker_db（或你的数据库名，如果不设置，默认使用 notetaker_db）

注意：不要把敏感信息写入代码或提交到仓库。使用 Vercel 的环境变量功能保存凭据。

## 部署步骤（CLI）
1. 登录 Vercel：
```bash
npm i -g vercel
vercel login
```
2. 在项目根执行：
```bash
vercel --prod
```
3. 在 Vercel Dashboard 设置好 `MONGO_URI` 与 `MONGO_DB_NAME`（或者使用 `vercel env add` 命令）：
```bash
vercel env add MONGO_URI
# 粘贴您的 MongoDB 连接字符串

vercel env add MONGO_DB_NAME
# 输入：notetaker_db
```

## 部署步骤（GitHub 集成）- 推荐
1. 将代码推送到 GitHub
2. 在 Vercel Dashboard 中：
   - 点击 **New Project**
   - 选择您的 GitHub 仓库
   - 点击 **Import**
3. **在导入前**，添加环境变量：
   - 展开 **Environment Variables** 部分
   - 添加 `MONGO_URI` 和 `MONGO_DB_NAME`
4. 点击 **Deploy**

## 代码更新说明

本次更新修复了 Vercel 部署时的 500 错误：

### 修改的文件：
- ✅ `api/notes.py` - 使用 Flask Response 对象替代字典格式
- ✅ `api/note.py` - 使用 Flask Response 对象替代字典格式
- ✅ `api/users.py` - 使用 Flask Response 对象替代字典格式
- ✅ `api/user.py` - 使用 Flask Response 对象替代字典格式
- ✅ `api/_mongo.py` - 改进错误处理
- ✅ `vercel.json` - 添加环境变量配置

### 主要改进：
1. **正确的响应格式**：从字典格式改为 Flask Response 对象
2. **CORS 支持**：添加 `Access-Control-Allow-Origin: *` 头部
3. **更好的错误处理**：详细的错误信息和日志
4. **备用数据库**：如果未配置 MongoDB，使用内存数据库（仅用于测试）

## 常见问题与排查

### 问题 1：500 Internal Server Error
**原因**：`MONGO_URI` 未设置或无法连接到 MongoDB

**解决方案**：
1. 检查 Vercel 环境变量是否正确设置
2. 检查 MongoDB Atlas 网络访问设置
3. 查看 Vercel 函数日志获取详细错误

### 问题 2：SSL/TLS 错误
**原因**：证书验证问题

**解决方案**：
- 我们已在 `api/_mongo.py` 中使用 `tlsCAFile=certifi.where()` 来解决此问题
- 确保 `certifi` 包在 `requirements.txt` 中

### 问题 3：连接超时
**原因**：MongoDB Atlas IP 白名单限制

**解决方案**：
1. 在 Atlas 中进入 **Network Access**
2. 添加 IP 地址 `0.0.0.0/0`（允许所有 IP）
3. 注意：Vercel 无服务器函数没有固定 IP，必须允许所有 IP 或使用私有链接

### 问题 4：数据不持久化
**症状**：每次访问数据都消失了

**原因**：`MONGO_URI` 未设置，使用了内存备用数据库

**解决方案**：
- 在 Vercel 中设置 `MONGO_URI` 环境变量
- 重新部署应用

## 安全建议
- ❌ 不要把 `MONGO_URI` 写在代码中
- ❌ 不要把 `MONGO_URI` 提交到 Git 仓库
- ✅ 始终使用 Vercel 的环境变量功能
- ⚠️ 在生产环境中，不要使用 `0.0.0.0/0`，应使用 VPC peering 或 Private Endpoint

## 本地测试

### 测试 1：验证环境配置
```powershell
# 设置环境变量
$env:MONGO_URI = 'mongodb+srv://user:pass@cluster.mongodb.net/'
$env:MONGO_DB_NAME = 'notetaker_db'

# 运行检查脚本
python scripts/check_vercel_env.py
```

### 测试 2：测试 API 响应格式
```powershell
python scripts/test_api_response.py
```

### 测试 3：本地运行 Vercel Dev
```bash
vercel dev
```

然后访问 `http://localhost:3000/api/notes`

## 更多帮助

如需更详细的设置说明，请参阅：
- `VERCEL_SETUP.md` - 完整的 Vercel 配置指南
- `scripts/check_vercel_env.py` - 环境检查工具
- `scripts/test_api_response.py` - API 测试工具

如果你希望我把 `start_flask_with_atlas.ps1` 中的明文凭据移除并替换为读取环境变量的版本，我也可以替你改并提交。 
