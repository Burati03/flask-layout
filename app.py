from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "123456"


def conectar_banco():
    banco = sqlite3.connect("banco.db")
    banco.row_factory = sqlite3.Row
    return banco


def criar_banco():
    banco = conectar_banco()
    cursor = banco.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    usuario = cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        ("gabriel",)
    ).fetchone()

    if usuario is None:
        senha_hash = generate_password_hash("1234")

        cursor.execute("""
            INSERT INTO usuarios (nome, usuario, senha)
            VALUES (?, ?, ?)
        """, ("Gabriel", "gabriel", senha_hash))

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS boletim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia TEXT NOT NULL,
            nota REAL NOT NULL
        )
    """)

    banco.commit()
    banco.close()


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Home"
    )


@app.route("/sobremim")
def sobremim():

    banco = conectar_banco()

    aluno = banco.execute(
        "SELECT nome, usuario FROM usuarios WHERE usuario = ?",
        ("gabriel",)
    ).fetchone()

    banco.close()

    return render_template(
        "sobremim.html",
        title="Sobre mim",
        aluno=aluno
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        senha = request.form["senha"]

        banco = conectar_banco()

        dados = banco.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        ).fetchone()

        banco.close()

        if dados and check_password_hash(dados["senha"], senha):

            session["usuario_id"] = dados["id"]
            session["usuario"] = dados["usuario"]

            return redirect(url_for("boletim"))

        return render_template(
            "login.html",
            title="Login",
            erro="Usuário ou senha incorretos."
        )

    return render_template(
        "login.html",
        title="Login"
    )


@app.route("/boletim")
def boletim():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    banco = conectar_banco()

    notas = banco.execute(
        "SELECT * FROM boletim"
    ).fetchall()

    banco.close()

    return render_template(
        "boletim.html",
        title="Boletim",
        notas=notas
    )


@app.route("/notas")
def notas():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    banco = conectar_banco()

    notas = banco.execute(
        "SELECT * FROM boletim"
    ).fetchall()

    banco.close()

    return render_template(
        "notas.html",
        title="Notas",
        notas=notas
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)