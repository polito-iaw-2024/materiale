import sqlite3

def nuovo_utente(p_nome, p_cognome, p_email, p_foto_profilo):
  sql = "INSERT INTO utenti (nome, cognome, email, foto_profilo) VALUES (?, ?, ?, ?)"
  
  conn = sqlite3.connect('tasks.db')
  cursor = conn.cursor()
  cursor.execute(sql, (p_nome, p_cognome, p_email, p_foto_profilo))
  
  conn.commit()
  cursor.close()
  conn.close()