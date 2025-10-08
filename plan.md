# Lab2 Project Implementation Plan

## Objective
Provide a clear implementation and verification plan for the current note-taking application (note-taking-app-updated-GentleBear2612). The plan includes development steps, validation procedures, and deliverables so that I can implement them step by step after you approve.

## Assumptions
- The repository in use is `COMP5241-2526Sem1/note-taking-app-updated-GentleBear2612`.
- Your local environment can run Python (3.10+) and start the Flask application.
- I can create/modify files in the repository and push changes to the remote (you already permitted a previous push).

## Deliverables
- `plan.md` (this file)
- A locally runnable application with verified UI behavior
- Basic automated tests for backend API (smoke tests)
- Minimal CI configuration (GitHub Actions) to run tests on push
- README updates describing how to run, test, and deploy

## High-level Steps (priority order)

1) Sanity checks and setup (5–10 minutes)
   - Confirm branch and clean working tree: `git status --branch`
   - Install Python dependencies: `python -m pip install -r requirements.txt`
   - Start the server: `python -m src.main` (visit `http://localhost:5001/`)
   - Open the page and manually verify basic UI functionality
   - Success criteria: server starts and the page loads without errors

2) Verify and fine-tune frontend behavior (10–30 minutes)
   - Verify: "Delete" button is hidden when creating a new note; "Clear" button is hidden when viewing an existing note; clicking Clear empties inputs; saving a new note behaves as expected.
   - If UI tweaks are needed, make minimal edits to `src/static/index.html` and re-check.
   - Success criteria: UI behaves as intended (manual acceptance)

3) Add minimal automated backend tests (30–60 minutes)
   - Create a `tests/` directory and add `test_api_notes.py` using `pytest` and either `requests` or Flask test client to exercise `/api/notes` (GET/POST/PUT/DELETE).
   - Add `pytest` to `requirements.txt` if not present.
   - Run `pytest` and fix issues until tests pass.
   - Success criteria: core API endpoints are covered and tests pass

4) Add CI via GitHub Actions (15–30 minutes)
   - Add `.github/workflows/ci.yml` that sets up Python on `ubuntu-latest`, installs dependencies, and runs `pytest`.
   - Push and verify the workflow passes on GitHub Actions.
   - Success criteria: pushes trigger the workflow and tests pass

5) Update README (10–20 minutes)
   - Document how to run the app, run tests, and debug.
   - Note the new UI behaviors (Clear/Delete rules)

6) Optional improvements (future)
   - Frontend tests (Playwright or Jest)
   - Additional UX polish and styling
   - Automatic deployment (GitHub Pages, Render, Heroku, etc.)

## Example commands for each step
- Install dependencies:
```powershell
python -m pip install -r requirements.txt
```
- Start the app:
```powershell
python -m src.main
```
- Run backend tests (example):
```powershell
pytest -q
```
- Commit and push changes to `origin/main`:
```powershell
git add .
git commit -m "Implement tests and CI"
git push origin main
```

## Acceptance and delivery
- I will implement tasks in the priority order above: first manual frontend verification and minor fixes, then backend tests, CI, and README updates.
- You may pause or modify the plan at any time by editing this file or asking me to change the plan.

---

Please review the plan and tell me:
- Approve to proceed (I'll start with step 1 and report results), or
- Suggest edits (specify changes) and I will update `plan.md` accordingly.

Once you confirm, I'll begin with step 1 (sanity checks and setup).
