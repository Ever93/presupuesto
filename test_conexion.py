import sqlite3

def conectar():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    return conn, c

if __name__ == "__main__":
    conn, c = conectar()
    print("Conexión exitosa:")
    print("Base de datos: crm.db")  # Imprimir el nombre de la base de datos
    print("Cursor:", c)

    # Obtener la lista de tablas disponibles en la base de datos
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print("Tablas disponibles:")
    for table in tables:
        print(table[0])

    conn.commit()
    conn.close()
