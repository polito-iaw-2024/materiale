from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, nome, cognome, email, password):
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.password = password
