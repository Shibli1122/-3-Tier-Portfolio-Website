"""
Database Tier - Python + SQLite
Manages all portfolio data persistence
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "portfolio.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and seed data"""
    conn = get_connection()
    cursor = conn.cursor()

    # Projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            tech_stack TEXT,
            image_url TEXT,
            github_url TEXT,
            live_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Skills table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            level INTEGER DEFAULT 80
        )
    """)

    # Contact messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            sent_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed projects
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        projects = [
            ("E-Commerce Platform", "Full-stack shopping app with cart, auth, and payments.", '["React","Node.js","PostgreSQL"]', "", "https://github.com", "https://example.com"),
            ("AI Chat Dashboard", "Real-time dashboard for monitoring AI conversations.", '["React","Python","WebSockets"]', "", "https://github.com", "https://example.com"),
            ("Portfolio CMS", "A headless CMS built for developers.", '["Next.js","SQLite","REST API"]', "", "https://github.com", "https://example.com"),
            ("Weather Analytics", "Data visualization app for historical weather patterns.", '["D3.js","Flask","SQLite"]', "", "https://github.com", "https://example.com"),
        ]
        cursor.executemany(
            "INSERT INTO projects (title, description, tech_stack, image_url, github_url, live_url) VALUES (?,?,?,?,?,?)",
            projects
        )

    # Seed skills
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        skills = [
            ("React", "Frontend", 90), ("Node.js", "Backend", 85),
            ("Python", "Backend", 88), ("TypeScript", "Frontend", 82),
            ("PostgreSQL", "Database", 78), ("SQLite", "Database", 85),
            ("Docker", "DevOps", 70), ("REST APIs", "Backend", 92),
        ]
        cursor.executemany(
            "INSERT INTO skills (name, category, level) VALUES (?,?,?)",
            skills
        )

    conn.commit()
    conn.close()
    print("✅ Database initialized.")

def get_all_projects():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_skills():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM skills ORDER BY category, level DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_message(name, email, message):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (name, email, message) VALUES (?,?,?)",
        (name, email, message)
    )
    conn.commit()
    conn.close()
    return {"status": "saved", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    init_db()
    print("Projects:", json.dumps(get_all_projects(), indent=2))
    print("Skills:", json.dumps(get_all_skills(), indent=2))
