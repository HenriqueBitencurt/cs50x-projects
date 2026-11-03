import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///studysync.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Painel principal (Dashboard) do StudySync"""
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? AND status = 'pendente' LIMIT 5", session["user_id"])
    exams = db.execute("SELECT * FROM exams WHERE user_id = ? ORDER BY exam_date ASC LIMIT 5", session["user_id"])

    return render_template("index.html", tasks=tasks, exams=exams)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must provide password confirmation", 400)
        elif password != confirmation:
            return apology("passwords must match", 400)

        hash_pw = generate_password_hash(password)
        try:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw)
        except ValueError:
            return apology("username already exists", 400)

        session["user_id"] = new_user_id
        flash("Registered successfully!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    """Gerir tarefas e trabalhos de casa"""
    if request.method == "POST":
        title = request.form.get("title")
        subject = request.form.get("subject")
        due_date = request.form.get("due_date")

        if not title:
            return apology("must provide task title", 400)
        elif not subject:
            return apology("must provide subject", 400)

        db.execute(
            "INSERT INTO tasks (user_id, title, subject, due_date, status) VALUES (?, ?, ?, ?, 'pendente')",
            session["user_id"], title, subject, due_date
        )

        flash("Task added successfully!")
        return redirect("/tasks")
    else:
        tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC", session["user_id"])
        return render_template("tasks.html", tasks=tasks)


@app.route("/complete_task/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    """Marcar tarefa como concluída ou eliminá-la"""
    task = db.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", task_id, session["user_id"])
    if not task:
        return apology("task not found", 404)

    db.execute("UPDATE tasks SET status = 'concluído' WHERE id = ?", task_id)
    flash("Task marked as completed!")
    return redirect("/tasks")


@app.route("/exams", methods=["GET", "POST"])
@login_required
def exams():
    """Gerir calendário de exames e testes"""
    if request.method == "POST":
        subject = request.form.get("subject")
        exam_date = request.form.get("exam_date")

        if not subject:
            return apology("must provide subject", 400)
        elif not exam_date:
            return apology("must provide exam date", 400)

        db.execute(
            "INSERT INTO exams (user_id, subject, exam_date) VALUES (?, ?, ?)",
            session["user_id"], subject, exam_date
        )

        flash("Exam added successfully!")
        return redirect("/exams")
    else:
        exams = db.execute("SELECT * FROM exams WHERE user_id = ? ORDER BY exam_date ASC", session["user_id"])
        return render_template("exams.html", exams=exams)


@app.route("/delete_exam/<int:exam_id>", methods=["POST"])
@login_required
def delete_exam(exam_id):
    """Apagar um exame da lista"""
    exam = db.execute("SELECT * FROM exams WHERE id = ? AND user_id = ?", exam_id, session["user_id"])
    if not exam:
        return apology("exam not found", 404)

    db.execute("DELETE FROM exams WHERE id = ?", exam_id)
    flash("Exam removed successfully!")
    return redirect("/exams")


@app.route("/grades", methods=["GET", "POST"])
@login_required
def grades():
    """Gerir e calcular notas e avaliações"""
    if request.method == "POST":
        subject = request.form.get("subject")
        assessment_name = request.form.get("assessment_name")
        score = request.form.get("score")
        max_score = request.form.get("max_score")

        if not subject or not assessment_name or not score or not max_score:
            return apology("must fill out all fields", 400)

        try:
            score = float(score)
            max_score = float(max_score)
        except ValueError:
            return apology("scores must be valid numbers", 400)

        if score < 0 or max_score <= 0 or score > max_score:
            return apology("invalid score values", 400)

        db.execute(
            "INSERT INTO grades (user_id, subject, assessment_name, score, max_score) VALUES (?, ?, ?, ?, ?)",
            session["user_id"], subject, assessment_name, score, max_score
        )

        flash("Grade added successfully!")
        return redirect("/grades")
    else:
        grades = db.execute("SELECT * FROM grades WHERE user_id = ?", session["user_id"])
        return render_template("grades.html", grades=grades)
    
@app.route("/delete_grade/<int:grade_id>", methods=["POST"])
@login_required
def delete_grade(grade_id):
    """Apagar um registo de nota"""
    grade = db.execute("SELECT * FROM grades WHERE id = ? AND user_id = ?", grade_id, session["user_id"])
    if not grade:
        return apology("grade not found", 404)

    db.execute("DELETE FROM grades WHERE id = ?", grade_id)
    flash("Grade removed successfully!")
    return redirect("/grades")
