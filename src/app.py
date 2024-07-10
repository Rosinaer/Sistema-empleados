from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mysqldb import MySQL
from datetime import datetime
import os


app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*******'
app.config['MYSQL_DB'] = 'proyecto_cac'

UPLOADS = os.path.join(app.root_path, 'uploads')
app.config['UPLOADS'] = UPLOADS

mysql = MySQL(app)

@app.route('/uploads/<path:nombreFoto>')
def uploads(nombreFoto):
    try:
       print(f"Solicitando la foto: {nombreFoto}")
       print(f"Directorio completo: {app.config['UPLOADS']}")
       return send_from_directory(app.config['UPLOADS'], nombreFoto)
    except Exception as e:
        print(f"Error al servir la foto: {e}")
        return "Error al servir la foto", 404

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
    return render_template('empleados/create.html')

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form['txtNombre']
    _doc = request.form['txtDoc']
    _dirección = request.form['txtDirección']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    now = datetime.now()
    tiempo = now.strftime("%y%H%M%S")
    
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' +_foto.filename
        _foto.save(os.path.join(app.root_path, 'uploads', nuevoNombreFoto))
    
   
    sql = "INSERT INTO empleados (nombre, doc, dirección, correo, foto) values(%s, %s, %s, %s, %s);" 
    datos = (_nombre, _doc, _dirección, _correo, nuevoNombreFoto)

    conn = mysql.connection 
    cursor = conn.cursor()
    cursor.execute(sql, datos)     
    conn.commit()
    
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connection 
    cursor = conn.cursor()
    
    sql = 'SELECT foto FROM empleados WHERE id=%s'
    cursor.execute(sql, (id, )) 
    
    nombreFoto = cursor.fetchone()[0]
    
    try:
        os.remove(os.path.join(app.config[UPLOADS], nombreFoto))
    except:
        pass
    
    sql = 'DELETE FROM empleados WHERE id=%s' 
    cursor.execute(sql, (id, )) 
     
    conn.commit()

    return redirect('/')
   
@app.route('/modify/<int:id>')
def modify(id):
    conn = mysql.connection 
    cursor = conn.cursor()
    
    sql = 'SELECT * FROM empleados WHERE id=%s' 
    cursor.execute(sql, (id, ))
    empleado = cursor.fetchone() 
    conn.commit()
    
    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def updates():
    _nombre = request.form['txtNombre']
    _doc = request.form['txtDoc']
    _dirección = request.form['txtDirección']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']
    print(f"Nombre: {_nombre}, Doc: {_doc}, Dirección: {_dirección}, Correo: {_correo}, Foto: {_foto.filename}, ID: {id}")
    
    conn = mysql.connection 
    cursor = conn.cursor()
    
    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%y%H%M%S")
        nuevoNombreFoto = tiempo + '_' +_foto.filename
        _foto.save(os.path.join(app.config['UPLOADS'], nuevoNombreFoto))
 
       # Obtener el nombre de la foto anterior
        sql = 'SELECT foto FROM empleados WHERE id=%s' 
        cursor.execute(sql, (id, ))
        nombreFoto = cursor.fetchone()[0]
        conn.commit()
        
        # Borrar la foto anterior
        borrarEstaFoto = os.path.join(app.config['UPLOADS'], nombreFoto)  
        print(f"Intentando borrar: {borrarEstaFoto}")
        
        # Borrar la foto anterior si existe
        if os.path.exists(borrarEstaFoto):
           os.remove(borrarEstaFoto)
        else:
            print(f"Archivo no encontrado: {borrarEstaFoto}")  
            
        # Actualizar la base de datos con el nuevo nombre de la foto
        sql ='UPDATE empleados SET foto =%s  WHERE id=%s'
        cursor.execute(sql,(nuevoNombreFoto, id) )
        conn.commit()
        
    # Actualizar los demás campos
    sql = 'UPDATE empleados SET nombre=%s, Doc=%s, dirección=%s, correo=%s WHERE id=%s'
    datos = (_nombre, _doc, _dirección, _correo, id)
    
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/')
   
if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)

    