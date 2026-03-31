from flask import Flask, render_template, request, redirect, session, send_file
import csv
from datetime import datetime
from collections import defaultdict
import io
import os

app = Flask(__name__)
app.secret_key = "secret123"


# 🔹 Load students
def load_students():
    students = []
    with open("students.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(row)
    return students


# 🔹 Check user
def check_user(username, password):
    with open("users.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return True
    return False


# 🔐 Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if check_user(user, pwd):
            session["user"] = user
            return redirect("/dashboard")
        else:
            return "❌ Invalid Credentials"

    return render_template("login.html")


# 🏠 Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    students = load_students()
    total = len(students)

    return render_template("index.html", students=students, total=total)


# 📥 Submit Attendance (FIXED)
@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect("/")

    students = load_students()
    date = datetime.now().strftime("%Y-%m-%d")

    file_exists = os.path.isfile("attendance.csv")

    absentees = []

    with open("attendance.csv", "a", newline="") as file:
        writer = csv.writer(file)

        # ✅ Write header if file is new or empty
        if not file_exists or os.stat("attendance.csv").st_size == 0:
            writer.writerow(["date", "roll", "name", "status"])

        for student in students:
            roll = student["roll"]
            status = request.form.get(roll)

            writer.writerow([date, roll, student["name"], status])

            if status == "Absent":
                absentees.append(student)

    for student in absentees:
        print(f"{student['name']} is absent. Notify: {student['parent_phone']}")

    return redirect("/success")


# ✅ Success
@app.route("/success")
def success():
    if "user" not in session:
        return redirect("/")
    return render_template("success.html")


# 📊 Report (SAFE VERSION)
@app.route("/report")
def report():
    if "user" not in session:
        return redirect("/")

    report_data = defaultdict(lambda: {"present": 0, "absent": 0})

    try:
        with open("attendance.csv", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("name")
                status = row.get("status", "Absent")  # ✅ SAFE

                if not name:
                    continue

                if status == "Present":
                    report_data[name]["present"] += 1
                else:
                    report_data[name]["absent"] += 1
    except FileNotFoundError:
        pass

    return render_template("report.html", report=report_data)


# 📥 Download CSV
@app.route("/download")
def download():
    if "user" not in session:
        return redirect("/")

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Name", "Present", "Absent"])

    report_data = defaultdict(lambda: {"present": 0, "absent": 0})

    try:
        with open("attendance.csv", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("name")
                status = row.get("status", "Absent")

                if not name:
                    continue

                if status == "Present":
                    report_data[name]["present"] += 1
                else:
                    report_data[name]["absent"] += 1
    except FileNotFoundError:
        pass

    for name, data in report_data.items():
        writer.writerow([name, data["present"], data["absent"]])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="attendance_report.csv",
    )


# 🚪 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# 🚀 Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
