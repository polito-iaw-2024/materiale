from flask import Flask, render_template, request, redirect, url_for

import utenti_dao

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form.html")


@app.route("/welcome")
def welcome_page():
    return render_template("welcome.html")


@app.route("/subscribe", methods=["POST"])
def nuovo_utente():
    nome = request.form.get("txt_nome")
    cognome = request.form.get("txt_cognome")
    email = request.form.get("txt_email")

    utenti_dao.nuovo_utente(nome, cognome, email)

    return redirect(url_for("welcome_page"))