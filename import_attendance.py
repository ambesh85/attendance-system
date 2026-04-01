import csv
from db import get_db

db = get_db()

# 🔥 CLEAR OLD DATA
db.execute("DELETE FROM attendance")

with open("attendance_all_classes.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    count = 0

    for row in reader:
        db.execute(
            "INSERT INTO attendance (date, roll, name, status, class) VALUES (?, ?, ?, ?, ?)",
            (row["date"], row["roll"], row["name"], row["status"], row["class"]),
        )
        count += 1

db.commit()
db.close()

print(f"✅ {count} records inserted successfully!")