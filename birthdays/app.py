import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # 1. Obter os dados enviados pelo formulário
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # 2. Validar se todos os campos foram preenchidos
        if name and month and day:
            # Converter mês e dia para inteiros para garantir segurança
            try:
                month = int(month)
                day = int(day)
                # Inserir o novo aniversário na base de dados
                db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
            except ValueError:
                pass

        # Recarregar a página inicial
        return redirect("/")

    else:

        # 3. Consultar todos os aniversários registados na base de dados
        birthdays = db.execute("SELECT * FROM birthdays")

        # 4. Renderizar a página index.html passando os dados
        return render_template("index.html", birthdays=birthdays)
