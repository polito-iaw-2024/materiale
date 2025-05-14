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
