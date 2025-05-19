from flask import Flask, render_template, request, redirect, url_for

#Account di test credenziali nome: Test, cognome: Test, mail: test@test.test, password: testtest per chiunque voglia provare

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from models import User

import studenti_dao, aule_dao, fasce_orarie_dao, prenotazioni_dao

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "Chiave para c'è posto"

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/aule")
@login_required
def aule():
    lista_aule_db = aule_dao.get_aule()
    return render_template("aule.html", p_aule=lista_aule_db)

@app.route("/aule/<int:id_aula>")
def aula_singolare(id_aula):
    aula_selezionata = aule_dao.get_aula(id_aula)
    return render_template("aula.html", p_aula=aula_selezionata)


@app.route("/signup")
def signup():
    return render_template("sign-up.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/subscribe", methods=["POST"])
def nuovo_utente():
    nome = request.form.get("txt_nome")
    cognome = request.form.get("txt_cognome")
    email = request.form.get("txt_email")
    password_form = request.form.get("txt_password")

    password_con_hash = generate_password_hash(password_form)

    studenti_dao.nuovo_utente(nome, cognome, email, password_con_hash)

    return redirect(url_for("home"))


@app.route("/autenticare", methods=["POST"])
def autenticare_utente():

    utente_form = request.form.to_dict()
    utente_db = studenti_dao.get_user_by_email(utente_form["txt_email"])

    if not utente_db or not check_password_hash(
        utente_db["password"], utente_form["txt_password"]
    ):
        print("Credenziali non valide")
        return redirect(url_for("home"))
    else:
        new = User(
            id=utente_db["id"],
            nome=utente_db["nome"],
            cognome=utente_db["cognome"],
            email=utente_db["email"],
            password=utente_db["password"],
        )

        login_user(new)

        return redirect(url_for("home"))


@app.route("/prenotazione")
@login_required
def prenotazione():
    aule = aule_dao.get_aule()
    fasce_orarie_disponibili = fasce_orarie_dao.get_fasce_orarie()
    return render_template("prenotazione.html", p_aule = aule, p_fasce = fasce_orarie_disponibili)

@app.route("/prenotare", methods=["POST"])
@login_required
def prenotare():
    prenotazione_form = request.form.to_dict()

    fascia_oraria_form = prenotazione_form.get("select_fascia_oraria")
    aula_form = prenotazione_form.get("select_aula")
    data_form = prenotazione_form.get("txt_date")
    
    prenotazioni_dao.prenotare_aula(current_user.id, aula_form, 1, data_form, fascia_oraria_form)

    return redirect(url_for("home"))
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):
    db_user = studenti_dao.get_user_by_id(user_id)
    if db_user is not None:
        user = User(
            id=db_user["id"],
            nome=db_user["nome"],
            cognome=db_user["cognome"],
            email=db_user["email"],
            password=db_user["password"],
        )
    else:
        user = None

    return user


#ROUTE PER L'AREA PERSONALE
@app.route("/myprofile")
@login_required
def info_personali():
    prenotazioni_db = prenotazioni_dao.get_prenotazioni_by_id(current_user.id)
    return render_template("profilo.html", p_prenotazioni = prenotazioni_db)