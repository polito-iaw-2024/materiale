from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/loop")
def print_items():
    items = ["Apple", "Banana", "Orange"]
    return render_template("loop.html", p_items=items)


@app.route("/conditional")
def print_if():
    return render_template("conditional.html", p_user="Juan")