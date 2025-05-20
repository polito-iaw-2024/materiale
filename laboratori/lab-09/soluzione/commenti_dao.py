import sqlite3
import datetime

# Operazioni sui Commenti

def get_comments(id):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT commenti.id, commenti.data_pubblicazione, commenti.testo, commenti.valutazione, commenti.immagine_commento, commenti.id_utente, utenti.nickname, utenti.immagine_profilo FROM commenti LEFT JOIN utenti ON commenti.id_utente = utenti.id WHERE commenti.id_post = ?'
    cursor.execute(sql, (id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return comments

def add_comment(comment):
    conn = sqlite3.connect('db/social_network.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()

    sql = 'INSERT INTO commenti(data_pubblicazione,testo,id_post,id_utente,valutazione,immagine_commento) VALUES(?,?,?,?,?,?)'
    cursor.execute(sql, (x.strftime("%Y-%m-%d"),
                         comment['testo'], comment['id_post'], comment['id_utente'], comment['valutazione'], comment['immagine_commento']))
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