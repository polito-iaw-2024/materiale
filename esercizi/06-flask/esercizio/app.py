from flask import Flask, render_template

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
