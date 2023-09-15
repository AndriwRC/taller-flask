from flask import Flask, render_template
import pyodbc

def make_connection():
    # Conexion Base de Datos
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\cuc\Desktop\taller-flask\TasksDB.accdb;")
    # Abrir cursor
    cursor=conn.cursor()
    return conn, cursor

def query_db_info(cursor):
    # Consultar informacion de la DB
    cursor.execute("SELECT * FROM Tareas")
    db_info = cursor.fetchall()
    return db_info

def close_connection(cursor, conn):
    # Cerrar conexion
    cursor.close
    conn.close

conn, cursor = make_connection()
db_info = query_db_info(cursor)
close_connection(conn, cursor)

app = Flask(__name__)


@app.route("/")
def index(db_info=db_info):
    return render_template('index.html', db_info=db_info)

@app.route("/add/")
def add_task():
    return render_template('add.html')

if __name__ == '__main__':
    app.run()
    