from db import get_db

db = get_db()
c = db.cursor()

# USERS TABLE
c.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    class TEXT
)
"""
)

# STUDENTS TABLE
c.execute(
    """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll INTEGER,
    name TEXT,
    parent_phone TEXT,
    class TEXT
)
"""
)

# ATTENDANCE TABLE
c.execute(
    """
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    roll INTEGER,
    name TEXT,
    status TEXT,
    class TEXT
)
"""
)

db.commit()
db.close()

print("✅ Tables created successfully!")
