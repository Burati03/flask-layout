from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    aluno = {
        "nome": "Gabriel",
        "turma": "2° TEC"
    }

    return render_template("index.html", title="Home", aluno=aluno)

@app.route("/boletim")
def boletim():
    return render_template("boletim.html", title="Boletim")

@app.route("/sobremim")
def sobremim():
    aluno = {
        "nome": "Gabriel",
        "turma": "2° TEC"
    }

    return render_template("sobremim.html", title="Sobre mim", aluno=aluno)

if __name__ == "__main__":
    app.run(debug=True)