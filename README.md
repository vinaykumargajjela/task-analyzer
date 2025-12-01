# Task Analyzer

Simple Django + static frontend project that analyzes tasks and returns a prioritized list.

## Overview

This repository contains a small Django backend and a static frontend (HTML/CSS/JS). The frontend posts a JSON array of tasks to the backend API at `/api/tasks/analyze/`. The backend computes a numeric `score` for each task (based on due date, importance, and estimated hours) and returns the tasks sorted by priority.

## Prerequisites

- Python 3.8+ (3.13 used in dev)
- pip
- (optional) Git

## Recommended quick setup (Windows PowerShell)

1. Open PowerShell, change to the project folder:

```powershell
cd "C:\Users\USER\Downloads\task-analyzer"
```

2. (Optional) Create a venv if one is not present:

```powershell
python -m venv venv
```

3. Activate the virtual environment:

```powershell
& .\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run once (as admin) and then re-run activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

4. Install dependencies. If you have a `requirements.txt` (this repo may include one), run:

```powershell
pip install -r requirements.txt
```

Or install the essentials directly:

```powershell
pip install django django-cors-headers
```

5. Apply migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server:

```powershell
python manage.py runserver 127.0.0.1:8000
```

7. Open the app in your browser:

```
http://127.0.0.1:8000/
```

## API

- `POST /api/tasks/analyze/` - Accepts a JSON array of task objects and returns a sorted array with added `score` values.

Task object example:

```json
{
  "title": "Fix Bug",
  "due_date": "2025-12-01",
  "importance": 8,
  "estimated_hours": 2
}
```

Example curl request:

```bash
curl -X POST "http://127.0.0.1:8000/api/tasks/analyze/" -H "Content-Type: application/json" -d '[{"title":"Fix Bug","due_date":"2025-12-01","importance":8,"estimated_hours":2}]'
```

## Development notes

- The backend uses `django-cors-headers` for local development; `CORS_ALLOW_ALL_ORIGINS=True` is enabled in settings for convenience. Do NOT use this configuration in production.
- Static files are served at `/static/` during development. The frontend files live in the `frontend/` folder.
- The scoring logic is in `tasks/scoring.py` and the API view is `tasks/views.py`.

## Troubleshooting

- If static files 404: ensure the server was restarted after settings changes and that `STATIC_URL` is `/static/`.
- If the server fails to start because port is in use, run with a different port:

```powershell
python manage.py runserver 127.0.0.1:8001
```

- If you get CORS errors while developing the frontend separately, ensure the backend allows your frontend origin or set `CORS_ALLOWED_ORIGINS` appropriately.

## Next steps (optional)

- Add a `requirements.txt` pinned with current package versions (`pip freeze > requirements.txt`).
- Add tests for `tasks.scoring.calculate_task_score`.

If you want, I can add a `requirements.txt` and a short test or a visible raw-JSON panel in the UI — tell me which and I'll implement it.
