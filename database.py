import sqlite3

def conectar():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    return conn, c

def crear_tablas():
    conn, c = conectar()
    
    # Creamos la tabla "clientes"
    c.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL
        )
    """)
    
    # Creamos la tabla "Pedidos"
    c.execute("""
        CREATE TABLE IF NOT EXISTS Pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        codigo_producto TEXT,
        cantidad INTEGER,
        nombre_producto TEXT,
        precio_local REAL,
        precio_dolar REAL,
        FOREIGN KEY (id_cliente) REFERENCES clientes (id)
    )
    """)
    
    conn.commit()

# Resto del código del archivo database.py

    conn.close()
