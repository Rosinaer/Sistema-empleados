from flask import Flask, render_template
from flask_mysqldb import MySQL
import MySQLdb


app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '********'
app.config['MYSQL_DB'] = 'proyecto_cac'
mysql = MySQL(app)

@app.route('/')
def index():
    conn = mysql.connection 
    cursor = conn.cursor()

    sql = "insert into empleados (nombre, Doc, dirección, correo, foto)values('Juan Garcia', 28456789, 'malvinas 345', 'juangonzalez@gmail.com', 'fotojuan.jpg');"
    cursor.execute(sql)

    conn.commit()

    return render_template('empleados/index.html')

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
