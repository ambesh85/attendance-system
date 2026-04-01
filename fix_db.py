from db import get_db

db = get_db()

# ❌ Drop old table
db.execute("DROP TABLE IF EXISTS students")

# ✅ Create fresh table with INTEGER class
db.execute(
    """
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll INTEGER,
    name TEXT,
    parent_phone TEXT,
    class INTEGER
)
"""
)

db.commit()
db.close()

print("✅ Students table recreated successfully!")
