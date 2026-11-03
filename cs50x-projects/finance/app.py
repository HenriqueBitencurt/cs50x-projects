import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    rows = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        session["user_id"]
    )

    portfolio = []
    grand_total = 0

    for row in rows:
        stock = lookup(row["symbol"])
        if stock:
            total_value = stock["price"] * row["total_shares"]
            grand_total += total_value
            portfolio.append({
                "symbol": stock["symbol"],
                "name": stock["name"],
                "shares": row["total_shares"],
                "price": stock["price"],
                "total": total_value
            })

    user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = user[0]["cash"]
    grand_total += cash

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol.upper())
        if not stock:
            return apology("invalid symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("shares must be a positive integer", 400)

        total_cost = stock["price"] * shares

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = user_cash[0]["cash"]

        if cash < total_cost:
            return apology("cant afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"], stock["symbol"], shares, stock["price"]
        )

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol.upper())
        if not stock:
            return apology("invalid stock symbol", 400)

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")


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
            new_user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_pw
            )
        except ValueError:
            return apology("username already exists", 400)

        session["user_id"] = new_user_id

        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must select symbol", 400)

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("shares must be a positive integer", 400)

        user_shares = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            session["user_id"], symbol
        )

        if not user_shares or user_shares[0]["total_shares"] < shares:
            return apology("too many shares", 400)

        stock = lookup(symbol)
        total_sale = stock["price"] * shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, session["user_id"])
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"], symbol, -shares, stock["price"]
        )

        flash("Sold!")
        return redirect("/")
    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            session["user_id"]
        )
        return render_template("sell.html", stocks=stocks)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow user to add cash to their account (Personal Touch)."""
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                raise ValueError
        except ValueError:
            return apology("invalid amount", 400)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        flash("Cash added successfully!")
        return redirect("/")
    else:
        return render_template("add_cash.html")
