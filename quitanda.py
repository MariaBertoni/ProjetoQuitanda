from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import uuid

app = Flask(__name__)
app.secret_key = "quitandadozezinho"

usuario = "adim"
senha = "1234"
login = False

# ------------------------------ FUNÇÃO PARA VERIFICAR A SESSÃO ------------------------------

def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False
    
# ------------------------------ CONEXÃO COM O BANCO DE DADOS ------------------------------

def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao

# ------------------------------ INICIAR O BANCO DE DADOS ------------------------------

def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
        conexao.commit()
        conexao.close()

# ------------------------------ ROTA DA PÁGINA INICIAL ------------------------------

@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", produtos=produtos, title=title)

# ------------------------------ ROTA DA PÁGINA LOGIN ------------------------------
@app.route("/login")
def login():
    title="Login"
    return render_template("login.html", title=title)

@app.route("/acesso", methods=['POST'])
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]


    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/') #homepage
    else:
        return render_template("login.html",msg="Usuário/Senha estão errados!")
    
@app.route("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
        conexao.close()
        title = "Administração"
        return render_template("adm.html", produtos=produtos, title=title)
    else:
        return redirect("/login")
    
    #código do LOGOUT
@app.route("/logout")
def logout():
    global login
    login = False
    session.clear()
    return redirect('/')

@app.route("/cadastro")
def cadastro ():
    if verifica_sessao():
        title = "Cadastro de produtos"
        return render_template("cadastro.html",title=title)
    else:
        return redirect("/login")
    
#ROTA PARA CADASTRO NO BANCO DE DADOS
@app.route("/cadastro", methods=["post"])
def cadastro():
    if verifica_sessao:
        nome_prod=request.form['nome_prod']
        desc_prod=request.form['desc_prod']
        preco_prod=request.form['preco_prod']
        img_prod=request.files['img_prod']
        id_foto=str(uuid.uuid4().hex)
        filename=id_foto+nome_prod+'.png'
        img_prod.save("static/img/produtos"+filename)
        conexao = conecta_database()
        conexao.execute('INSERT INTO produtos (nome_prod, desc_prod, preco_prod, img_prod) VALUES (?, ?, ?, ?)', (nome_prod, desc_prod, preco_prod, filename))
        conexao.commit() #Confirma a alteração no BD
        conexao.close()
        return redirect('/adm')
    else:
        return redirect('/login') # Vai para HOME

# ------------------------------ FINAL DO CODIGO - EXECUTANDO O SERVIDOR ------------------------------

app.run(debug=True)  
