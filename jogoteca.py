from flask import Flask, render_template, request, redirect, session, flash, url_for


app = Flask(__name__)
app.secret_key = 'alura'

from dao import conect, cursor

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

usuario1 = Usuario('enzo', 'Enzo Torres', '3636')
usuario2 = Usuario('maliulia', 'Marilia Anita', '3636')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2}

from views import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
