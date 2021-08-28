from flask import Flask, render_template, request, redirect, session, flash, url_for
import psycopg2


app = Flask(__name__)
app.secret_key = 'alura'

conect = psycopg2.connect(host='192.168.0.136', database='Site',
                                        user='enzotorr',
                                        password='cueca135galinha')
cursor = conect.cursor()


class Download:
    def __init__(self, nome_do_filme, usuario, resolucao):
        self.nome_do_filme = nome_do_filme
        self.usuario = usuario
        self.resolucao = resolucao

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('enzo', 'Enzo Torres', '3636')
usuario2 = Usuario('maliulia', 'Marilia Anita', '3636')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2}



@app.route('/')
def index():
    sql = "SELECT * from downloads"
    cursor.execute(sql)
    lista = cursor.fetchall()
    return render_template('lista.html', titulo='Lista de filmes', lista=lista)


@app.route('/login')
def login():
    proximo = request.args.get('proximo')

    return render_template('login.html', proximo=proximo)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            proxima_pagina = request.form['proximo']
            session['usuario_logado'] = usuario.id
            flash(usuario.nome+' se logou com sucesso!')
            return redirect(proxima_pagina)
    else:
        flash('usuario ou senha incorretos')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/gravar', methods=['POST', ])
def gravar():
    nome_do_filme = request.form['nome_do_filme']
    usuario = request.form['usuario']
    obervacao = request.form['obs']
    resolucao = request.form['resolucao']
    sql = f"INSERT INTO DOWNLOADS VALUES ('{nome_do_filme}', '{usuario}', '{obervacao}', '{resolucao}')"
    cursor.execute(sql)
    conect.commit()
    return redirect(url_for('index'))

@app.route('/typing')
def typing():
    return render_template('typing.html')

app.run(host='0.0.0.0', port='8000', debug=True)
