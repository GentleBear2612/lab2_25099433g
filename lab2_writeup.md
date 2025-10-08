## Live Activity Log

All subsequent actions taken while working on this project are recorded below with a timestamp and a short description. Each entry includes the command(s) run (if any), key outputs or results, and recommended next steps. Entries are ordered chronologically.

### Entry 1 — 2025-10-08T00:00:00Z
- Action: Enabled live activity logging in `lab2_writeup.md`.
- Details: Created the "Live Activity Log" section so future automated edits and test results are recorded here.

### Entry 2 — 2025-10-08T00:00:00Z
- Action: Implemented `src/llm.py` following an OpenAI-client style.
- Details:
  - File: `src/llm.py`
  - Behavior: reads API token from the environment (uses `GITHUB_TOKEN` in the current implementation), uses `python-dotenv` to load a `.env` file if present, defines `call_llm_model()` and `translate()` helpers and a small CLI (`--text`, `--to`, `--model`).
  - Security: No API keys are stored in the repository. `.env` is included in `.gitignore`.
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
- Action: Enabled automatic logging (append subsequent actions directly to `lab2_writeup.md`).
- Details:
  - I added a lightweight logger script in the repository, `scripts/activity_logger.py`, which can append timestamped entries to `lab2_writeup.md` (script path: `scripts/activity_logger.py`).
  - For convenience, I now record changes directly in this file and guarantee that each modification I make to the repo (create/edit files, run tests, commit/push, etc.) will append a log entry to `lab2_writeup.md`.
  - Entry format (example):

```
### Entry - 2025-10-08T00:50:00Z
- Action: <short action title>
- Details:
  - <detailed notes, code blocks allowed>
```

  - Changes recorded so far (as of this entry):
    - Modified: `src/llm.py` (CLI improvements, stdin support, error handling)
    - Added: translation endpoint in `src/routes/note.py` at `/api/notes/<id>/translate`
    - Added: `tests/test_llm.py` (pytest-style unit tests)
    - Updated: `README.md` (added usage examples for `src/llm.py`)
    - Added: `scripts/activity_logger.py` (optional logger to programmatically append entries)

  - Agreement:
    1. I will append a timestamped entry to this file every time I make a repository change or run an important command (e.g., create/edit files, run tests, git commit, push, start/stop services).
    2. If you want command outputs included in the log (such as failing test logs or git push output), please explicitly permit it; outputs may contain sensitive information (e.g., remote URLs) — I will avoid writing any secrets (tokens/API keys) into the log.

- Next: I will append the corresponding entry to this file after the next repository change (such as a commit or running tests). If you want me to commit and push the currently uncommitted changes now and record the commit log, reply “提交并推送” (commit and push) and I will perform the actions and record the results here.

# Lab2 Write-up

## Overview
This document summarizes the recent changes made to the note-taking application (`note-taking-app-updated-GentleBear2612`) as part of Lab2 work. It records what was changed, why, commands used, how the changes were validated, challenges encountered, and lessons learned. Use this as the first draft — you can refine, add screenshots, or expand details later.

## Organization and Quick Start (Summary)

Below is a concise summary of the Lab2 work, how to quickly reproduce key functionality, test status, and recommendations. Consider this the primary section for grading and reproduction.

### 1. Key Changes
- Backend:
  - `src/llm.py` — Enhanced CLI tool: supports `--token` to override environment variables, supports reading text from stdin, and improved error handling (raises readable RuntimeError).
  - `src/routes/note.py` — Added a translation API: `POST /api/notes/<note_id>/translate`. The request body may include `to`, `model`, and `token`. The endpoint returns `{ id, translated_content }` or `{ error }`.
- Frontend:
  - `src/static/index.html` — Added a `Translate` button (🌐) to the note editor. Clicking it calls the backend translation API and displays the translated text below the editor.
- Tests & Tools:
  - Added `tests/test_llm.py` (pytest-style) to validate `translate()` behavior (including raising when token missing and a monkeypatch-based mock test to avoid real network calls).
  - Added `scripts/activity_logger.py` to optionally programmatically append activity entries to `lab2_writeup.md`.
- Documentation:
  - Updated `README.md` to include command-line examples for `src/llm.py` (parameters, stdin, and `--token`).

### 2. Quick run & reproduction (recommended steps)
1. Prepare a Python virtual environment and install dependencies:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Start the backend server (run from project root):

```powershell
python -u src/main.py
```

- The service will listen on http://localhost:5001.

3. In a browser open http://localhost:5001, create/save a note. After saving, click the "Translate" button in the editor action bar to trigger translation and see the result displayed below the editor.

4. You can call the translation API directly from the command line (replace <id> with the note ID):

```powershell
curl -X POST -H "Content-Type: application/json" -d "{ \"to\": \"English\" }" http://localhost:5001/api/notes/<id>/translate
```

- If the backend requires an API token, set the environment variable `GITHUB_TOKEN` (or include a `token` field in the request body to override).

5. Run unit tests (recommended inside the virtual environment):

```powershell
pip install pytest
pytest -q
```

> Note: The CI/environment for this repo may not have `pytest` pre-installed; please install it locally before running.

### 3. Known limitations / caveats
- Unit tests: `pytest` may not be installed in the running environment (I saw a missing pytest error when I tried locally). Install dependencies in CI or locally to run tests.
- LLM calls depend on external services and a valid token: if no valid `GITHUB_TOKEN` (or `--token`) is provided, `translate()` raises a readable RuntimeError. Different providers use different endpoints; if you see 404, check `src/llm.py` for `endpoint` and `model` configuration.
- Frontend UX: translation results are displayed on the page but are not persisted to the database; if you want translations saved, extend the backend and data model.

### 4. Next recommendations (priority)
1. Add a CI workflow (GitHub Actions) to run tests (install dependencies and run `pytest`).
2. Improve frontend translation UX: add a language selector, loading state (disable button/spinner), and retry on error.
3. If you want to persist translations: add a `translations` field to the `Note` model or a separate collection/table to store multilingual versions and add a "Save translation" button in the frontend.
4. Add end-to-end (e2e) tests covering create note → translate → display flow.

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
- Action: Frontend translation direction selector (Chinese ↔ English)
- Details:
  - Added a dropdown selector `#translateTo` in the editor action bar with two options: `中文 → English` (value: `English`) and `English → 中文` (value: `Chinese`).
  - The `Translate` button now reads the selector value and sends the `to` field with the POST request to the backend `/api/notes/<id>/translate`.
  - These changes are in `src/static/index.html`, including styles and JavaScript logic.
  - Usage: after saving a note, choose the translation direction from the dropdown and click `Translate` to see the translated result below the page.

- Next: If you want the translation direction text internationalized or prefer an icon-based toggle instead of a dropdown, I can implement that.

### Entry - 2025-10-08T01:35:00Z
- Action: Frontend UI refinement — adjust translation control placement and visibility
- Details:
  - Moved the `Translate` button before the language selector (`#translateTo`) to make the button visually more prominent.
  - Hid the translation controls (button and selector) in the "create new note" scenario; they now only appear when viewing or updating an existing saved note to avoid exposing the feature in meaningless contexts.
  - These changes are implemented in `src/static/index.html` and include JavaScript logic to control show/hide behavior.

- Why: Improve UI clarity and prevent users from accidentally invoking translation on empty/new notes.

### Entry - 2025-10-08T02:10:00Z
- Action: Refactored backend storage from SQLite/SQLAlchemy to MongoDB (PyMongo) and updated related routes/models
- Details:
  - Files changed:
    - `src/main.py` — initialize a PyMongo client, use environment variables `MONGO_URI` and `MONGO_DB_NAME` for configuration, and inject the db into `app.config['MONGO_DB']`.
    - `src/models/note.py`, `src/models/user.py` — replaced previous SQLAlchemy models with simple document construction/conversion helpers (`make_*_doc`, `*_doc_to_dict`).
    - `src/routes/note.py`, `src/routes/user.py` — perform CRUD operations on the `notes` and `users` collections using `current_app.config['MONGO_DB']`, keeping the original API paths intact.
    - `requirements.txt` — added `pymongo` and `dnspython`.
  - Running & configuration:
    1. Create a cluster on MongoDB Cloud and obtain a connection string (example: `mongodb+srv://<user>:<pass>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority`).
    2. Set environment variables locally or in your deployment environment:
       - `MONGO_URI` = your connection string
       - `MONGO_DB_NAME` = target database name (e.g., `notetaker_db`)
    3. Start the service:

```powershell
venv\Scripts\activate
pip install -r requirements.txt
python -u src/main.py
```

  - Notes & known issues:
    - I replaced SQLAlchemy-related models/dependencies with a PyMongo implementation but kept the SQLAlchemy line in `requirements.txt` for rollback or compatibility checks.
    - `pymongo` must be installed to run locally (I did not attempt to connect to a real MongoDB from this environment).
    - ObjectId is used for document IDs: the `id` in API paths is now the string form of an ObjectId; ensure the frontend/caller uses the string value returned by the API when handling IDs.

- Next: If you want me to migrate existing SQLite data to MongoDB, I can write a small script to read `database/app.db` and insert data into MongoDB collections (I would need permission to access the source DB file).

### Entry - 2025-10-08T02:28:00Z
- Action: Connected to the provided MongoDB connection string and performed a smoke test (insert & read temporary document)
- Details:
  - Procedure: In the current PowerShell session I set `MONGO_URI` and `MONGO_DB_NAME` as session environment variables, installed dependencies, and ran `scripts/mongo_smoke_test.py` to verify connectivity and basic CRUD.
  - Commands (run in session; credentials were not written to the repo):

```powershell
$env:MONGO_URI = '<redacted - provided by user in chat>'
$env:MONGO_DB_NAME = 'notetaker_db'
pip install -r requirements.txt
python -u .\scripts\mongo_smoke_test.py
```

  - Key output (redacted of credentials):
    - Successfully installed `pymongo` and `dnspython`.
    - Connecting to MongoDB... Using database: notetaker_db
    - Inserted id: 68e643fd02eeba6d267048e9
    - Found document title: smoke-test
    - Deleted test document
  - Note: A Python DeprecationWarning appeared related to datetime.datetime.utcnow(); this is triggered by the test script and can be replaced with timezone-aware UTC timestamps later.

  - Result: MongoDB cloud cluster is reachable from this environment and basic CRUD (insert/find/delete) succeeded.

  - Next steps (recommendations):
  1. To migrate existing SQLite data to MongoDB, I can write and run a migration script (read `database/app.db`, insert notes and users into MongoDB) but I will need your confirmation and access to the file. Back up the SQLite file first.
  2. I can run an end-to-end test on the connected MongoDB: start Flask, create notes, use the frontend Translate button to initiate a translation, and record the full workflow in the write-up.
  3. If desired, I can put `MONGO_URI` into a project environment file (e.g., `.env`) but do not recommend committing credentials to the repo; set them in deployment/CI.

### Entry - 2025-10-08T02:50:00Z
- Action: Ran SQLite -> MongoDB migration script in dry-run mode
- Details:
  - Command: `python scripts/migrate_sqlite_to_mongo.py --dry-run`
  - Discovery: SQLite (`database/app.db`) contains:
    - notes: 2 records
    - users: 0 records
  - Example note (sanitized, content omitted): id=1, title='maths'
  - Conclusion: dry-run successfully read local SQLite data and printed migration statistics without writing to MongoDB (dry-run mode).

- Next: If confirmed, I will run with `--commit` to write these 2 notes to MongoDB (each inserted document will include a `sqlite_id` field for traceability).

### Entry - 2025-10-08T02:58:00Z
- Action: Performed SQLite -> MongoDB migration (`--commit`)
- Details:
  - Command: `python scripts/migrate_sqlite_to_mongo.py --commit`
  - Output summary:
    - Found 2 notes and 0 users in SQLite
    - Migration report:
      - notes to migrate: 2
      - users to migrate: 0
      - notes inserted: 2
      - users inserted: 0
  - Post-migration verification (via `scripts/check_mongo.py`):
    - notes collection count: 2
    - example note title: maths
    - users collection: not found

  - Notes & recommendations:
    - Each inserted document includes a `sqlite_id` field to track the original SQLite ID.
    - After verification, consider backing up and optionally deleting or archiving the original SQLite `database/app.db` to avoid duplication or accidental re-migration.
    - If you want, I can remove migrated records from `database/app.db` or rename the file to `app.db.bak` and record the action in the repo.

### Entry - 2025-10-08T03:20:00Z
- Action: Fixed Flask development server crash on Windows (WinError 10038)
- Details:
  - Symptom: During development, Flask/Werkzeug auto-reloader triggered thread/socket operations when files changed, causing OSError: [WinError 10038] a socket operation was attempted on something that is not a socket.
  - Fix: Disabled the auto-reloader in `app.run()` inside `src/main.py` using `use_reloader=False` to avoid the error on Windows.
  - Files changed: `src/main.py`

  - Note: For production, use a proper WSGI server (e.g., Gunicorn/uvicorn) rather than the Flask development server.
