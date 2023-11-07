from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import uuid #gera um nome único para salvar as imagens

app = Flask(__name__)
app.secret_key = "quitandazezinho"
usuario = "usuario"
senha = "senha"
login = False

#Função para verificar sessão
def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False
#conexão com o banco de dados
def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao
#iniciar banco de dados 
def iniciar_db():
    conexao = conecta_database
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()
#rota da pagina inicial
@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", produtos=produtos, title=title)
# final do código
app.run(debug=True)
