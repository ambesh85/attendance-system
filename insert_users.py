from db import get_db

db = get_db()

teachers = [
    ("teacher1", "1234", "1"),
    ("teacher2", "1234", "2"),
    ("teacher3", "1234", "3"),
    ("teacher4", "1234", "4"),
    ("teacher5", "1234", "5"),
    ("teacher6", "1234", "6"),
    ("teacher7", "1234", "7"),
    ("teacher8", "1234", "8"),
    ("teacher9", "1234", "9"),
    ("teacher10", "1234", "10"),
    ("admin", "admin", "all"),
]

for t in teachers:
    db.execute("INSERT INTO users (username, password, class) VALUES (?, ?, ?)", t)

db.commit()
db.close()

print("✅ Users inserted successfully!")
