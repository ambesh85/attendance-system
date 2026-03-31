from flask import Flask, render_template, request, redirect, session, send_file
from db import get_db
from datetime import datetime
import csv

app = Flask(__name__)
app.secret_key = "secret123"


# 🔐 LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()

        user_data = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (user, pwd)
        ).fetchone()

        if user_data:
            session["user"] = user_data["username"]
            session["class"] = user_data["class"]
            return redirect("/dashboard")
        else:
            return "❌ Invalid Credentials"

    return render_template("login.html")


# 🏠 DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    teacher_class = session.get("class")

    if teacher_class == "all":
        selected_class = request.form.get("class")
    else:
        selected_class = teacher_class

    if selected_class:
        students = db.execute(
            "SELECT * FROM students WHERE class=?", (selected_class,)
        ).fetchall()
    else:
        students = []

    return render_template(
        "index.html",
        students=students,
        total=len(students),
        selected_class=selected_class,
        teacher_class=teacher_class,
    )


# 📥 SUBMIT (DEFAULT PRESENT)
@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    teacher_class = session.get("class")

    if teacher_class == "all":
        selected_class = request.form.get("class")
    else:
        selected_class = teacher_class

    students = db.execute(
        "SELECT * FROM students WHERE class=?", (selected_class,)
    ).fetchall()

    date = datetime.now().strftime("%Y-%m-%d")
    absent_list = request.form.getlist("absent")

    for student in students:
        roll = str(student["roll"])
        status = "Absent" if roll in absent_list else "Present"

        db.execute(
            "INSERT INTO attendance (date, roll, name, status, class) VALUES (?, ?, ?, ?, ?)",
            (date, roll, student["name"], status, selected_class),
        )

    db.commit()
    return redirect("/success")


# 📊 REPORT WITH GROUPING
@app.route("/report")
def report():
    if "user" not in session:
        return redirect("/")

    db = get_db()

    rows = db.execute("SELECT name, status FROM attendance").fetchall()

    report_data = {}

    for row in rows:
        name = row["name"]
        status = row["status"]

        if name not in report_data:
            report_data[name] = {"present": 0, "absent": 0}

        if status == "Present":
            report_data[name]["present"] += 1
        else:
            report_data[name]["absent"] += 1

    print(report_data)  # 🔥 DEBUG (check terminal)

    return render_template("report.html", report=report_data)


# 📥 DOWNLOAD CSV
@app.route("/download")
def download():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    rows = db.execute("SELECT * FROM attendance").fetchall()

    filename = "attendance_report.csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Roll", "Name", "Status", "Class"])

        for row in rows:
            writer.writerow(
                [row["date"], row["roll"], row["name"], row["status"], row["class"]]
            )

    return send_file(filename, as_attachment=True)


# ✅ SUCCESS
@app.route("/success")
def success():
    return render_template("success.html")


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# 🚀 RUN
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
