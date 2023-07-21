import sqlite3

def conectar():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    return conn, c

conn, c = conectar()
conn.commit()
conn.close()
