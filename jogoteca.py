from flask import Flask, render_template, request, redirect, session, flash, url_for
#fazer rota para gravar downloads

app = Flask(__name__)
app.secret_key = 'alura'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('enzo', 'Enzo Torres', '3636')
usuario2 = Usuario('maliulia', 'Marilia Anita', '3636')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
lista = [jogo1, jogo2]


@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proximo=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


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
    with open('filmes.txt', 'w') as arq:
        arq.write(nome_do_filme)
        arq.write(usuario)
    return redirect(url_for('index'))


app.run(host='0.0.0.0', port='8000', debug=True)
