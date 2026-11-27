# Digital Suggestion Box

Mini-project: a web app where users can submit
suggestions/complaints/ideas, which are stored in a database and reviewed
by an admin through a dashboard.

## Features

- **User page** — a public form to submit a suggestion (name/email
  optional, category required, message required). Includes a live
  character counter and validation.
- **Database** — every suggestion is stored in a local SQLite database
  (`suggestions.db`), created automatically the first time you run the app.
- **Admin dashboard** — a password-protected page where the admin can:
  - See all suggestions with category, status, and timestamp
  - Search by name/keyword, and filter by status or category
  - Update a suggestion's status (New → In Review → Resolved)
  - Delete a suggestion
  - See live counts (total, new, in review, resolved)
- **UI/UX** — a custom "notice board" visual design (not a generic
  template), responsive down to mobile, with clear focus states.

## Tech stack

- **Backend:** Python 3 + Flask
- **Database:** SQLite (via Python's built-in `sqlite3`)
- **Frontend:** Jinja2 templates + plain HTML/CSS/JS (no framework needed)
- **Auth:** Flask sessions + hashed admin password (Werkzeug)

## Project structure

```
digital_suggestion_box/
├── app.py                     # Flask app: routes, DB logic, admin auth
├── requirements.txt
├── suggestions.db             # created automatically on first run
├── templates/
│   ├── base.html               # shared layout, nav, flash messages
│   ├── index.html               # user suggestion form
│   ├── thank_you.html           # confirmation page
│   ├── admin_login.html         # admin login form
│   └── admin_dashboard.html     # admin dashboard
└── static/
    ├── css/style.css            # all styling
    └── js/script.js             # character counter
```

## How to run it

1. **Install dependencies** (Python 3.8+ required):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - User page: http://127.0.0.1:5000/
   - Admin login: http://127.0.0.1:5000/admin/login

4. **Default admin login (for demo/evaluation):**
   - Username: `admin`
   - Password: `admin123`

   Change `ADMIN_USERNAME` and the password passed to `generate_password_hash(...)`
   near the top of `app.py` before using this anywhere beyond a local demo.

## How the database works

On first run, `init_db()` creates a `suggestions` table:

| Column      | Type    | Notes                                   |
|-------------|---------|------------------------------------------|
| id          | INTEGER | Primary key, auto-increment              |
| name        | TEXT    | "Anonymous" if left blank                |
| email       | TEXT    | Optional                                 |
| category    | TEXT    | One of the fixed categories               |
| message     | TEXT    | The suggestion text                      |
| status      | TEXT    | New / In Review / Resolved               |
| created_at  | TEXT    | Timestamp of submission                  |

You can inspect the database directly with any SQLite browser, or via:
```bash
sqlite3 suggestions.db "SELECT * FROM suggestions;"
```

## Ideas for extending this project (good for a viva/demo)

- Add pagination on the admin dashboard for large numbers of suggestions.
- Export suggestions to CSV/PDF from the dashboard.
- Add email notifications when a suggestion is marked "Resolved".
- Add multiple admin accounts with roles (e.g., department-specific admins).
- Deploy it (Render/PythonAnywhere) and swap SQLite for PostgreSQL.
- Add a simple analytics chart (suggestions per category/month).

## Notes for your project report

- **Problem statement:** Colleges often lack a simple, anonymous, digital
  channel for students to raise issues to the administration.
- **Objective:** Build a lightweight web application that lets students
  submit suggestions and lets admins triage and resolve them.
- **Scope:** Single-admin demo scope, suitable as a working prototype;
  see "Ideas for extending" above for how to grow it into a full system.
