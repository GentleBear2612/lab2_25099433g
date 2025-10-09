# 🔍 Vercel 部署调试指南

## 当前状态
- ✅ 构建成功 (Build Completed)
- ❌ 运行时崩溃 (500 FUNCTION_INVOCATION_FAILED)

## 📋 调试步骤

### 1. 等待新部署完成（约 1-2 分钟）

### 2. 查看详细日志

#### 方法 A：访问 Vercel Dashboard
1. 打开 https://vercel.com/dashboard
2. 选择你的项目
3. 点击 **Deployments** 标签
4. 点击最新的部署（顶部的）
5. 点击 **Functions** 标签
6. 点击 **"View Function Logs"** 或点击具体的函数

**查找带有以下前缀的日志：**
- `[Vercel] Step X:` - 看哪一步失败了
- `[MongoDB]` - MongoDB 连接信息
- 错误堆栈 (Traceback)

#### 方法 B：使用调试端点
访问这些 URL 来获取信息：

```
https://你的项目.vercel.app/api/debug
```
这个端点会返回：
- Python 版本
- 环境变量状态
- 文件系统信息
- 当前工作目录

### 3. 常见错误和解决方案

#### 错误 1: ModuleNotFoundError
**症状：** `Step 2-4` 中的某一步失败
```
ModuleNotFoundError: No module named 'flask' (or 'pymongo', 'dotenv')
```

**原因：** requirements.txt 中的依赖未正确安装

**解决：** 检查 Build Logs 中的依赖安装部分

---

#### 错误 2: ImportError: cannot import name 'app'
**症状：** `Step 5` 失败
```
ImportError: cannot import name 'app' from 'src.main'
```

**原因：** src/main.py 执行时出错

**解决：** 查看完整的 traceback，看 src/main.py 中哪一行出错

---

#### 错误 3: pymongo.errors.ServerSelectionTimeoutError
**症状：** 日志中有 MongoDB 连接错误
```
ServerSelectionTimeoutError: ...
```

**原因：** 
- MONGODB_URI 未设置
- MongoDB Atlas Network Access 未配置
- 连接字符串错误

**解决：**
1. 确认 Vercel Environment Variables 中有 MONGODB_URI
2. 确认 MongoDB Atlas Network Access 允许 0.0.0.0/0
3. 检查连接字符串是否正确

---

#### 错误 4: AttributeError: 'NoneType' object has no attribute
**症状：** 尝试访问 None 对象的属性
```
AttributeError: 'NoneType' object has no attribute 'notes'
```

**原因：** MongoDB 客户端为 None

**解决：** 这个已经在最新代码中修复了

---

### 4. 应急测试

如果主应用崩溃，尝试访问调试端点：

```
https://你的项目.vercel.app/api/debug
```

如果这个能工作，说明问题在 src/main.py 的导入或初始化中。

---

## 📊 预期的日志输出

### 成功的日志应该是：
```
[Vercel] Starting initialization...
[Vercel] Python: 3.12.x
[Vercel] Current dir: /var/task/api
[Vercel] Parent dir: /var/task
[Vercel] src dir exists: True
[Vercel] Step 1: Importing os and sys - OK
[Vercel] Step 2: Flask imported - OK
[Vercel] Step 3: dotenv imported - OK
[Vercel] Step 4: pymongo imported - OK
[Vercel] Step 5: src.main imported - OK
[Vercel] Initialization complete!
```

### 如果在某一步失败：
```
[Vercel] Step X: FAILED - <错误信息>
<完整的 Python traceback>
```

---

## 🎯 下一步行动

### 选项 A：等待并查看日志
1. 等待 Vercel 重新部署（约 1-2 分钟）
2. 访问 Vercel Dashboard 查看 Function Logs
3. 找到失败的步骤和错误信息
4. 将错误信息发给我

### 选项 B：测试调试端点
1. 等待部署完成
2. 访问 `https://你的项目.vercel.app/api/debug`
3. 如果能访问，说明 Flask 能工作，问题在主应用
4. 如果不能访问，说明基础环境有问题

### 选项 C：检查环境变量
1. Vercel Dashboard → 项目 → Settings → Environment Variables
2. 确认 `MONGODB_URI` 存在且正确
3. 确认选择了所有环境（Production, Preview, Development）
4. **保存后必须 Redeploy**

---

## 💡 提示

- 日志中的 `[Vercel] Step X` 可以精确定位问题
- 如果看到应急 fallback app 的响应，说明导入失败但错误被捕获了
- Function Logs 是最重要的调试信息来源

---

## 📞 需要帮助？

把以下信息发给我：
1. Vercel Function Logs 的完整内容（特别是带 `[Vercel]` 前缀的部分）
2. 或者 `/api/debug` 端点的返回内容
3. 或者任何错误截图

我会根据具体的错误信息继续修复！
