import MySQLdb

try:
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="Ag140209",
        db="proyecto_cac"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    row = cursor.fetchone()
    print("Conexión exitosa a la base de datos:", row)
    cursor.close()
    conn.close()
except MySQLdb.Error as e:
    print(f"Error al conectar a MySQL: {e}")