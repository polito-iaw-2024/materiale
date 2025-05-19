import sqlite3


def prenotare_aula(id_studente, id_aula, attiva, data, id_fascia_oraria):

    sql = "INSERT INTO prenotazioni (id_studente, id_aula, attiva, data, fascia_oraria) VALUES (?, ?, ?, ?, ?)"

    conn = sqlite3.connect("ceposto.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(sql, (id_studente, id_aula, attiva, data, id_fascia_oraria))

    conn.commit()

    cursor.close()
    conn.close()
    return


def get_prenotazioni_by_id(id_studente):
    
    sql = "SELECT prenotazioni.id, fasce_orarie.ora_inizio, fasce_orarie.ora_fine, aule.nome FROM prenotazioni LEFT JOIN aule ON prenotazioni.id_aula = aule.id WHERE id_studente = ? AND fasce_orarie.id = prenotazioni.id"

    conn = sqlite3.connect("ceposto.db")
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute(sql, (id_studente,))

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
