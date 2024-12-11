from flask import Flask, redirect, request, session

app = Flask(__name__)


@app.route("/")
def home():
    return f"amigo secreto"


if __name__ == "__main__":
    app.run(host="localhost", port=5432, debug=True)
