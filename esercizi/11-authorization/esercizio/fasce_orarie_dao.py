import sqlite3


def get_fasce_orarie():
    
    sql = "SELECT * FROM fasce_orarie"

    conn = sqlite3.connect("ceposto.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(sql)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
