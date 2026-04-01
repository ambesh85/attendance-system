from flask import Flask, render_template, request, redirect, session, send_file
from db import get_db
from datetime import datetime
import csv
import os

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
            "SELECT * FROM students WHERE CAST(class AS INTEGER)=?",
            (int(selected_class),),
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


# 📥 SUBMIT ATTENDANCE
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
        "SELECT * FROM students WHERE CAST(class AS INTEGER)=?", (int(selected_class),)
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


# 📊 DATE-WISE REPORT (ROLE-BASED)
@app.route("/report", methods=["GET", "POST"])
def report():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    teacher_class = session.get("class")

    selected_date = request.form.get("date")

    query = "SELECT * FROM attendance WHERE 1=1"
    params = []

    # 📅 Date filter
    if selected_date:
        query += " AND date=?"
        params.append(selected_date)

    # 🎯 Role-based filter
    if teacher_class != "all":
        query += " AND CAST(class AS INTEGER)=?"
        params.append(int(teacher_class))

    query += " ORDER BY date DESC"

    rows = db.execute(query, params).fetchall()

    # 🔥 Group by date
    report_data = {}

    for row in rows:
        date = row["date"]

        if date not in report_data:
            report_data[date] = []

        report_data[date].append(
            {"roll": row["roll"], "name": row["name"], "status": row["status"]}
        )

    return render_template("report.html", report=report_data)


# 📥 DOWNLOAD CSV (ROLE-BASED)
@app.route("/download")
def download():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    teacher_class = session.get("class")

    query = "SELECT * FROM attendance WHERE 1=1"
    params = []

    # 🎯 Role-based filter
    if teacher_class != "all":
        query += " AND CAST(class AS INTEGER)=?"
        params.append(int(teacher_class))

    rows = db.execute(query, params).fetchall()

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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
