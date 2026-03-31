from db import get_db

db = get_db()

db.execute("DELETE FROM students")

db.commit()
db.close()

print("✅ Students table cleared!")
