import os
import time
from flask import Flask, jsonify, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-before-public-deployment")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "false").lower() == "true",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 24 * 7,
)

CATALOG = [
    {"id": 1, "title": "The Last Horizon", "category": "Sci-Fi", "year": 2025, "rating": "U/A 13+", "duration": "2h 08m", "description": "When a mysterious signal arrives from beyond the solar system, a small research crew must decide whether humanity is ready to answer.", "poster": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1800&q=90", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", "featured": True},
    {"id": 2, "title": "Midnight in Kyoto", "category": "Drama", "year": 2024, "rating": "U/A 16+", "duration": "1h 54m", "description": "A photographer returns to Kyoto and discovers that the city, and the people she left behind, have changed in unexpected ways.", "poster": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1800&q=90", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"},
    {"id": 3, "title": "Wild Earth", "category": "Documentary", "year": 2025, "rating": "U", "duration": "6 Episodes", "description": "Journey across remarkable landscapes and meet the wildlife adapting to a changing planet.", "poster": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1800&q=90", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"},
    {"id": 4, "title": "The Silent Code", "category": "Thriller", "year": 2025, "rating": "U/A 16+", "duration": "1h 48m", "description": "A cybersecurity analyst finds a hidden message buried in ordinary network traffic—and someone knows she found it.", "poster": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"},
    {"id": 5, "title": "Beyond the Blue", "category": "Adventure", "year": 2024, "rating": "U/A 13+", "duration": "2h 02m", "description": "Two explorers set out across the ocean in search of a legendary island that appears on no map.", "poster": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"},
    {"id": 6, "title": "Neon District", "category": "Action", "year": 2025, "rating": "U/A 16+", "duration": "1h 51m", "description": "In a city that never sleeps, one courier carries a secret that could change everything.", "poster": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"},
    {"id": 7, "title": "A Place to Begin", "category": "Romance", "year": 2023, "rating": "U/A 13+", "duration": "1h 46m", "description": "Two strangers meet during a delayed train journey and discover that the best plans are sometimes unplanned.", "poster": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4"},
    {"id": 8, "title": "Frozen Frontier", "category": "Adventure", "year": 2024, "rating": "U/A 13+", "duration": "1h 59m", "description": "A rescue team races against a fierce winter storm to reach a remote mountain station.", "poster": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"},
    {"id": 9, "title": "The Art of Tomorrow", "category": "Documentary", "year": 2025, "rating": "U", "duration": "52m", "description": "Artists, designers and inventors imagine how creativity will shape the next generation.", "poster": "https://images.unsplash.com/photo-1531058020387-3be344556be6?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1531058020387-3be344556be6?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"},
    {"id": 10, "title": "City of Stories", "category": "Drama", "year": 2023, "rating": "U/A 13+", "duration": "8 Episodes", "description": "Intersecting lives unfold across a vibrant city, where every neighbourhood has a story to tell.", "poster": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"},
    {"id": 11, "title": "Deep Blue", "category": "Documentary", "year": 2024, "rating": "U", "duration": "1h 12m", "description": "Explore the extraordinary ecosystems hidden beneath the ocean surface.", "poster": "https://images.unsplash.com/photo-1518467166778-b88f373ffec7?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1518467166778-b88f373ffec7?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"},
    {"id": 12, "title": "After the Storm", "category": "Thriller", "year": 2025, "rating": "U/A 16+", "duration": "1h 42m", "description": "A quiet coastal town is shaken when a storm reveals evidence of a long-buried mystery.", "poster": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=700&q=85", "backdrop": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1800&q=85", "video": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"}
]

def get_connection():
    for attempt in range(15):
        try:
            return psycopg.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("DB_NAME", "netflix_demo"),
                user=os.getenv("DB_USER", "netflix_user"),
                password=os.getenv("DB_PASSWORD", "change-me"),
                connect_timeout=4,
                row_factory=dict_row
            )
        except psycopg.OperationalError:
            if attempt == 14:
                raise
            time.sleep(2)

def initialize_database():
    """Create/upgrade the demo schema and seed the catalogue."""
    statements = [
        """CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            display_name VARCHAR(100) NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS catalog (
            id INTEGER PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            category VARCHAR(80) NOT NULL,
            year INTEGER NOT NULL,
            rating VARCHAR(30),
            duration VARCHAR(40),
            description TEXT,
            poster TEXT,
            backdrop TEXT,
            video TEXT,
            featured BOOLEAN DEFAULT FALSE
        )""",
        """CREATE TABLE IF NOT EXISTS my_list (
            id SERIAL PRIMARY KEY,
            profile_name VARCHAR(80) NOT NULL DEFAULT 'Aditi',
            movie_id INTEGER NOT NULL REFERENCES catalog(id) ON DELETE CASCADE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(profile_name, movie_id)
        )""",
        """CREATE TABLE IF NOT EXISTS playback_events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            event_type VARCHAR(30) NOT NULL,
            movie_id INTEGER,
            profile_name VARCHAR(80) DEFAULT 'Aditi',
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS service_health (
            id SERIAL PRIMARY KEY,
            service_name VARCHAR(100) NOT NULL,
            status VARCHAR(30) NOT NULL,
            checked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )"""
    ]
    with get_connection() as conn:
        for statement in statements:
            conn.execute(statement)
        for item in CATALOG:
            # Every catalogue record must provide all named SQL parameters.
            # Only the featured hero title is explicitly marked True; all
            # other titles safely default to False.
            item = {**item, "featured": bool(item.get("featured", False))}
            conn.execute("""
                INSERT INTO catalog
                (id,title,category,year,rating,duration,description,poster,backdrop,video,featured)
                VALUES (%(id)s,%(title)s,%(category)s,%(year)s,%(rating)s,%(duration)s,
                        %(description)s,%(poster)s,%(backdrop)s,%(video)s,%(featured)s)
                ON CONFLICT (id) DO UPDATE SET
                  title=EXCLUDED.title, category=EXCLUDED.category, year=EXCLUDED.year,
                  rating=EXCLUDED.rating, duration=EXCLUDED.duration,
                  description=EXCLUDED.description, poster=EXCLUDED.poster,
                  backdrop=EXCLUDED.backdrop, video=EXCLUDED.video, featured=EXCLUDED.featured
            """, item)

@app.get("/")
def index():
    return render_template("index.html")


def current_user():
    """Return the authenticated user's public fields, or None."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, email, display_name FROM users WHERE id=%s",
            (user_id,)
        ).fetchone()


@app.get("/api/auth/me")
def auth_me():
    try:
        user = current_user()
        return jsonify(authenticated=bool(user), user=user)
    except Exception:
        app.logger.exception("Could not read current user")
        return jsonify(error="Authentication service unavailable"), 503


@app.post("/api/auth/register")
def auth_register():
    data = request.get_json(silent=True) or {}
    display_name = str(data.get("name", "")).strip()[:100]
    email = str(data.get("email", "")).strip().lower()[:255]
    password = str(data.get("password", ""))
    if not display_name or not email or not password:
        return jsonify(error="Name, email and password are required."), 400
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return jsonify(error="Enter a valid email address."), 400
    if len(password) < 8:
        return jsonify(error="Password must contain at least 8 characters."), 400
    try:
        with get_connection() as conn:
            user = conn.execute(
                """INSERT INTO users(email, display_name, password_hash)
                   VALUES(%s, %s, %s)
                   ON CONFLICT (email) DO NOTHING
                   RETURNING id, email, display_name""",
                (email, display_name, generate_password_hash(password))
            ).fetchone()
        if not user:
            return jsonify(error="An account with this email already exists. Please sign in."), 409
        session.clear()
        session.permanent = True
        session["user_id"] = user["id"]
        return jsonify(ok=True, user=user), 201
    except Exception:
        app.logger.exception("Registration failed")
        return jsonify(error="Could not create your account. Please try again."), 503


@app.post("/api/auth/login")
def auth_login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    if not email or not password:
        return jsonify(error="Email and password are required."), 400
    try:
        with get_connection() as conn:
            user = conn.execute(
                "SELECT id, email, display_name, password_hash FROM users WHERE email=%s",
                (email,)
            ).fetchone()
        if not user or not check_password_hash(user["password_hash"], password):
            return jsonify(error="Incorrect email or password."), 401
        session.clear()
        session.permanent = True
        session["user_id"] = user["id"]
        return jsonify(
            ok=True,
            user={"id": user["id"], "email": user["email"], "display_name": user["display_name"]}
        )
    except Exception:
        app.logger.exception("Login failed")
        return jsonify(error="Login service unavailable. Please try again."), 503


@app.post("/api/auth/logout")
def auth_logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/health")
@app.get("/api/health")
def health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ok", database="connected", application="Netflix Demo"), 200
    except Exception:
        app.logger.exception("Database health check failed")
        return jsonify(status="degraded", database="unavailable"), 503

@app.get("/api/catalog")
def catalog():
    category = request.args.get("category", "").strip()
    search = request.args.get("q", "").strip()
    with get_connection() as conn:
        if search:
            rows = conn.execute(
                "SELECT * FROM catalog WHERE title ILIKE %s OR category ILIKE %s ORDER BY featured DESC, title",
                (f"%{search}%", f"%{search}%")
            ).fetchall()
        elif category and category.lower() != "all":
            rows = conn.execute(
                "SELECT * FROM catalog WHERE category ILIKE %s ORDER BY featured DESC, title",
                (category,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM catalog ORDER BY featured DESC, id").fetchall()
    return jsonify(rows)

@app.get("/api/my-list")
def get_my_list():
    user = current_user()
    if not user:
        return jsonify(error="Please sign in."), 401
    profile = user["email"][:80]
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT c.* FROM catalog c
            JOIN my_list m ON m.movie_id=c.id
            WHERE m.profile_name=%s ORDER BY m.created_at DESC
        """, (profile,)).fetchall()
    return jsonify(rows)

@app.post("/api/my-list/<int:movie_id>")
def toggle_my_list(movie_id):
    user = current_user()
    if not user:
        return jsonify(error="Please sign in."), 401
    profile = user["email"][:80]
    with get_connection() as conn:
        exists = conn.execute(
            "SELECT id FROM my_list WHERE profile_name=%s AND movie_id=%s",
            (profile, movie_id)
        ).fetchone()
        if exists:
            conn.execute("DELETE FROM my_list WHERE profile_name=%s AND movie_id=%s", (profile, movie_id))
            saved = False
        else:
            conn.execute(
                "INSERT INTO my_list(profile_name,movie_id) VALUES(%s,%s) ON CONFLICT DO NOTHING",
                (profile, movie_id)
            )
            saved = True
    return jsonify(saved=saved, movie_id=movie_id)

@app.post("/api/playback")
def playback():
    user = current_user()
    if not user:
        return jsonify(error="Please sign in."), 401
    data = request.get_json(silent=True) or {}
    movie_id = data.get("movie_id")
    event_type = str(data.get("event_type", "play"))[:30]
    profile = user["email"][:80]
    with get_connection() as conn:
        movie = conn.execute("SELECT id,title FROM catalog WHERE id=%s", (movie_id,)).fetchone()
        if not movie:
            return jsonify(error="Title not found"), 404
        conn.execute(
            "INSERT INTO playback_events(title,event_type,movie_id,profile_name) VALUES(%s,%s,%s,%s)",
            (movie["title"], event_type, movie_id, profile)
        )
    return jsonify(ok=True, title=movie["title"])

@app.get("/api/history")
def history():
    user = current_user()
    if not user:
        return jsonify(error="Please sign in."), 401
    profile = user["email"][:80]
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT DISTINCT ON (movie_id) movie_id,title,event_type,created_at
            FROM playback_events WHERE profile_name=%s
            ORDER BY movie_id, created_at DESC LIMIT 30
        """, (profile,)).fetchall()
    return jsonify(rows)

@app.get("/api/metrics")
def metrics():
    with get_connection() as conn:
        movies = conn.execute("SELECT COUNT(*) AS n FROM catalog").fetchone()["n"]
        saved = conn.execute("SELECT COUNT(*) AS n FROM my_list").fetchone()["n"]
        plays = conn.execute("SELECT COUNT(*) AS n FROM playback_events WHERE event_type='play'").fetchone()["n"]
    return jsonify(catalog_titles=movies, saved_titles=saved, play_events=plays, database="PostgreSQL")

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)
