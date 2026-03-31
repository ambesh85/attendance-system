import csv
from db import get_db

db = get_db()

with open("students.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    count = 0

    for row in reader:
        db.execute(
            "INSERT INTO students (roll, name, parent_phone, class) VALUES (?, ?, ?, ?)",
            (row["roll"], row["name"], row["parent_phone"], row["class"]),
        )
        count += 1

db.commit()
db.close()

print(f"✅ {count} students inserted successfully!")
