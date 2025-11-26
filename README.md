# Django Bills Project

This repository contains a Django backend and a frontend for a small bills/instalments app.

Repository structure (important top-level folders):

- `bill/` — Django project and app code (backend). Key subfolders include `backend/` which holds `manage.py`, `requirements.txt` and the `bills` app.
- `frontend/` — Frontend application (Vite + React/TypeScript).
- Several virtual environments appear under the workspace for local development.

## Quick setup (Windows — PowerShell)

Open PowerShell and run the following from the repository root (where this README lives):

1) Create and activate a virtual environment (recommended path: `deferit` or any name):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2) Install backend requirements:

```powershell
pip install --upgrade pip; pip install -r bill/backend/requirements.txt
```

3) Apply migrations and create a superuser if needed:

```powershell
cd bill/backend
python manage.py migrate
python manage.py createsuperuser  # optional
```

4) Run the development server:

```powershell
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/ by default.

## Running tests (backend)

From `bill/backend` run:

```powershell
python manage.py test
```

## Frontend (optional)

If you want to run the frontend:

```powershell
cd frontend
# Install dependencies (run once)
npm install
# Start dev server
npm run dev
```

Adjust ports or proxies as needed to connect the frontend to the backend.
