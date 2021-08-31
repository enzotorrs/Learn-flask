from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, cursor, conect


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

@app.route("/editar")
def editar():
    sql = "SELECT * from downloads"
    cursor.execute(sql)
    lista = cursor.fetchall()
    return render_template("editar.html", titulo='Editar filmes', lista=lista)

@app.route("/atualizar/<string:nome>")
def atualizar(nome):
    sql = f"SELECT * FROM downloads where nome_do_filme = '{nome}' "
    cursor.execute(sql)
    lista = cursor.fetchall()[0]
    print(lista[0])
    return render_template("atualizar.html", lista=lista)

@app.route('/muda', methods=['POST', ])
def muda():
    sql = f"""UPDATE DOWNLOADS
    SET nome_do_filme = '{request.form['nome_do_filme']}',
    usuario ='{request.form['usuario']}',
    resolucao = '{request.form['resolucao']}'
    where nome_do_filme = '{request.form['nome']}'
"""
    cursor.execute(sql)
    conect.commit()
    flash(f"{request.form['nome_do_filme']} foi atualizado")
    return redirect(url_for('index'))

@app.route('/deletar/<string:nome>')
def deletar(nome):
    sql = f"""Delete from downloads
    where nome_do_filme = '{nome}'
"""
    cursor.execute(sql)
    conect.commit()
    flash(f"{nome} foi deladado")
    return redirect(url_for('index'))

@app.route('/typing')
def typing():
    return render_template('typing.html')

