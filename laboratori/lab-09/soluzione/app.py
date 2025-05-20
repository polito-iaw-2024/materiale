# import module
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

import posts_dao, commenti_dao, utenti_dao

from models import User

# Import the Image module from the PIL (Python Imaging Library) package. Used to preprocess the images uploaded by the users. Ensure 'Pillow' is installed before running the application by using the command 'pip install Pillow'
from PIL import Image

PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

# create the application
app = Flask(__name__)

app.config["SECRET_KEY"] = "Secret key del social network"

login_manager = LoginManager()
login_manager.init_app(app)


# define the homepage
@app.route("/")
def home():
    posts_db = posts_dao.get_posts()

    return render_template("home.html", posts=posts_db)


# define the single post page
@app.route("/posts/<int:id>")
def single_post(id):
    post_db = posts_dao.get_post(id)
    comments_db = commenti_dao.get_comments(id)

    return render_template("post.html", post=post_db, comments=comments_db)


# define the new post endpoint
@app.route("/posts/new", methods=["POST"])
@login_required
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

        # Open the user-provided image using the Image module
        img = Image.open(post_image)

        # Get the width and height of the image
        width, height = img.size

        # Calculate the new height while maintaining the aspect ratio based on the desired width
        new_height = height / width * POST_IMG_WIDTH

        # Define the size for thumbnail creation with the desired width and calculated height
        size = POST_IMG_WIDTH, new_height
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # Extracting file extension from the image filename
        ext = post_image.filename.split(".")[-1]
        # Getting the current timestamp in seconds
        secondi = int(datetime.now().timestamp())

        # Saving the image with a unique filename in the 'static' directory
        img.save(
            "static/@" + current_user.nickname.lower() + "-" + str(secondi) + "." + ext
        )

        # Updating the 'immagine_post' field in the post dictionary with the image filename
        post["immagine_post"] = (
            "@" + current_user.nickname.lower() + "-" + str(secondi) + "." + ext
        )

    post["id_utente"] = int(current_user.id)
    success = posts_dao.add_post(post)

    if success:
        app.logger.info("Post creato correttamente")
    else:
        app.logger.error("Errore nella creazione del post: riprova!")

    return redirect(url_for("home"))


# define the new comment endpoint
@app.route("/comments/new", methods=["POST"])
@login_required
def new_comment():

    comment = request.form.to_dict()

    if comment["testo"] == "":
        app.logger.error("Il commento non può essere vuoto!")
        return redirect(url_for("single_post", id=comment["id_post"]))

    comment_image = request.files["immagine_commento"]
    if comment_image:
        # Open the user-provided image using the Image module
        img = Image.open(comment_image)

        # Get the width and height of the image
        width, height = img.size

        # Calculate the new height while maintaining the aspect ratio based on the desired width
        new_height = height / width * POST_IMG_WIDTH

        # Define the size for thumbnail creation with the desired width and calculated height
        size = POST_IMG_WIDTH, new_height
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # Extracting file extension from the image filename
        ext = comment_image.filename.split(".")[-1]
        # Getting the current timestamp in seconds
        secondi = int(datetime.now().timestamp())

        # Saving the image with a unique filename in the 'static' directory
        img.save("static/@comment-" + str(secondi) + "." + ext)

        # Updating the 'immagine_commento' field in the comment dictionary with the image filename
        comment["immagine_commento"] = "@comment-" + str(secondi) + "." + ext
    else:
        comment["immagine_commento"] = None

    comment["id_post"] = int(comment["id_post"])
    comment["id_utente"] = int(current_user.id)
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


# define the signup page
@app.route("/iscriviti")
def iscriviti():
    return render_template("signup.html")


@app.route("/iscriviti", methods=["POST"])
def iscriviti_post():

    nuovo_utente_form = request.form.to_dict()

    user_in_db = utenti_dao.get_user_by_nickname(nuovo_utente_form.get("nickname"))

    if user_in_db:
        flash("C'è già un utente registrato con questo nickname", "danger")
        return redirect(url_for("iscriviti"))
    else:
        img_profilo = ""
        usr_image = request.files["immagine_profilo"]
        if usr_image:
            # Open the user-provided image using the Image module
            img = Image.open(usr_image)

            # Get the width and height of the image
            width, height = img.size

            # Calculate the new width while maintaining the aspect ratio
            new_width = PROFILE_IMG_HEIGHT * width / height

            # Define the size for thumbnail creation with the desired height and calculated width
            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # Calculate the coordinates for cropping the image to a square shape
            left = new_width / 2 - PROFILE_IMG_HEIGHT / 2
            top = 0
            right = new_width / 2 + PROFILE_IMG_HEIGHT / 2
            bottom = PROFILE_IMG_HEIGHT

            # Crop the image using the calculated coordinates to create a square image
            img = img.crop((left, top, right, bottom))

            # Extracting file extension from the image filename
            ext = usr_image.filename.split(".")[-1]

            # Saving the image with a unique filename in the 'static' directory
            img.save("static/" + nuovo_utente_form.get("nickname").lower() + "." + ext)

            img_profilo = nuovo_utente_form.get("nickname").lower() + "." + ext

        nuovo_utente_form["password"] = generate_password_hash(
            nuovo_utente_form.get("password")
        )
        # Updating the 'immagine_profilo' field in the user dictionary with the image filename
        nuovo_utente_form["immagine_profilo"] = img_profilo

        success = utenti_dao.add_user(nuovo_utente_form)

        if success:
            flash("Utente creato correttamente", "success")
            return redirect(url_for("home"))
        else:
            flash("Errore nella creazione del utente: riprova!", "danger")

    return redirect(url_for("iscriviti"))


@app.route("/login", methods=["POST"])
def login():

    utente_form = request.form.to_dict()

    utente_db = utenti_dao.get_user_by_nickname(utente_form["nickname"])

    if not utente_db or not check_password_hash(
        utente_db["password"], utente_form["password"]
    ):
        flash("Credenziali non valide, riprova", "danger")
        return redirect(url_for("home"))
    else:
        new = User(
            id=utente_db["id"],
            nickname=utente_db["nickname"],
            password=utente_db["password"],
            immagine_profilo=utente_db["immagine_profilo"],
        )
        login_user(new, True)
        flash("Bentornato " + utente_db["nickname"] + "!", "success")

        return redirect(url_for("home"))


@login_manager.user_loader
def load_user(user_id):

    db_user = utenti_dao.get_user_by_id(user_id)
    if db_user is not None:
        user = User(
            id=db_user["id"],
            nickname=db_user["nickname"],
            password=db_user["password"],
            immagine_profilo=db_user["immagine_profilo"],
        )
    else:
        user = None

    return user


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


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
