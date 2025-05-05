from flask import Flask, render_template, request, redirect, url_for

import utenti_dao

app = Flask(__name__)

lista = [
    {
        "id": 0,
        "nome": "Aula 1",
        "descrizione": "Descrizione Aula 1",
        "capienza": 50,
        "img": "images/aula-1.jpg",
    },
    {
        "id": 1,
        "nome": "Aula 2",
        "descrizione": "Descrizione Aula 2",
        "capienza": 20,
        "img": "images/aula-2.jpg",
    },
    {
        "id": 2,
        "nome": "Aula 3",
        "descrizione": "Descrizione Aula 3",
        "capienza": 100,
        "img": "images/aula-3.jpg",
    },
]


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/aule")
def aule():
    return render_template("aule.html", p_aule=lista)


@app.route("/aule/<int:id_aula>")
def aula_singolare(id_aula):
    aula_selezionata = lista[id_aula]
    return render_template("aula.html", p_aula=aula_selezionata)


@app.route("/signup")
def signup():
    return render_template("sign-up.html")


@app.route("/subscribe", methods=["POST"])
def nuovo_utente():
    nome = request.form.get("txt_nome")
    cognome = request.form.get("txt_cognome")
    email = request.form.get("txt_email")

    utenti_dao.nuovo_utente(nome, cognome, email)

    return redirect(url_for("home"))


@app.route("/prenotare")
def prenotazione():
    lista_id_nome = [{"id": item["id"], "nome": item["nome"]} for item in lista]
    return render_template("prenotazione.html", p_aule=lista_id_nome)
