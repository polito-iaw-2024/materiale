import sqlite3

if __name__ == '__main__':

  sql = "INSERT INTO utenti (nome, cognome, email) VALUES (?, ?, ?)"

  conn = sqlite3.connect('tasks.db')
  cursor = conn.cursor()

  cursor.execute(sql, ("Alberto", "Monge", "alberto.monge@polito.it"))

  conn.commit()

  cursor.close()
  conn.close()