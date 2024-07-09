from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '******'
app.config['MYSQL_DB'] = 'proyecto_cac'
mysql = MySQL(app)

@app.route('/')
def index():
    conn = mysql.connection 
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados"
    cursor.execute(sql)  
    
    empleados = cursor.fetchall()
     
    conn.commit()

    return render_template('empleados/index.html', empleados=empleados)

@app.route('/create')
def create():
    return render_template("empleados/create.html")

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _doc = request.form['']
    _dirección = request.form['txtDirección']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
   
    sql = "INSERT INTO empleados (nombre, doc, dirrección, correo, foto) values(%s, %i, %s, %s, %s);" 
    datos = (_nombre, _doc, _dirección, _correo, _foto.filename)

    conn = mysql.connection 
    cursor = conn.cursor()
    cursor.execute(sql, datos)     
    conn.commit()
    
    return redirect('/')
   
    
if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
