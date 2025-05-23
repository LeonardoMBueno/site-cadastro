from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "chave_super_secreta"  # Necessário para usar sessão

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do banco de dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)

# Cria o banco de dados se não existir
with app.app_context():
    db.create_all()

# Página inicial (cadastro)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect("/login")

    return render_template("index.html")

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email, senha=senha).first()

        if usuario:
            session["usuario"] = usuario.nome
            return redirect("/usuarios")
        else:
            return "Email ou senha incorretos."

    return render_template("login.html")

# Lista de usuários cadastrados (somente logado)
@app.route("/usuarios")
def usuarios():
    if "usuario" not in session:
        return redirect("/login")

    todos = Usuario.query.all()
    return render_template("usuarios.html", usuarios=todos)

# Logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
