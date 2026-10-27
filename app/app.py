<<<<<<< HEAD
import os
import time
import psycopg
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def get_connection():
    for attempt in range(10):
        try:
            return psycopg.connect(
                host=os.environ["DB_HOST"],
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=3
            )
        except psycopg.OperationalError:
            if attempt == 9:
                raise
            time.sleep(2)

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}, 200
    except Exception:
        app.logger.exception("Database health check failed")
        return {"status": "degraded", "database": "unavailable"}, 503

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not message or len(name) > 100:
            return "Enter a valid name and message.", 400

        with get_connection() as conn:
            conn.execute(
                "INSERT INTO messages (name, message) VALUES (%s, %s)",
                (name, message)
            )

        return redirect(url_for("index"))

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, message, created_at "
            "FROM messages ORDER BY id DESC LIMIT 100"
        ).fetchall()

    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
=======

>>>>>>> dcb6921dce89c2bd2bec2f8cb0065bd71940e21b
