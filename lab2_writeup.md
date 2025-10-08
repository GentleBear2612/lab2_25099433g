## Live Activity Log

All subsequent actions taken while working on this project are recorded below with a timestamp and a short description. Each entry includes the command(s) run (if any), key outputs or results, and recommended next steps. Entries are ordered chronologically.

### Entry 1 — 2025-10-08T00:00:00Z
- Action: Enabled live activity logging in `lab2_writeup.md`.
- Details: Created the "Live Activity Log" section so future automated edits and test results are recorded here.

### Entry 2 — 2025-10-08T00:00:00Z
- Action: Implemented `src/llm.py` per requested OpenAI-client style.
- Details:
  - File: `src/llm.py`
  - Behavior: reads API token from environment (uses `GITHUB_TOKEN` in current implementation), uses `python-dotenv` to load `.env` if present, defines `call_llm_model()` and `translate()` helpers and a small CLI (`--text`, `--to`, `--model`).
  - Security: No API keys are stored in the repository. `.env` is listed in `.gitignore`.
  - How to test locally:
    1. Ensure your shell or `.env` contains a valid token (e.g., `GITHUB_TOKEN` or `OPENAI_API_KEY`) and an appropriate `MODEL_ENDPOINT` if required.
    2. Run: `python -m src.llm --text "Hello" --to Chinese`

### Entry 3 — 2025-10-08T00:00:00Z
- Action: Initial LLM test (diagnostic run).
- Command: `python -m src.llm --text "Hello, how are you?" --to Chinese`
- Result: HTTP 404 from the configured endpoint (`https://models.github.ai/inference`) — server returned "404 page not found".
- Diagnostic notes: Provider endpoints differ. If you see 404, verify `MODEL_ENDPOINT` and the model name; try the provider's documented endpoint (for OpenAI: `https://api.openai.com/v1/chat/completions`).

### Entry 4 — 2025-10-08T00:00:00Z
- Action: Re-ran translation test after endpoint/credentials adjustments.
- Command: `python -m src.llm --text "Hello, how are you?" --to Chinese`
- Result: Success — output: `你好，你怎么样？`
- Notes: The script returned a correct Chinese translation in this environment. I recorded the successful output here. If you'd like, I can commit & push `src/llm.py` and this updated write-up to the remote repository.

### Entry — 2025-10-08T00:50:00Z
- Action: 启用自动记录（在 `lab2_writeup.md` 中直接记录所有后续操作）
- Details:
  - 我已在仓库中添加了一个轻量记录脚本 `scripts/activity_logger.py`，该脚本可以将时间戳条目追加到 `lab2_writeup.md`（脚本路径：`scripts/activity_logger.py`）。
  - 为便捷起见，我现在直接在本文件中记录并保证：在我对仓库进行的每一步修改（创建/编辑文件、运行测试、提交推送等）都会追加一条日志条目到 `lab2_writeup.md`。
  - 条目格式（示例）：

```
### Entry - 2025-10-08T00:50:00Z
- Action: <简短动作标题>
- Details:
  - <详细说明，支持多行和代码块>
```

  - 已记录的相关更改（截至此条目）：
    - 修改：`src/llm.py`（CLI 改进、stdin 支持、错误处理）
    - 新增：`src/routes/note.py` 中的翻译端点 `/api/notes/<id>/translate`
    - 新增：`tests/test_llm.py`（pytest 风格的单元测试）
    - 更新：`README.md`（添加 `src/llm.py` 使用示例）
    - 新增：`scripts/activity_logger.py`（可选的记录器脚本，用于程序化追加条目）

  - 约定：
    1. 我每次在仓库做出修改或运行关键命令后会在本文件追加一条时间戳条目。例：创建/编辑文件、运行测试、提交 git、推送远程、启动/停止服务等。
    2. 如果你希望我在记录中包含命令输出（如测试失败日志、git push 输出等），请明确许可；输出可能包含敏感信息（如远程 URL）—我会在记录中避免写入任何 secret（token/API key 等）。

- Next: 我会在下一次对仓库进行修改（如执行 commit 或运行测试）后，自动追加对应的条目到本文件。如果你确认要我现在将当前未提交的变更提交并记录 commit 日志，请回复“提交并推送”，我将执行并把结果记录在本文件中。

# Lab2 Write-up

## Overview
This document summarizes the recent changes made to the note-taking application (`note-taking-app-updated-GentleBear2612`) as part of Lab2 work. It records what was changed, why, commands used, how the changes were validated, challenges encountered, and lessons learned. Use this as the first draft — you can refine, add screenshots, or expand details later.

## 整理与操作指南（概要）

下面是对本次 Lab2 工作的整理摘要、如何快速复现关键功能、测试状态和后续建议。把这部分当作评分与复现的首要阅读内容。

### 一、关键变更汇总
- 后端：
  - `src/llm.py` — 增强命令行工具：支持 `--token` 覆盖环境变量、支持从 stdin 读取文本、改善错误处理（可读的 RuntimeError）
  - `src/routes/note.py` — 新增翻译 API：`POST /api/notes/<note_id>/translate`，请求体可选 `to`、`model`、`token`，返回 `{ id, translated_content }` 或 `{ error }`。
- 前端：
  - `src/static/index.html` — 在笔记编辑器中加入 `Translate` 按钮（🌐），点击后会调用后端翻译接口并在界面下方显示翻译文本。
- 测试与工具：
  - 新增 `tests/test_llm.py`（pytest 风格）用于验证 `translate()` 行为（包含无 token 抛错与通过 monkeypatch 模拟返回的测试）。
  - 新增 `scripts/activity_logger.py`，可程序化追加活动条目至 `lab2_writeup.md`（可选，记录历史操作）。
- 文档：
  - 更新 `README.md`：增加 `src/llm.py` 的命令行示例（参数、stdin、--token）。

### 二、如何快速运行与复现（推荐步骤）
1. 准备 Python 虚拟环境并安装依赖：

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. 启动后端服务（在项目根目录执行）：

```powershell
python -u src/main.py
```

- 服务将监听 http://localhost:5001。

3. 在浏览器打开 http://localhost:5001，创建/保存一个笔记。保存后在编辑器的动作栏点击 “Translate” 按钮即可触发翻译并在页面下方显示翻译结果。

4. 可以使用命令行直接调用翻译 API（替换 <id> 为笔记 ID）：

```powershell
curl -X POST -H "Content-Type: application/json" -d "{ \"to\": \"English\" }" http://localhost:5001/api/notes/<id>/translate
```

- 若后端需要 API token，请设置环境变量 `GITHUB_TOKEN`（或在请求体中传 `token` 字段覆盖）。

5. 运行单元测试（推荐在虚拟环境）：

```powershell
pip install pytest
pytest -q
```

> 注意：本仓库的 CI/环境可能未预装 `pytest`，本地请先安装。

### 三、当前已知/限制
- 单元测试：`pytest` 未必在运行环境中已安装（我在本地尝试运行时显示找不到 pytest）。请在 CI 或本地环境先安装依赖以运行测试。
- LLM 调用依赖外部服务与有效 token：若未提供有效 `GITHUB_TOKEN`（或 `--token`），`translate()` 会抛出可读的 RuntimeError；此外，不同提供商端点不同，若遇到 404 请检查 `src/llm.py` 中的 `endpoint` 与 `model` 配置。
- 前端 UX：当前翻译结果仅展示在页面，不会自动保存到数据库（如果需要保存翻译建议后端和数据模型需要扩展）。

### 四、下一步建议（优先级排序）
1. 在 CI（GitHub Actions）中添加测试工作流（安装依赖并运行 `pytest`）。
2. 增强前端翻译 UX：添加语言选择下拉、加载状态（禁用按钮/旋转图标）、错误重试。
3. 若需要持久化翻译：为 `Note` 模型添加 `translations` 字段或单独表以保存多语言版本，并在前端添加“保存翻译”按钮。
4. 增加端到端测试（e2e）来覆盖创建笔记 → 翻译 → 展示的用户流程。

## Changes made (summary)
Below are the concrete edits applied to the project and the reasons behind them.

1. Frontend: Add a Clear button and adjust editor behavior
   - File: `src/static/index.html`
   - What changed:
     - Added a new button labeled `Clear` (id: `clearBtn`) in the editor action bar.
     - Added CSS styles for `.btn-clear` to match the UI.
     - Implemented a `clearInputs()` method in the `NoteTaker` class to clear the title and content inputs and show a short success message.
     - Updated event bindings to attach `clearBtn` to `clearInputs()`.
     - Controlled visibility rules for action buttons:
       - When creating a new note: hide the Delete button, show the Clear button.
       - When selecting/viewing an existing note: show the Delete button, hide the Clear button.
       - When hiding the editor: also hide the Clear button.
     - Modified `saveNote()` logic so that when creating a new note (non-auto-save) and the save succeeds, the input fields are cleared and the editor is hidden (this can be changed later if you prefer to keep the editor open).
   - Why:
     - Improve UX: prevent showing Delete for new notes where delete is not relevant and provide a one-click Clear for convenience.
     - Ensure inputs are reset after creating a new note to reduce accidental duplicate or leftover content.

2. Repository maintenance: remove invalid upstream remote
   - Action: Removed the `upstream` remote because it pointed to a non-existing repository and caused extensions/tools to report errors like "repo undefined".
   - Commands used:
     ```powershell
     git remote remove upstream
     git remote -v
     ```
   - Why: avoid tooling errors and confusion from an invalid remote.

3. Project documentation: add plan and writeup draft
   - Files added:
     - `plan.md` — a step-by-step plan for Lab2 (sanity checks, UI verification, tests, CI, README updates).
     - `lab2_writeup.md` — (this file) to capture the changes and lessons.
   - Why: keep a clear record of intended work and completed steps for grading and reproducibility.

4. Backend: Enhance `src/llm.py` CLI and improve project documentation and tests
   - File: `src/llm.py`
   - What changed:
     - Enhanced CLI to support `--token` parameter for API token (overrides `GITHUB_TOKEN`).
     - Added friendly error messages and readable error exits when token is not provided.
     - Added support for reading text to translate from standard input (if `--text` not provided).
     - Improved error handling for external API calls, wrapping exceptions as readable `RuntimeError`.
   - New test file: `tests/test_llm.py`, includes:
     - A test that verifies `RuntimeError` is raised when no env token is present.
     - A test for `translate()` that replaces `call_llm_model` with a mock implementation using monkeypatch (avoids real network requests).
   - Updated `README.md`: Added command-line usage examples for `src/llm.py` (including parameter, stdin pipe, and --token usage examples).
   - Why:
     - Improve usability and flexibility of the translation script, especially in CI or pipeline scenarios.
     - Provide clear documentation and tests to ensure reliability and ease of use.

## Commands executed (selection)
Commands I ran while making and publishing the changes (run from project root):

```powershell
# Check git status
git -C 'd:\note-taking-app-updated-GentleBear2612' status --branch

# Edit and stage a changed file (example)
git add src/static/index.html

git commit -m "Add Clear button and adjust editor behavior for new/existing notes"

git push origin main

# Remove invalid remote
git remote remove upstream
```

## How I validated the changes
- Static verification: Confirmed `src/static/index.html` contains the expected new elements and JavaScript functions.
- Manual smoke test (recommended):
  1. Start the backend: `python -m src.main`.
  2. Open `http://localhost:5001/` in a browser.
  3. Click `New Note` and verify Delete is hidden and Clear is visible.
  4. Type text and click `Clear` to ensure inputs clear and a success message appears.
  5. Create a new note and verify it appears in the left notes list.
  6. Click on an existing note to confirm Delete shows and Clear is hidden.

I performed the code edits and pushed them to GitHub. You can review the live repo here:
https://github.com/COMP5241-2526Sem1/note-taking-app-updated-GentleBear2612

## Challenges encountered
- The `upstream` remote pointed to a non-existent GitHub repository which caused tooling to complain with messages like "repo undefined" or "Repository not found." Solution: removed the remote.
- Some UI behavior choices may be opinionated (e.g., hiding the editor after creating a note). These are easy to change; I noted them in the plan for your approval.
- There was no GitHub CLI available in the environment, so I created and pushed changes using local `git` commands. If automated GitHub actions or repo creation are desired in future, `gh` can simplify the workflow.
- Difficulty: External LLM API endpoints and credentials vary by provider, and default configurations may lead to 404/authentication failures in different environments. Must clarify token source and provide friendly feedback.
- Learned: Adding stdin support and credential override parameters to CLI tools greatly enhances script usability in pipelines and CI environments; using monkeypatch in tests avoids real API calls, making tests stable and fast.

## Lessons learned
- Keep remotes accurate: an invalid remote can confuse IDE extensions and automation.
- Keep front-end logic explicit about UI states (create vs. edit) to avoid surprising button visibility.
- Small UX affordances like a Clear button significantly reduce friction for quick entries.

## Screenshots
(Placeholders — add screenshots manually or tell me and I can capture them locally if you want.)

- Screenshot 1: New Note editor (Clear visible, Delete hidden)
- Screenshot 2: Existing Note selected (Delete visible, Clear hidden)

## Next steps (recommendations)
1. Add automated backend tests using `pytest` (see `plan.md`).
2. Add a GitHub Actions workflow file to run tests on push.
3. Optionally change `saveNote()` behavior for new notes to keep the editor open but clear inputs instead of hiding it — if you prefer that UX.
4. Add README updates describing the new behaviors and how to run tests.

--- 
*Draft created automatically during the Lab2 work. Please review and tell me if you'd like this write-up in Chinese, include screenshots, or have other edits.*

## How to update this write-up
If you want to expand this file with more detail, screenshots, or code snippets, tell me what to add and I will update `lab2_writeup.md` and push the changes.

---

*Draft created automatically during the Lab2 work. Please review and tell me if you'd like this write-up in Chinese, include screenshots, or have other edits.*

### Entry - 2025-10-08T01:20:00Z
- Action: 前端翻译语言选择器（中英互译）
- Details:
  - 在编辑器的操作栏中添加了一个下拉选择框 `#translateTo`，提供两个选项：`中文 → English`（value: `English`）与 `English → 中文`（value: `Chinese`）。
  - `Translate` 按钮现在会读取此选择器的值，并将 `to` 字段随 POST 请求发送到后端 `/api/notes/<id>/translate`。
  - 这些更改位于 `src/static/index.html`，包括样式与 JavaScript 逻辑更新。
  - 使用方式：保存笔记后，在下拉中选择翻译方向，点击 `Translate` 即可在页面下方看到翻译结果。

- Next: 如需我将翻译方向文本国际化或将下拉改为图标切换，我可以继续改进。

### Entry - 2025-10-08T01:35:00Z
- Action: 前端界面优化 — 调整翻译控件位置与可见性
- Details:
  - 把 `Translate` 按钮移到语言选择（`#translateTo`）之前，使按钮在视觉上更突出。
  - 在创建新笔记场景中隐藏翻译控件（按钮与选择器），仅在查看已有笔记或更新已保存笔记时显示翻译功能，避免在无意义的上下文中暴露该功能。
  - 这些更改在 `src/static/index.html` 中实现，包含 JavaScript 控制显示/隐藏逻辑。

- Why: 提高界面清晰性，避免用户在新建/空白笔记时误触翻译功能。

### Entry - 2025-10-08T02:10:00Z
- Action: 将后端数据存储从 SQLite/SQLAlchemy 重构为 MongoDB（PyMongo）并更新相关路由/模型
- Details:
  - 变更的文件：
    - `src/main.py` — 初始化 PyMongo 客户端，使用环境变量 `MONGO_URI` 和 `MONGO_DB_NAME` 来配置并把 db 注入到 `app.config['MONGO_DB']`。
    - `src/models/note.py`、`src/models/user.py` — 将原有 SQLAlchemy 模型替换为简单的文档构造/转换辅助函数（`make_*_doc`, `*_doc_to_dict`）。
    - `src/routes/note.py`、`src/routes/user.py` — 使用 `current_app.config['MONGO_DB']` 的集合进行 CRUD 操作（`notes`, `users`），保持原来的 API 路径不变。
    - `requirements.txt` — 新增 `pymongo` 与 `dnspython`。
  - 运行与配置：
    1. 在 MongoDB Cloud 上创建集群并获得连接字符串（示例：`mongodb+srv://<user>:<pass>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority`）。
    2. 在本地或部署环境设置环境变量：
       - `MONGO_URI` = 你的连接字符串
       - `MONGO_DB_NAME` = 目标数据库名（例如 `notetaker_db`）
    3. 启动服务：

```powershell
venv\Scripts\activate
pip install -r requirements.txt
python -u src/main.py
```

  - 注意事项 & 已知问题：
    - 我已将项目中的 SQLAlchemy 相关模型/依赖替换为 PyMongo 实现，但保留了 `requirements.txt` 中的 SQLAlchemy 行以便回滚或兼容性检查。
    - 需要安装 `pymongo` 才能在本地运行（我在当前环境中未尝试连接实际 MongoDB）。
    - ObjectId 用于文档 ID：API 路径中 `id` 现在为字符串形式的 ObjectId；确保前端/调用方在处理 ID 时使用返回的字符串值。

- Next: 如果你希望我把现有 SQLite 数据迁移到 MongoDB，我可以编写一个小脚本来读取 `database/app.db` 并将数据插入到 MongoDB 集合中（需要你允许访问源数据库文件）。

### Entry - 2025-10-08T02:28:00Z
- Action: 使用提供的 MongoDB 连接串进行连接与 smoke-test（插入并读取临时文档）
- Details:
  - 操作说明：在当前 PowerShell 会话中把 `MONGO_URI` 和 `MONGO_DB_NAME` 设置为会话变量，然后安装依赖并运行 `scripts/mongo_smoke_test.py` 来验证连通性与 CRUD 能力。
  - 命令（已在会话中运行，未把凭证写入仓库）：

```powershell
$env:MONGO_URI = '<redacted - provided by user in chat>'
$env:MONGO_DB_NAME = 'notetaker_db'
pip install -r requirements.txt
python -u .\scripts\mongo_smoke_test.py
```

  - 关键输出（摘录，不包含凭证）：
    - Successfully installed `pymongo` and `dnspython`.
    - Connecting to MongoDB... Using database: notetaker_db
    - Inserted id: 68e643fd02eeba6d267048e9
    - Found document title: smoke-test
    - Deleted test document
  - 注意：运行中出现了一个 Python DeprecationWarning（关于 datetime.datetime.utcnow()），这是测试脚本中使用的时间函数触发的，可在后续脚本中改为使用时区感知的 UTC 时间。

- Result: MongoDB cloud cluster is reachable from this environment and basic CRUD (insert/find/delete) succeeded.

- Next steps (recommendations):
  1. 若要把现有 SQLite 数据迁移到 MongoDB，我可以编写并运行一个迁移脚本（读取 `database/app.db`，将 notes 与 users 写入 MongoDB），但需要你确认并允许访问该文件。建议先备份 SQLite 文件。
  2. 我可以在已连通的 MongoDB 上再执行一次端到端测试：启动 Flask，创建笔记，通过前端 Translate 按钮发起翻译请求并记录完整流程结果到写作里。
  3. 若需要，我可以把 MONGO_URI 写入项目的环境配置（例如 `.env`）但不建议在仓库中提交凭证；更安全的做法是在部署环境/CI 中设置环境变量。

### Entry - 2025-10-08T02:50:00Z
- Action: 运行 SQLite -> MongoDB 迁移脚本（dry-run）
- Details:
  - 命令：`python scripts/migrate_sqlite_to_mongo.py --dry-run`
  - 发现：SQLite (`database/app.db`) 中的记录：
    - notes: 2 条
    - users: 0 条
  - 示例笔记（示例，不含内容字段以保护隐私）： id=1, title='maths'
  - 结论：dry-run 成功读取本地 SQLite 的数据并显示迁移统计，未写入 MongoDB（dry-run 模式）。

- Next: 如果确认，我将执行 `--commit` 模式将这 2 条笔记写入 MongoDB（会在每个插入文档中添加 `sqlite_id` 字段以便追踪）。

### Entry - 2025-10-08T02:58:00Z
- Action: 执行 SQLite -> MongoDB 迁移（--commit）
- Details:
  - 命令：`python scripts/migrate_sqlite_to_mongo.py --commit`
  - 输出摘要：
    - Found 2 notes and 0 users in SQLite
    - Migration report:
      - notes to migrate: 2
      - users to migrate: 0
      - notes inserted: 2
      - users inserted: 0
  - 迁移后验证（通过 `scripts/check_mongo.py`）：
    - notes 集合计数: 2
    - 示例 note title: maths
    - users 集合：未找到

- Notes & recommendations:
  - 已在每个插入的文档中设置 `sqlite_id` 字段以便追踪原始 SQLite ID。
  - 建议在确认无误后备份并（可选）删除或归档原始 SQLite `database/app.db`，以避免数据不一致或重复迁移。
  - 如果你想，我可以删除 `database/app.db` 中已迁移的条目或把其重命名为 `app.db.bak`（会在仓库中记录这一操作）。

### Entry - 2025-10-08T03:20:00Z
- Action: 修复 Windows 上 Flask 开发服务器崩溃（WinError 10038）
- Details:
  - 现象：在开发期间，Flask/Werkzeug 自动重载（reloader）在检测到文件变更时触发线程操作，导致 OSError: [WinError 10038] 在一个非套接字上尝试了一个操作。
  - 修复：在 `src/main.py` 的 `app.run()` 中禁用自动重载，使用 `use_reloader=False`，以避免在 Windows 环境下重复出现该错误。
  - 更改文件：`src/main.py`

- Note: 在生产部署中请使用合适的 WSGI 服务器（例如 Gunicorn/uvicorn），不要使用 Flask 开发服务器。
