from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

utenti = []


@app.route("/")
def home():
    return render_template("form.html")


@app.route("/welcome")
def welcome_page():
    ultimo_utente = utenti[len(utenti) - 1]
    return render_template("welcome.html", p_ultimo=ultimo_utente)


@app.route("/subscribe", methods=["POST"])
def nuovo_utente():
    nome = request.form.get("txt_nome")
    email = request.form.get("txt_email")

    uploaded_file = request.files["file_profilo"]

    # Save file
    uploaded_file.save("static/profile-images/" + uploaded_file.filename)

    nuovo_utente = {"nome": nome, "email": email}

    utenti.append(nuovo_utente)

    return redirect(url_for("welcome_page"))
