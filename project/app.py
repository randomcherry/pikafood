import os
from sqlalchemy import create_engine, text
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_very_secret_and_random_key_here'
Session(app)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure SQLAlchemy engine
engine = create_engine("sqlite:///project.db", echo=True, future=True)
conn = engine.connect()

@app.after_request
def after_request(response):
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
        additional = request.form.get("additional") or "NULL"
        recipe = request.form.get("recipe") or "NULL"
        anonymous = request.form.get("anonymous") == "anonymous"

        if not name:
            return render_template("debug.html", text1="invalid name.")
        elif not food:
            return render_template("debug.html", text1="invalid food.")
        else:
            conn.execute(
                text("INSERT INTO requests (name, food, additional, recipe, anonymous) VALUES (:name, :food, :additional, :recipe, :anonymous)"),
                {"name": name, "food": food, "additional": additional, "recipe": recipe, "anonymous": anonymous}
            )
            conn.commit()
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
            row = conn.execute(text("SELECT upvotes FROM requests WHERE id=:id"), {"id": requestID}).mappings().first()
            newVotes = int(row["upvotes"]) + 1
            conn.execute(text("UPDATE requests SET upvotes=:upvotes WHERE id=:id"), {"upvotes": newVotes, "id": requestID})
            conn.commit()
            session[sessionKey] = True
            return redirect("/viewRequests")
        else:
            return render_template("debug.html", text1="You cannot upvote the same item more than once")
    else:
        requests = conn.execute(text("SELECT id, name, food, upvotes, anonymous FROM requests")).mappings().all()
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
                count = conn.execute(text("SELECT COUNT(*) AS n FROM admins WHERE name=:name"), {"name": name}).mappings().first()
                if count["n"] == 1:
                    pw = conn.execute(text("SELECT password FROM admins WHERE name=:name"), {"name": name}).mappings().first()
                    if pw["password"] == password:
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

        if not name:
            return render_template("debug.html", text1="invalid username.")
        elif not password:
            return render_template("debug.html", text1="invalid password.")
        elif not adminKey or adminKey != correctAdminKey:
            return render_template("debug.html", text1="invalid admin key.")
        else:
            count = conn.execute(text("SELECT COUNT(*) AS n FROM admins WHERE name=:name"), {"name": name}).mappings().first()
            if count["n"] != 0:
                return render_template("debug.html", text1="duplicate username.")
            else:
                conn.execute(text("INSERT INTO admins (name, password) VALUES (:name, :password)"), {"name": name, "password": password})
                conn.commit()
                return redirect("/addAdmin")
    else:
        return render_template("addAdmin.html")

@app.route("/editRequests", methods=["GET", "POST"])
def editRequests():
    if request.method == "POST":
        removeRequest = request.form.get("removeRequest")
        finishRequest = request.form.get("finishRequest")
        removeFinished = request.form.get("removeFinished")
        if removeRequest:
            conn.execute(text("DELETE FROM requests WHERE id=:id"), {"id": removeRequest})
            conn.commit()
        if finishRequest:
            finishedRequest = conn.execute(text("SELECT id, name, food, additional, recipe, anonymous, upvotes FROM requests WHERE id=:id"), {"id": finishRequest}).mappings().first()
            if finishedRequest:
                conn.execute(
                    text("INSERT INTO finished (requestID, name, food, additional, recipe, anonymous, upvotes) VALUES (:id, :name, :food, :additional, :recipe, :anonymous, :upvotes)"),
                    finishedRequest
                )
                conn.execute(text("DELETE FROM requests WHERE id=:id"), {"id": finishRequest})
                conn.commit()
        if removeFinished:
            conn.execute(text("DELETE FROM finished WHERE requestID=:id"), {"id": removeFinished})
            conn.commit()
        return redirect("/editRequests")
    elif request.method == "GET":
        requests = conn.execute(text("SELECT id, name, food, upvotes, anonymous, additional, recipe FROM requests")).mappings().all()
        finished = conn.execute(text("SELECT requestID, food, name, anonymous, upvotes, additional, recipe FROM finished")).mappings().all()
        comments = conn.execute(text("SELECT * FROM comments")).mappings().all()
        return render_template("editRequests.html", requests=requests, finished=finished, comments=comments)

@app.route("/viewFinished", methods=["GET", "POST"])
def viewFinished():
    finished = conn.execute(text("SELECT requestID, name, food, anonymous, upvotes, rating FROM finished")).mappings().all()
    return render_template("viewFinished.html", finished=finished)

@app.route("/rateComment", methods=["GET", "POST"])
def rateComment():
    if request.method == "POST":
        requestNumber = request.form.get("requestNumber")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        count = conn.execute(text("SELECT COUNT(*) AS n FROM finished WHERE requestID=:id"), {"id": requestNumber}).mappings().first()
        if count["n"] == 0:
            return render_template("debug.html", text1="invalid request number.")
        elif not rating and not comment:
            return render_template("debug.html", text1="please provide a valid rating or comment.")
        else:
            if rating:
                row = conn.execute(text("SELECT rating, ratingCount FROM finished WHERE requestID=:id"), {"id": requestNumber}).mappings().first()
                currentRating = row["rating"]
                ratingCount = row["ratingCount"]
                if currentRating is None:
                    newRating = int(rating)
                else:
                    newRating = round((int(currentRating) * int(ratingCount) + int(rating)) / (int(ratingCount) + 1), 1)
                conn.execute(text("UPDATE finished SET rating=:rating, ratingCount=:count WHERE requestID=:id"),
                             {"rating": newRating, "count": ratingCount + 1, "id": requestNumber})
                conn.commit()
            if comment:
                conn.execute(text("INSERT INTO comments (requestID, comment) VALUES (:id, :comment)"),
                             {"id": requestNumber, "comment": comment})
                conn.commit()
            return redirect("/viewFinished")
    else:
        return render_template("rateComment.html")

if __name__ == "__main__":
    app.run(debug=True)
