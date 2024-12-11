import json
import os
from uuid import uuid4

from flask import Flask, jsonify, redirect, render_template, request, session

from api import db

app = Flask(__name__)
app.secret_key = os.getenv("secretkey", "default_secret_key")


def db_read():
    data = db.Data.objects.first().data
    return data


def db_write(data):
    obj = db.Data.objects.first()
    obj.data = data
    obj.save()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/code", methods=["POST"])
def code():
    name = request.form["name"]

    if session.get("name") == name:
        return {"status": "Vc ja fez isso!"}

    obj = db.Data.objects.first()
    data = obj.data

    if data[name]["id"]:
        return {"status": "Vc ja fez isso!"}

    id_ = str(uuid4())
    data[name]["id"] = id_
    obj.data = data
    obj.save()

    session["name"] = name
    session["id"] = id_

    return redirect("/choose")


@app.route("/choose", methods=["GET", "POST"])
def choose():
    if request.method == "GET":
        return render_template("choose.html", name=session["name"], id=session["id"])

    if request.method == "POST":
        obj = db.Data.objects.first()
        data = obj.data

        if data[session["name"]]["people"]:
            return {"status": "Vc ja fez isso!"}

        options = [f"option_{i}" for i in range(1, 6)]
        people = [request.form[option] for option in options]

        data[session["name"]]["people"] = people
        obj.data = data
        obj.save()

        return {"status": "DEU BOA!"}


@app.route("/results")
def results():
    data = db_read()
    return jsonify(data)


@app.route("/reset")
def env():
    session.clear()

    return f"Reset"


if __name__ == "__main__":
    app.run(host="localhost", port=5432, debug=True)
