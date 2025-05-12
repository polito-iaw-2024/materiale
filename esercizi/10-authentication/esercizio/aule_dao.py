import sqlite3

def get_aule():

  sql = "SELECT * FROM aule"
  
  conn = sqlite3.connect('ceposto.db')
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute(sql)

  aule = cursor.fetchall()
  
  cursor.close()
  conn.close()

  return aule

def get_aula(id):
    
    sql = "SELECT * FROM aule WHERE aule.id = ?"

    conn = sqlite3.connect('ceposto.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    
    post = cursor.fetchone()

    cursor.close()
    conn.close()

    return post