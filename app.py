from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    aluno = {
        "nome": "Gabriel",
        "turma": "2° TEC"
    }
   
    return render_template('index.html', title="Home", aluno=aluno)

@app.route("/boletim")
def boletim():
    return render_template('boletim.html', title="Boletim")
