import os

# from cs50 import SQL
from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql import text

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
# db = SQL("sqlite:///project.db")
db = 'sqlite:///project.db'
meta = MetaData()
conn = engine.connect()

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

        if not name:
            return render_template("debug.html", text1="invalid name.")
        elif not food:
            return render_template("debug.html", text1="invalid food.")
        else:
            if not additional:
                additional = "NULL"
            if not recipe:
                recipe = "NULL"
            if anonymous == "anonymous":
                anonymous = True
            else:
                anonymous = False
            db.execute("INSERT INTO requests (name, food, additional, recipe, anonymous) VALUES (?,?,?,?,?)", name, food, additional, recipe, anonymous)
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
    if "admin" not in session:
        name = request.form.get("name")
        password = request.form.get("password")
        if request.method == "POST":
            if not name:
                return render_template("debug.html", text1="invalid username.")
            elif not password:
                return render_template("debug.html", text1="invalid password.")
            else:
                if db.execute("SELECT COUNT(*) AS n FROM admins WHERE name=?", name)[0]["n"] == 1:
                    if db.execute("SELECT password FROM admins WHERE name=?", name)[0]["password"] == password:
                        session["admin"] = True
                        return render_template("editRequests.html")
                    else:
                        return render_template("debug.html", text1="invalid password.")
                else:
                    return render_template("debug.html", text1="invalid username.")
        else:
            return render_template("adminLogIn.html")
    elif session["admin"] == True:
        return redirect("/editRequests")

@app.route("/addAdmin", methods=["GET", "POST"])
def addAdmin():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        adminKey = request.form.get("adminKey")
        correctAdminKey = "pikafoodAdminHuhu"
        # return render_template("debug.html", text1=[name, password, adminKey])
        if not name:
            return render_template("debug.html", text1="invalid username.")
        elif not password:
            return render_template("debug.html", text1="invalid password.")
        elif not adminKey or adminKey != correctAdminKey:
            return render_template("debug.html", text1="invalid admin key.")
        else:
            if db.execute("SELECT COUNT(*) AS n FROM admins WHERE name=?", name)[0]["n"] != 0:
                return render_template("debug.html", text1="duplicate username.")
            else:
                db.execute("INSERT INTO admins (name, password) VALUES (?,?)", name, password)
                return redirect("/addAdmin")
    else:
        return render_template("addAdmin.html")

@app.route("/editRequests", methods=["GET", "POST"])
def editRequests():
    if request.method == "POST":
        removeRequest = request.form.get("removeRequest")
        finishRequest = request.form.get("finishRequest")
        if removeRequest:
            db.execute("DELETE FROM requests WHERE id=?", removeRequest)
        if finishRequest:
            finishedRequest = db.execute("SELECT id, name, food, additional, recipe, anonymous, upvotes FROM requests WHERE id=?", finishRequest)[0]
            if finishedRequest:
                db.execute("INSERT INTO finished (requestID, name, food, additional, recipe, anonymous, upvotes) VALUES (?,?,?,?,?,?,?)", finishedRequest["id"], finishedRequest["name"], finishedRequest["food"], finishedRequest["additional"], finishedRequest["recipe"], finishedRequest["anonymous"], finishedRequest["upvotes"])
                db.execute("DELETE FROM requests WHERE id=?", finishRequest)
        return redirect("/editRequests")
    elif request.method == "GET":
        requests = db.execute("SELECT id, name, food, upvotes, anonymous, additional, recipe FROM requests")
        finished = db.execute("SELECT requestID, food, name, anonymous, upvotes, additional, recipe FROM finished")
        comments = db.execute("SELECT * FROM comments")
        return render_template("editRequests.html", requests=requests, finished=finished, comments=comments)

@app.route("/viewFinished", methods=["GET", "POST"])
def viewFinished():
    finished = db.execute("SELECT requestID, name, food, anonymous, upvotes, rating FROM finished")
    return render_template("viewFinished.html", finished=finished)

@app.route("/rateComment", methods=["GET", "POST"])
def rateComment():
    if request.method == "POST":
        requestNumber = request.form.get("requestNumber")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        if db.execute("SELECT COUNT(*) AS n FROM finished WHERE requestID=?", requestNumber)[0]["n"] == 0:
            return render_template("debug.html", text1="invalid request number.")
        elif not rating and not comment:
            return render_template("debug.html", text1="please provide a valid rating or comment.")
        else:
            if rating:
                currentRating = db.execute("SELECT rating FROM finished WHERE requestID=?", requestNumber)[0]["rating"]
                ratingCount = db.execute("SELECT ratingCount FROM finished WHERE requestID=?", requestNumber)[0]["ratingCount"]
                if currentRating == None:
                    newRating = rating
                else:
                    newRating = round((int(currentRating)*int(ratingCount) + int(rating))/(int(ratingCount)+1), 1)
                db.execute("UPDATE finished SET rating=? WHERE requestID=?", newRating, requestNumber)
                db.execute("UPDATE finished SET ratingCount=? WHERE requestID=?", ratingCount+1 ,requestNumber)
            if comment:
                db.execute("INSERT INTO comments (requestID, comment) VALUES (?,?)", requestNumber, comment)
            return redirect("/viewFinished")
    else:
        return render_template("rateComment.html")

if __name__ == "__main__":
    app.run(debug=True)
