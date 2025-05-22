from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')  # Rota principal
def home():
    return render_template('cadastro.html')  # Mostra o formulário

@app.route('/cadastrar', methods=['POST'])  # Rota que recebe o formulário
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Salvar em arquivo (poderia ser banco de dados)
    with open('usuarios.txt', 'a') as arquivo:
        arquivo.write(f'{nome},{email},{senha}\n')

    return f"Cadastro realizado com sucesso para {nome}!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

