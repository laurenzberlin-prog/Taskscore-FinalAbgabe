import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "taskscore.db"

WEEKDAYS = ["Montag 💼", "Dienstag 📊", "Mittwoch ⏳", "Donnerstag 🎯", "Freitag 🏁", "Samstag 🕺", "Sonntag 🌿"]


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                weekday TEXT NOT NULL,
                points_total INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'OPEN'
            )
        """)

        try:
            conn.execute("ALTER TABLE tasks ADD COLUMN rewarded INTEGER NOT NULL DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        conn.execute("UPDATE tasks SET rewarded = 0 WHERE rewarded IS NULL")

        try:
            conn.execute("ALTER TABLE tasks ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass

        conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                done_score INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("INSERT OR IGNORE INTO stats (id, done_score) VALUES (1, 0)")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)


def create_user(username, password):
    username = (username or "").strip()
    if len(username) < 3:
        return False, "Benutzername muss mindestens 3 Zeichen haben."
    if len(password) < 4:
        return False, "Passwort muss mindestens 4 Zeichen haben."

    pw_hash = generate_password_hash(password)

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, pw_hash)
            )
        return True, "OK"
    except sqlite3.IntegrityError:
        return False, "Benutzername ist bereits vergeben."


def verify_user(username, password):
    username = (username or "").strip()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    if not row:
        return None

    user_id, pw_hash = row
    return user_id if check_password_hash(pw_hash, password) else None


def get_done_score():
    with get_connection() as conn:
        return conn.execute(
            "SELECT done_score FROM stats WHERE id = 1"
        ).fetchone()[0]


def get_all_tasks(user_id):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT id, title, description, weekday, points_total, status
            FROM tasks
            WHERE user_id = ?
            ORDER BY id ASC
        """, (user_id,)).fetchall()

    return [dict(r) for r in rows]


def insert_task(title, description, weekday, points_total, user_id):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO tasks (title, description, weekday, points_total, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, weekday, points_total, user_id))


def get_total_points(user_id):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT SUM(points_total) FROM tasks WHERE user_id = ?",
            (user_id,)
        ).fetchone()[0]
    return result or 0


def get_done_points(user_id):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT SUM(points_total) FROM tasks WHERE status = 'DONE' AND user_id = ?",
            (user_id,)
        ).fetchone()[0]
    return result or 0


def get_weekly_points(user_id):
    weekly = {day: 0 for day in WEEKDAYS}

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT weekday, SUM(points_total)
            FROM tasks
            WHERE user_id = ?
            GROUP BY weekday
        """, (user_id,)).fetchall()

    for weekday, total in rows:
        if weekday in weekly:
            weekly[weekday] = total or 0

    return weekly


def toggle_task_status(task_id, user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT status, rewarded FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()

        if not row:
            return

        status, rewarded = row
        new_status = "DONE" if status != "DONE" else "OPEN"

        conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?",
            (new_status, task_id, user_id)
        )

        if new_status == "DONE" and (rewarded is None or rewarded == 0):
            conn.execute(
                "UPDATE tasks SET rewarded = 1 WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            conn.execute(
                "UPDATE stats SET done_score = done_score + 1 WHERE id = 1"
            )


def delete_task(task_id, user_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )

def get_done_task_count(user_id):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE status = 'DONE' AND user_id = ?",
            (user_id,)
        ).fetchone()[0]
    return result or 0