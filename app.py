from flask import Flask, render_template, request
from consulta_cep import consultar_cep, salvar_historico

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    dados = None
    erro = None

    if request.method == "POST":
        cep = request.form.get("cep")
        dados, erro = consultar_cep(cep)
        
        if dados:
            salvar_historico(dados)

    return render_template("index.html", dados=dados, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)