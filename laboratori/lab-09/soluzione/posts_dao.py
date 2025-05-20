import sqlite3

# Operazioni sui Post

def get_posts():
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT posts.id, posts.data_pubblicazione, posts.testo, posts.immagine_post, utenti.nickname, utenti.immagine_profilo FROM posts LEFT JOIN utenti ON posts.id_utente = utenti.id ORDER BY data_pubblicazione DESC'
    cursor.execute(sql)
    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return posts

def get_post(id):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT posts.id, posts.data_pubblicazione, posts.testo, posts.immagine_post, posts.id_utente, utenti.nickname, utenti.immagine_profilo FROM posts LEFT JOIN utenti ON posts.id_utente = utenti.id WHERE posts.id = ?'
    cursor.execute(sql, (id,))
    post = cursor.fetchone()

    cursor.close()
    conn.close()

    return post

def add_post(post):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    if 'immagine_post' in post:
        sql = 'INSERT INTO posts(data_pubblicazione,testo,immagine_post,id_utente) VALUES(?,?,?,?)'
        cursor.execute(sql, (post['data_pubblicazione'],
                             post['testo'], post['immagine_post'], post['id_utente']))
    else:
        sql = 'INSERT INTO posts(data_pubblicazione,testo,id_utente) VALUES(?,?,?)'
        cursor.execute(sql, (post['data_pubblicazione'],
                             post['testo'], post['id_utente']))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success