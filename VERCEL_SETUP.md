# Vercel 部署配置指南

## 问题说明

如果您在 Vercel 上部署时遇到 `/api/notes:1 Failed to load resource: the server responded with a status of 500` 错误，这通常是因为 MongoDB 连接未正确配置。

## 解决方案

### 1. 在 Vercel 中配置环境变量

您需要在 Vercel 项目中设置以下环境变量：

1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择您的项目
3. 进入 **Settings** > **Environment Variables**
4. 添加以下环境变量：

#### 必需的环境变量：

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

将上述 URI 替换为您的实际 MongoDB Atlas 连接字符串。

#### 可选的环境变量：

```
MONGO_DB_NAME=notetaker_db
```

如果不设置，默认使用 `notetaker_db`。

### 2. 获取 MongoDB Atlas 连接字符串

如果您还没有 MongoDB Atlas 账户：

1. 访问 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. 创建免费账户
3. 创建一个新的集群（免费层即可）
4. 点击 **Connect** 按钮
5. 选择 **Connect your application**
6. 复制连接字符串
7. 将 `<password>` 替换为您的数据库用户密码

示例连接字符串：
```
mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 3. 重新部署

设置环境变量后：

1. 在 Vercel Dashboard 中，进入 **Deployments** 标签
2. 点击最新部署旁边的三个点
3. 选择 **Redeploy**

或者，推送新的代码到您的 Git 仓库，Vercel 会自动重新部署。

### 4. 验证部署

部署完成后，访问：
```
https://your-app.vercel.app/api/notes
```

您应该看到一个空数组 `[]` 或包含笔记的 JSON 数组，而不是 500 错误。

## 代码更改说明

我已经对以下文件进行了修改，使其与 Vercel 的无服务器函数兼容：

- `api/notes.py` - 修改为使用 Flask Response 对象
- `api/note.py` - 修改为使用 Flask Response 对象
- `api/users.py` - 修改为使用 Flask Response 对象
- `api/user.py` - 修改为使用 Flask Response 对象
- `api/_mongo.py` - 改进错误处理和连接管理

主要更改：
1. 将返回格式从字典（`{'statusCode': 200, 'body': ...}`）改为 Flask Response 对象
2. 添加 CORS 头部支持 (`Access-Control-Allow-Origin: *`)
3. 改进异常处理和错误日志

## 备用方案：使用内存数据库

如果您暂时无法配置 MongoDB，代码现在包含一个内存中的备用数据库。这意味着：

- ✅ 应用不会崩溃（不会返回 500 错误）
- ✅ 前端可以正常工作
- ⚠️ 数据不会持久化（每次部署后数据会丢失）
- ⚠️ 不适合生产环境

您会在 Vercel 的函数日志中看到警告：
```
WARNING: MONGO_URI not set — using in-memory fallback (ephemeral).
```

## 故障排除

### 如果仍然遇到 500 错误：

1. 检查 Vercel 函数日志：
   - 进入 Vercel Dashboard
   - 选择您的项目
   - 点击最新部署
   - 查看 **Functions** 标签下的日志

2. 验证 MongoDB 连接字符串：
   - 确保密码中的特殊字符已正确编码
   - 确保 IP 白名单包含 `0.0.0.0/0`（允许所有 IP）或 Vercel 的 IP 范围

3. 测试 MongoDB 连接：
   ```bash
   python scripts/check_mongo.py
   ```

### 如果 CORS 错误：

前端代码现在包含了 `Access-Control-Allow-Origin: *` 头部，应该可以解决 CORS 问题。

## 本地测试

在部署到 Vercel 之前，您可以在本地测试：

1. 创建 `.env` 文件：
   ```
   MONGO_URI=your_mongodb_connection_string
   MONGO_DB_NAME=notetaker_db
   ```

2. 运行 Flask 应用：
   ```bash
   python src/main.py
   ```

3. 测试 API：
   ```bash
   curl http://localhost:5000/api/notes
   ```

## 需要帮助？

如果您遇到其他问题，请检查：
- Vercel 函数日志
- MongoDB Atlas 网络访问设置
- 环境变量拼写和格式
