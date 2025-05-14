# import module
from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime

import posts_dao, commenti_dao, utenti_dao

# create the application
app = Flask(__name__)


# define the homepage
@app.route("/")
def home():
    posts_db = posts_dao.get_posts()
    users_db = utenti_dao.get_users()

    return render_template("home.html", posts=posts_db, users=users_db)


# define the single post page
@app.route("/posts/<int:id>")
def single_post(id):
    post_db = posts_dao.get_post(id)
    comments_db = commenti_dao.get_comments(id)
    users_db = utenti_dao.get_users()

    return render_template(
        "post.html", post=post_db, comments=comments_db, users=users_db
    )


# define the new post endpoint
@app.route("/posts/new", methods=["POST"])
def new_post():

    post = request.form.to_dict()

    if post["testo"] == "":
        app.logger.error("Il post non può essere vuoto!")
        return redirect(url_for("home"))

    if post["data_pubblicazione"] == "":
        app.logger.error("Devi selezionare una data")
        return redirect(url_for("home"))

    if datetime.strptime(post["data_pubblicazione"], "%Y-%m-%d").date() < date.today():
        app.logger.error("Data errata")
        return redirect(url_for("home"))

    post_image = request.files["immagine_post"]
    if post_image:
        post_image.save("static/" + post_image.filename)
        post["img"] = post_image.filename

    success = posts_dao.add_post(post)

    if success:
        app.logger.info("Post creato correttamente")
    else:
        app.logger.error("Errore nella creazione del post: riprova!")

    return redirect(url_for("home"))


# define the new comment endpoint
@app.route("/comments/new", methods=["POST"])
def new_comment():

    comment = request.form.to_dict()

    if comment["testo"] == "":
        app.logger.error("Il commento non può essere vuoto!")
        return redirect(url_for("single_post", id=comment["id_post"]))

    comment_image = request.files["immagine_commento"]
    if comment_image:
        comment_image.save("static/" + comment_image.filename)
        comment["immagine_commento"] = comment_image.filename
    else:
        comment["immagine_commento"] = None

    comment["id_post"] = int(comment["id_post"])
    comment["valutazione"] = int(comment["radioOptions"])

    if "isAnonymous" in comment and comment["isAnonymous"] == "on":
        comment["id_utente"] = None
    else:
        comment["id_utente"] = int(comment["id_utente"])

    success = commenti_dao.add_comment(comment)

    if success:
        app.logger.info("Commento creato correttamente")
    else:
        app.logger.error("Errore nella creazione del commento: riprova!")

    return redirect(url_for("single_post", id=comment["id_post"]))


# define the 'about' page
@app.route("/about")
def about():
    p_developers = [
        {
            "id": 1234,
            "name": "Juan Pablo Sáenz",
            "devimg": "user.jpg",
            "quote": "A well-known quote, contained in a blockquote element",
            "quoteAuthor": "First quote author",
        },
        {
            "id": 5678,
            "name": "Tommaso Calò",
            "devimg": "user.jpg",
            "quote": "A well-known quote, contained in a blockquote element",
            "quoteAuthor": "Second quote author",
        },
    ]
    return render_template("about.html", developers=p_developers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
