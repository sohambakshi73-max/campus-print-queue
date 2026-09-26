import os
import sqlite3
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
DB_NAME = os.getenv("DATABASE_PATH", "print_queue.db")
COMMIT = os.getenv("RENDER_GIT_COMMIT", "local")[:7]


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS print_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_name TEXT NOT NULL,
            student_name TEXT NOT NULL,
            pages INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Queued',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM print_jobs ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", jobs=jobs, commit=COMMIT)


@app.route("/submit", methods=["POST"])
def submit_job():
    doc_name = request.form.get("doc_name", "").strip()
    student_name = request.form.get("student_name", "").strip()
    pages_raw = request.form.get("pages", "").strip()

    if not doc_name or not student_name or not pages_raw.isdigit():
        return "Document name, student name, and a valid page count are required", 400

    pages = int(pages_raw)
    if pages <= 0:
        return "Page count must be greater than 0", 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO print_jobs (doc_name, student_name, pages, status) VALUES (?, ?, ?, ?)",
        (doc_name, student_name, pages, "Queued"),
    )
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/ready/<int:job_id>", methods=["POST"])
def mark_ready(job_id):
    conn = get_db_connection()
    conn.execute("UPDATE print_jobs SET status = 'Ready for Pickup' WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/api/jobs")
def api_jobs():
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM print_jobs").fetchall()
    conn.close()
    return jsonify([dict(j) for j in jobs])


@app.route("/health")
def health():
    return {"status": "ok", "commit": COMMIT}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)