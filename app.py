from flask import Flask, render_template, request, redirect
import mysql.connector


# Configura los parámetros de conexión
config = {
    "user": "public",
    "password": "42PzVD!K",
    "host": "localhost",
    "database": "TasksDB",
    "port": 3306,
}


def make_connection():
    # Conexion Base de Datos
    conn = mysql.connector.connect(**config)
    # Abrir cursor
    cursor = conn.cursor()
    return conn, cursor


def query_db_info(cursor):
    # Consultar informacion de la DB
    cursor.execute("SELECT * FROM Tareas")
    db_info = cursor.fetchall()
    return db_info


def close_connection(cursor, conn):
    # Cerrar conexion
    cursor.close()
    conn.close()


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    conn, cursor = make_connection()

    if request.method == "POST":
        description = request.form["description"]
        cursor.execute(f"INSERT INTO Tareas (Descripcion) VALUES ('{description}')")
        conn.commit()

    db_info = query_db_info(cursor)
    close_connection(conn, cursor)

    return render_template("index.html", db_info=db_info)


@app.route("/new-task/")
def add_task():
    return render_template("new-task.html")


@app.route("/task/<int:id>/complete/")
def complete_task(id):
    conn, cursor = make_connection()

    cursor.execute(f"SELECT Completado FROM Tareas WHERE Id = {id}")
    status = cursor.fetchone()
    if status[0]:
        update = f"UPDATE Tareas SET Completado = FALSE WHERE Id = {id}"
    else:
        update = f"UPDATE Tareas SET Completado = TRUE WHERE Id = {id}"
    cursor.execute(update)
    conn.commit()

    close_connection(conn, cursor)
    return redirect("/")


@app.route("/task/<int:id>/delete/")
def delete_task(id):
    conn, cursor = make_connection()

    cursor.execute(f"SELECT * FROM Tareas WHERE Id = {id}")
    task = cursor.fetchone()
    if task:
        cursor.execute(f"DELETE FROM Tareas WHERE Id = {id}")
    conn.commit()

    close_connection(conn, cursor)
    return redirect("/")


if __name__ == "__main__":
    app.run()
