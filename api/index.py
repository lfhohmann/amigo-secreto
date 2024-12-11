import json
from uuid import uuid4

from flask import Flask, jsonify, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "1234567890"


def db_read():
    with open("db.json", "r") as file:
        return json.load(file)


def db_write(data):
    with open("db.json", "w") as file:
        json.dump(data, file, indent=4)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/code", methods=["POST"])
def code():
    name = request.form["name"]

    # if session.get("name") == name:
    #     return {"status": "Vc ja fez isso!"}

    data = db_read()
    if data[name]["id"]:
        return render_template("error.html")

    id = str(uuid4())
    data[name]["id"] = id
    db_write(data)

    session["name"] = name
    session["id"] = id

    return redirect("/choose")


@app.route("/choose", methods=["GET", "POST"])
def choose():
    if request.method == "GET":
        return render_template("choose.html", name=session["name"], id=session["id"])

    if request.method == "POST":
        data = db_read()

        if data[session["name"]]["people"]:
            return {"status": "Vc ja fez isso!"}

        options = [f"option_{i}" for i in range(1, 6)]
        people = [request.form[option] for option in options]

        data[session["name"]]["people"] = people
        db_write(data)

        return {"status": "DEU BOA!"}


@app.route("/results")
def results():
    data = db_read()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="localhost", port=5432, debug=True)
