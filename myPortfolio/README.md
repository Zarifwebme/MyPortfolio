# Portfolio Web Application (Flask + SQLite + Bootstrap)

Production-ready personal portfolio with REST API, admin panel, and Bootstrap frontend. Deployable to Railway.

## Quickstart

1. Create virtualenv and install dependencies:

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Create `.env` from example and set values:

```bash
cp .env.example .env
```

3. Run locally:

```bash
# from project root
$env:FLASK_APP="backend.app:create_app()"
python -m flask run --debug
```

4. Deploy to Railway: push repo and Railway will use `Procfile` with gunicorn.

- SQLite lives in `instance/portfolio.db`
- Logs in `instance/app.log`

## API
- `/api/projects`, `/api/skills`, `/api/contact`, `/api/blogs`, `/api/categories`
- Full CRUD on each, JSON responses
- GitHub repos proxy: `/api/github/repos?username=<optional>`

## Admin
- `/admin/login`, `/admin/logout`, `/admin` dashboard
- CRUD pages for Projects, Skills, Contact, Blogs, Blog Categories

## Frontend
- Static pages in `frontend/` using Bootstrap and fetch API
