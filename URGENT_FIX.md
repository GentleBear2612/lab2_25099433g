# 🚨 Vercel 500 错误 - 紧急修复指南

## 当前状况

✅ **本地测试**：所有检查通过  
❌ **Vercel 部署**：显示 500 错误

这说明问题出在 **Vercel 的环境变量配置**上。

---

## 🎯 立即执行这些步骤（5分钟解决）

### 步骤 1️⃣：检查 Vercel 环境变量（最关键！）

1. 打开浏览器，访问：https://vercel.com/dashboard
2. 找到并点击你的项目（项目名可能是 `lab2-25099433g` 或类似）
3. 点击顶部的 **"Settings"** 标签
4. 在左侧菜单点击 **"Environment Variables"**

**检查以下内容：**

```
变量名: MONGO_URI
值: mongodb+srv://zmhlele:zmhlele@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
环境: ✓ Production  ✓ Preview  ✓ Development
```

**⚠️ 常见错误：**
- ❌ 变量名拼写错误（例如写成 `MONGODB_URI`）
- ❌ 只勾选了 Development，没勾选 Production
- ❌ 值中包含了空格或换行符
- ❌ 根本没有添加这个变量

**✅ 正确的样子：**
```
Name:     MONGO_URI
Value:    mongodb+srv://zmhlele:zmhlele@cluster...（你的完整连接字符串）
Environments: 
  [✓] Production
  [✓] Preview  
  [✓] Development
```

### 步骤 2️⃣：添加/修复环境变量

如果 `MONGO_URI` 不存在或配置错误：

1. 点击 **"Add New"** 按钮
2. 在 **"Name"** 输入：`MONGO_URI`
3. 在 **"Value"** 粘贴你的 MongoDB 连接字符串：
   ```
   mongodb+srv://zmhlele:zmhlele@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   （从本地环境变量或 MongoDB Atlas 获取）
4. 在 **"Environment"** 部分，**三个都勾选**：
   - ✅ Production
   - ✅ Preview
   - ✅ Development
5. 点击 **"Save"** 按钮

**可选（但推荐）：**
```
Name:     MONGO_DB_NAME
Value:    notetaker_db
Environments: [✓] Production [✓] Preview [✓] Development
```

### 步骤 3️⃣：重新部署（必须！）

**重要：** 添加或修改环境变量后，**必须重新部署**才能生效！

**方法 A - 通过 Vercel Dashboard（推荐）：**
1. 点击顶部的 **"Deployments"** 标签
2. 找到最新的部署（顶部第一个）
3. 点击右侧的 **三个点菜单 (⋯)**
4. 选择 **"Redeploy"**
5. 在弹出窗口中，确认点击 **"Redeploy"**
6. 等待部署完成（通常需要 1-2 分钟）

**方法 B - 通过 Git 推送：**
```powershell
# 对任何文件做一个小改动（例如在 README 添加一个空行）
git add .
git commit -m "Trigger redeploy"
git push origin 可运行
```

### 步骤 4️⃣：验证修复

部署完成后：

1. 访问你的 Vercel 应用 URL：`https://your-app.vercel.app/api/notes`
2. 你应该看到：
   ```json
   []
   ```
   或者包含笔记的 JSON 数组
3. 如果仍然是 500 错误，继续下一步

### 步骤 5️⃣：查看函数日志（如果仍然失败）

1. 在 Vercel Dashboard，点击最新的部署
2. 点击 **"Functions"** 标签
3. 找到并点击 `/api/notes`
4. 查看日志输出

**查找这些关键信息：**
- 如果看到 `"WARNING: MONGO_URI not set"`：
  - → 环境变量没有正确设置
  - → 回到步骤 1 和 2
  
- 如果看到 `"Unable to connect to MongoDB"`：
  - → MongoDB Atlas 网络访问问题
  - → 继续步骤 6

- 如果看到 `"Authentication failed"`：
  - → 用户名/密码错误
  - → 检查连接字符串中的凭据

### 步骤 6️⃣：检查 MongoDB Atlas 网络访问

1. 访问：https://cloud.mongodb.com
2. 登录你的账号
3. 选择你的集群
4. 点击左侧菜单的 **"Network Access"**
5. 查看 IP Access List

**必须包含：**
```
IP Address: 0.0.0.0/0
Comment: Allow from anywhere
```

**如果没有：**
1. 点击 **"Add IP Address"** 按钮
2. 选择 **"Allow Access from Anywhere"**
3. 或者手动输入：
   - IP Address: `0.0.0.0/0`
   - Comment: `Vercel deployment`
4. 点击 **"Confirm"**
5. 等待几秒钟生效
6. 回到步骤 3 重新部署

---

## 🔍 快速诊断清单

按顺序检查：

- [ ] Vercel 中 `MONGO_URI` 环境变量存在
- [ ] `MONGO_URI` 应用到了 Production 环境
- [ ] 环境变量值正确（以 `mongodb+srv://` 开头）
- [ ] 添加环境变量后已重新部署
- [ ] MongoDB Atlas 允许 0.0.0.0/0 访问
- [ ] 在 Vercel 函数日志中没有看到 "MONGO_URI not set"

---

## 💡 最可能的原因（按概率排序）

### 1. 环境变量未应用到 Production（90%）
- **症状**：本地工作，Vercel 不工作
- **原因**：添加环境变量时只勾选了 Development
- **修复**：步骤 1-2，确保勾选 Production

### 2. 添加环境变量后未重新部署（80%）
- **症状**：刚添加环境变量，但仍然报错
- **原因**：Vercel 需要重新部署才能应用新的环境变量
- **修复**：步骤 3

### 3. MongoDB Atlas 网络访问限制（60%）
- **症状**：连接超时或被拒绝
- **原因**：MongoDB Atlas 默认限制所有 IP
- **修复**：步骤 6

### 4. 变量名拼写错误（30%）
- **症状**：日志显示 "MONGO_URI not set"
- **原因**：变量名写成了 `MONGODB_URI` 或 `MONGO_URL`
- **修复**：删除错误的，添加正确的 `MONGO_URI`

---

## 🆘 仍然不工作？

### 方案 A：使用 Vercel CLI 直接添加环境变量

```powershell
# 安装 Vercel CLI（如果还没有）
npm install -g vercel

# 登录
vercel login

# 在项目目录中
cd d:\lab2_25099433g

# 链接到 Vercel 项目
vercel link

# 添加环境变量
vercel env add MONGO_URI production
# 粘贴你的 MongoDB 连接字符串，按 Enter

# 重新部署
vercel --prod
```

### 方案 B：检查前端配置

如果 API 工作但前端仍然显示错误，检查 `src/static/index.html`：

```javascript
// 确保 API URL 正确
const API_URL = '/api/notes';  // ✅ 正确（相对路径）
// 不要写成：
// const API_URL = 'http://localhost:5000/api/notes';  // ❌ 错误
```

### 方案 C：清除 Vercel 缓存

有时 Vercel 会缓存旧的构建：

1. Vercel Dashboard → Settings → General
2. 滚动到底部
3. 点击 **"Clear Build Cache"**
4. 重新部署

---

## 📊 预期结果

成功后，访问 `https://your-app.vercel.app/api/notes` 应该看到：

```json
[
  {
    "_id": "68e65089cb448aa41b0b3777",
    "title": "Test Note",
    "content": "Test content",
    "created_at": "2025-10-08T18:08:12.848242",
    "updated_at": "2025-10-08T18:08:12.848242",
    "translations": {}
  }
]
```

或者空数组 `[]`（如果数据库是空的）。

---

## 📞 需要更多帮助

1. **查看 Vercel 函数日志**并将错误消息发给我
2. **截图 Vercel 环境变量页面**（隐藏敏感信息）
3. **确认你的 Vercel 项目 URL**

---

**最后提醒：** 99% 的情况是环境变量配置问题。请仔细完成步骤 1-3！
