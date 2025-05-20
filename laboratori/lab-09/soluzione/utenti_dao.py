import sqlite3

def get_users():
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id, nickname FROM utenti'
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

def add_user(user):

    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO utenti(nickname,password,immagine_profilo) VALUES(?,?,?)'

    try:
        cursor.execute(
            sql, (user['nickname'], user['password'], user['immagine_profilo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_user_by_id(id):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

# Funzione ausiliare per cercare l'id di un utente dato il suo nickname

def get_user_by_nickname(nickname):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE nickname = ?'
    cursor.execute(sql, (nickname,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user