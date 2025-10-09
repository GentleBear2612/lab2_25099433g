# 🔧 故障排查指南

## 常见问题及解决方案

### 1. 部署失败

#### 问题：`vercel` 命令不存在
```powershell
# 解决方案：安装 Vercel CLI
npm install -g vercel
```

#### 问题：构建失败 - Python 依赖安装错误
```
# 检查 requirements.txt 格式
# 确保没有多余的空行或注释
# 尝试本地安装所有依赖
pip install -r requirements.txt
```

### 2. MongoDB 连接问题

#### 问题：连接超时 (ServerSelectionTimeoutError)
**原因：** MongoDB Atlas 网络访问限制

**解决方案：**
1. 登录 MongoDB Atlas
2. 进入 Network Access
3. 添加 IP 地址：`0.0.0.0/0`（允许所有 IP）
4. 等待 1-2 分钟使设置生效

#### 问题：认证失败 (Authentication failed)
**原因：** 用户名或密码错误

**解决方案：**
1. 检查 MONGODB_URI 中的用户名和密码
2. 确保特殊字符已正确编码（URL 编码）
3. 在 MongoDB Atlas Database Access 中重置密码

#### 问题：数据库不存在
**解决方案：**
- MongoDB Atlas 会自动创建数据库
- 确保 MONGO_DB_NAME 环境变量设置正确
- 首次写入数据时数据库会自动创建

### 3. 环境变量问题

#### 问题：环境变量未生效
```powershell
# 检查环境变量
vercel env ls

# 确保变量已添加到正确的环境（Production, Preview, Development）
vercel env add MONGODB_URI production

# 重新部署以应用环境变量
vercel --prod
```

#### 问题：本地测试时环境变量未加载
```powershell
# 确保 .env 文件存在
Get-Content .env

# 手动设置环境变量（PowerShell）
$env:MONGODB_URI="your-mongodb-uri"
$env:MONGO_DB_NAME="notetaker_db"

# 或使用测试脚本（会自动加载 .env）
.\test_local_with_atlas.ps1
```

### 4. API 错误

#### 问题：500 Internal Server Error
**可能原因：**
1. MongoDB 连接失败
2. 环境变量未设置
3. 代码错误

**诊断步骤：**
```powershell
# 查看 Vercel 日志
vercel logs

# 查看最近的错误
vercel logs --follow

# 本地复现问题
.\test_local_with_atlas.ps1
```

#### 问题：502 Bad Gateway
**原因：** 函数超时或崩溃

**解决方案：**
1. 检查函数是否在 10 秒内完成（免费计划限制）
2. 查看 Vercel 日志确认具体错误
3. 优化代码性能或升级 Vercel 计划

#### 问题：404 Not Found
**原因：** 路由配置错误

**解决方案：**
1. 检查 `vercel.json` 路由配置
2. 确保 API 路径正确（`/api/notes`）
3. 检查 `api/index.py` 是否正确导入 Flask 应用

### 5. 翻译功能问题

#### 问题：翻译请求失败
**原因：** GITHUB_TOKEN 未设置或无效

**解决方案：**
```powershell
# 检查 token 是否设置
vercel env ls | Select-String "GITHUB_TOKEN"

# 添加或更新 token
vercel env add GITHUB_TOKEN production

# 重新部署
vercel --prod
```

#### 问题：翻译超时
**原因：** LLM API 响应慢或 Vercel 函数超时

**解决方案：**
1. 检查 GitHub Models API 状态
2. 考虑升级 Vercel 计划以获得更长的超时时间
3. 优化翻译请求（减少内容长度）

### 6. CORS 错误

#### 问题：跨域请求被阻止
**解决方案：**
- Flask-CORS 已配置，不应出现此问题
- 如果出现，检查 `src/main.py` 中的 CORS 配置
- 确保前端和后端在同一域名下

### 7. 静态文件问题

#### 问题：index.html 不显示
**检查：**
1. `src/static/index.html` 文件存在
2. `vercel.json` 路由配置正确
3. `api/index.py` 正确导入了 Flask 应用

### 8. 本地测试问题

#### 问题：本地无法连接到 MongoDB Atlas
```powershell
# 运行连接测试
.\test_mongodb_connection.ps1

# 检查防火墙设置
# 确保本地网络可以访问 MongoDB Atlas

# 检查 DNS 解析
nslookup notetaker-note.bqbvigx.mongodb.net
```

#### 问题：Python 模块未找到
```powershell
# 安装所有依赖
pip install -r requirements.txt

# 检查 Python 路径
python -c "import sys; print('\n'.join(sys.path))"
```

## 🛠 诊断工具

### 运行完整测试套件
```powershell
.\run_all_tests.ps1
```

### 测试 MongoDB 连接
```powershell
.\test_mongodb_connection.ps1
```

### 测试 Vercel 部署
```powershell
.\test_vercel_deployment.ps1 https://your-project.vercel.app
```

### 查看 Vercel 日志
```powershell
# 实时日志
vercel logs --follow

# 最近 100 条日志
vercel logs -n 100

# 特定部署的日志
vercel logs <deployment-url>
```

## 📞 获取帮助

### 检查文档
- [Vercel 文档](https://vercel.com/docs)
- [MongoDB Atlas 文档](https://docs.atlas.mongodb.com/)
- [Flask 文档](https://flask.palletsprojects.com/)

### 常用命令
```powershell
# Vercel 项目信息
vercel whoami
vercel ls

# 环境变量管理
vercel env ls
vercel env pull

# 部署管理
vercel deploy --prod
vercel rollback
```

## ✅ 验证清单

完成以下检查以确保一切正常：

- [ ] MongoDB Atlas 网络访问允许 0.0.0.0/0
- [ ] 所有环境变量已在 Vercel 中配置
- [ ] 本地测试通过（`.\run_all_tests.ps1`）
- [ ] Vercel 部署成功
- [ ] API 端点测试通过（`.\test_vercel_deployment.ps1`）
- [ ] 前端页面可以正常访问
- [ ] 可以创建、读取、更新、删除笔记
- [ ] （可选）翻译功能正常工作

## 🚨 紧急问题

如果所有方法都失败：

1. **回滚到上一个版本**
   ```powershell
   vercel rollback
   ```

2. **从头开始**
   ```powershell
   # 删除 Vercel 项目
   vercel remove your-project-name
   
   # 重新部署
   vercel --prod
   ```

3. **检查 Vercel 状态**
   访问 https://www.vercel-status.com/

4. **联系支持**
   - Vercel: https://vercel.com/support
   - MongoDB Atlas: https://support.mongodb.com/
