import sqlite3


def nuovo_utente(p_nome, p_cognome, p_email, p_password):

    sql = "INSERT INTO studenti (nome, cognome, email, password) VALUES (?, ?, ?, ?)"

    conn = sqlite3.connect("ceposto.db")
    cursor = conn.cursor()
    cursor.execute(sql, (p_nome, p_cognome, p_email, p_password))

    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_id(p_id):

    sql = "SELECT * FROM studenti WHERE id = ?"

    conn = sqlite3.connect("ceposto.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(sql, (p_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def get_user_by_email(p_email):

    sql = "SELECT * FROM studenti WHERE email = ?"

    conn = sqlite3.connect("ceposto.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(sql, (p_email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user