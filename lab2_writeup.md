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
# Lab2 Write-up

## Overview
This document summarizes the recent changes made to the note-taking application (`note-taking-app-updated-GentleBear2612`) as part of Lab2 work. It records what was changed, why, commands used, how the changes were validated, challenges encountered, and lessons learned. Use this as the first draft — you can refine, add screenshots, or expand details later.

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
