import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_very_secret_and_random_key_here'
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/submitRequest", methods=["GET", "POST"])
def submitRequest():
    if request.method == "POST":
        name = request.form.get("name")
        food = request.form.get("food")
        additional = request.form.get("additional")
        recipe = request.form.get("recipe")
        anonymous = request.form.get("anonymous")

        if not additional:
            additional = "NULL"

        if not recipe:
            recipe = "NULL"

        if anonymous == "anonymous":
            anonymous = True
        else:
            anonymous = False

        db.execute("INSERT INTO requests (name, food, additional, recipe, anonymous) VALUES (?,?,?,?,?)", name, food, additional, recipe, anonymous)

        # debug: return render_template("debug.html", name=name, food=food, additional=additional, recipe=recipe, anonymous=anonymous)

        return redirect("/viewRequests")

    else:
        return render_template("submitRequest.html")

@app.route("/viewRequests", methods=["GET", "POST"])
def viewRequests():
    if request.method == "POST":
        requestID = request.form.get("upvote")
        sessionKey = "id" + str(requestID)
        if sessionKey not in session:
            session[sessionKey] = False

        if not session[sessionKey]:
            newVotes = int((db.execute("SELECT upvotes FROM requests WHERE id=?", requestID))[0]["upvotes"]) + 1
            db.execute("UPDATE requests SET upvotes=? WHERE id=?", newVotes, requestID)
            session[sessionKey] = True
            return redirect("/viewRequests")
        else:
            return render_template("debug.html", text1="You cannot upvote the same item more than once")

    else:
        requests = db.execute("SELECT id, name, food, upvotes, anonymous FROM requests")
        return render_template("viewRequests.html", requests=requests)

@app.route("/adminLogIn", methods=["GET", "POST"])
def adminLogIn():
    name = request.form.get("name")
    password = request.form.get("password")
    if request.method == "POST":
        if not name:
            return render_template("debug.html", "Warning: invalid username.")
        elif not password:
            return render_template("debug.html", "Warning: invalid password.")
        else:
            if db.execute("SELECT EXISTS (SELECT 1 FROM admins WHERE name=?", name)[0][name]
    else:
        return render_template("adminLogIn.html")
