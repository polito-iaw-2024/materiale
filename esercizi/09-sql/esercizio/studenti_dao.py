import sqlite3

def nuovo_utente(p_nome, p_cognome, p_email):

  sql = "INSERT INTO utenti (nome, cognome, email) VALUES (?, ?, ?)"
  
  conn = sqlite3.connect('ceposto.db')
  cursor = conn.cursor()
  cursor.execute(sql, (p_nome, p_cognome, p_email))
  
  conn.commit()
  cursor.close()
  conn.close()