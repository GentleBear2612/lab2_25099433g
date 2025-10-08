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

## 必要的环境变量（在 Vercel Dashboard -> Settings -> Environment Variables 中添加）
- `MONGO_URI` = 你的 Atlas 连接字符串（含用户名/密码）
- `MONGO_DB_NAME` = notetaker_db（或你的数据库名，如果不设置，默认使用 notetaker_db）

注意：不要把敏感信息写入代码或提交到仓库。使用 Vercel 的环境变量功能保存凭据。

## 部署步骤（CLI）
1. 登录 Vercel：
```
npm i -g vercel
vercel login
```
2. 在项目根执行：
```
vercel --prod
```
3. 在 Vercel Dashboard 设置好 `MONGO_URI` 与 `MONGO_DB_NAME`（或者使用 `vercel env add` 命令）。

## 常见问题与排查
- 如果函数日志报 `SSL handshake failed` 或类似 TLS 错误：
  - 尝试在 Atlas 暂时允许 0.0.0.0/0（用于验证是否为 IP 白名单问题），若确认是白名单问题请改用支持静态出站 IP 的后端部署方案（例如 Render、Cloud Run + NAT）。
  - 我们在 `api/_mongo.py` 中使用了 `tlsCAFile=certifi.where()` 来尽量避免 CA 信任差异。
- 如果连接被拒绝或超时：确认 Atlas 的 Network Access 是否允许来自 Vercel 的 IP（Vercel 并没有固定出站 IP，通常无法直接加入白名单）。

## 安全建议
- 不要把 `MONGO_URI` 写在脚本里（仓库中有旧的 `start_flask_with_atlas.ps1`，请删除其中的明文凭据或改为读取 env）。
- 在生产环境不要使用 `0.0.0.0/0`，应使用私有网络或 VPC peering/Private Endpoint。

## 本地测试
- 在本地测试 serverless endpoints：
  1. 在 PowerShell 中设置 env：
     ```powershell
     $env:MONGO_URI = '你的URI'
     $env:MONGO_DB_NAME = 'notetaker_db'
     ```
  2. 运行 `vercel dev` 或直接用 Python 运行专门的测试脚本（例如 repo 下的 `scripts/check_mongo_uri.py`）来验证连接。

如果你希望我把 `start_flask_with_atlas.ps1` 中的明文凭据移除并替换为读取环境变量的版本，我也可以替你改并提交。 
