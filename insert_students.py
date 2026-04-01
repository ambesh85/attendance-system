import csv
from db import get_db

db = get_db()

# CLEAR OLD DATA
db.execute("DELETE FROM students")

with open("attendance_all_classes.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    count = 0

    for row in reader:
        # 🔥 SAFE CLASS CONVERSION
        try:
            student_class = int(float(row["class"])) if row["class"] else None
        except:
            continue  # skip bad rows

        db.execute(
            "INSERT INTO students (roll, name, parent_phone, class) VALUES (?, ?, ?, ?)",
            (row["roll"], row["name"], "", student_class),
        )
        count += 1

db.commit()
db.close()

print(f"✅ {count} students inserted successfully!")
