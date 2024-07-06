from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()


if __name__ == '__main__':
     print("Starting Flask app...")
     app.run(debug=True) 
 