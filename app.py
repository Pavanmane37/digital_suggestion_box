import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "suggestions.db")

app = Flask(__name__)
app.secret_key = "abCD12@#" 


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin@321")

BRANCH = ["CSE", "MECHANICAL", "CIVIL", "ECE", "AIML", "Other"]
STATUSES = ["New", "In Review", "Resolved"]



def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            category TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'New',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Please log in to view the admin dashboard.", "error")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", categories=BRANCH)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    category = request.form.get("category", "").strip()
    message = request.form.get("message", "").strip()

    errors = []
    if not category or category not in BRANCH:
        errors.append("Please choose a valid category.")
    if not message:
        errors.append("Your suggestion can't be empty.")
    elif len(message) > 2000:
        errors.append("Please keep your suggestion under 2000 characters.")

    if errors:
        for e in errors:
            flash(e, "error")
        return render_template(
            "index.html", categories=BRANCH,
            name=name, email=email, category=category, message=message
        )

    conn = get_db()
    conn.execute(
        "INSERT INTO suggestions (name, email, category, message, status, created_at) "
        "VALUES (?, ?, ?, ?, 'New', ?)",
        (name or "Anonymous", email, category, message, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

    return redirect(url_for("thank_you"))


@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["is_admin"] = True
            flash("Welcome back!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Incorrect username or password.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("admin_login"))

@app.route("/admin")
@login_required
def admin_dashboard():
    status_filter = request.args.get("status", "All")
    category_filter = request.args.get("category", "All")
    search = request.args.get("q", "").strip()

    query = "SELECT * FROM suggestions WHERE 1=1"
    params = []

    if status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    if category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    if search:
        query += " AND (message LIKE ? OR name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY created_at DESC"

    conn = get_db()
    rows = conn.execute(query, params).fetchall()
    counts = conn.execute(
        "SELECT status, COUNT(*) as c FROM suggestions GROUP BY status"
    ).fetchall()
    total = conn.execute("SELECT COUNT(*) as c FROM suggestions").fetchone()["c"]
    conn.close()

    count_map = {row["status"]: row["c"] for row in counts}

    return render_template(
        "admin_dashboard.html",
        suggestions=rows,
        categories=BRANCH,
        statuses=STATUSES,
        status_filter=status_filter,
        category_filter=category_filter,
        search=search,
        total=total,
        new_count=count_map.get("New", 0),
        review_count=count_map.get("In Review", 0),
        resolved_count=count_map.get("Resolved", 0),
    )


@app.route("/admin/update-status/<int:suggestion_id>", methods=["POST"])
@login_required
def update_status(suggestion_id):
    new_status = request.form.get("status")
    if new_status in STATUSES:
        conn = get_db()
        conn.execute("UPDATE suggestions SET status = ? WHERE id = ?", (new_status, suggestion_id))
        conn.commit()
        conn.close()
        flash("Status updated.", "success")
    return redirect(request.referrer or url_for("admin_dashboard"))


@app.route("/admin/delete/<int:suggestion_id>", methods=["POST"])
@login_required
def delete_suggestion(suggestion_id):
    conn = get_db()
    conn.execute("DELETE FROM suggestions WHERE id = ?", (suggestion_id,))
    conn.commit()
    conn.close()
    flash("Suggestion deleted.", "success")
    return redirect(request.referrer or url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=False)
