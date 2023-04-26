from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bd_prog'

db = SQLAlchemy(app)

app.app_context().push()

class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    nome_social = db.Column(db.String(50))
    cpf = db.Column(db.String(14), nullable=False)
    altura = db.Column(db.Float)
    massa = db.Column(db.Float)
    genero = db.Column(db.String(10))
    idade = db.Column(db.Integer)
    email = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(14))
    endereco = db.Column(db.String(50))

    def to_json(self):
        return {'id_cliente': self.id_cliente, 'nome': self.nome, 'nome_social': self.nome_social, 'cpf': self.cpf, 'altura': self.altura, 'massa': self.massa, 'genero': self.genero, 'idade': self.idade, 'email': self.email, 'telefone': self.telefone, 'endereco': self.endereco}

# selecionar tudo
@app.route('/clientes', methods=['GET'])
def select_all():
    clientes_objetos = Cliente.query.all()
    clientes_json = [cliente.to_json() for cliente in clientes_objetos]

    return gera_response(200, 'clientes', clientes_json)

# selecionar um
@app.route('/clientes/<id_cliente>', methods=['GET'])
def select_client(id_cliente):
    cliente_objeto = Cliente.query.filter_by(id_cliente=id_cliente).first()
    cliente_json = cliente_objeto.to_json()

    return gera_response(200, 'cliente', cliente_json)

# cadastrar
@app.route('/cliente', methods=['POST'])
def cria_cliente():
    body = request.get_json()

    try:
        cliente = Cliente(nome=body['nome'], nome_social=body['nome_social'], cpf=body['cpf'], altura=body['altura'], massa=body['massa'], genero=body['genero'], idade=body['idade'], email=body['email'], telefone=body['telefone'], endereco=body['endereco'])
        db.session.add(cliente)
        db.session.commit()
        return gera_response(201, 'cliente', cliente.to_json(), 'Criado com sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_response(400, 'cliente', {}, 'Erro ao cadastrar')


# atualizar
@app.route('/cliente/<id_cliente>', methods=['PUT'])
def atualiza_cliente(id_cliente):
    cliente_objeto = Cliente.query.filter_by(id_cliente=id_cliente).first()
    body = request.get_json()

    try:
        if('nome' in body):
            cliente_objeto.nome = body['nome']
        if('nome_social' in body):
            cliente_objeto.nome_social = body['nome_social']
        if('cpf' in body):
            cliente_objeto.cpf = body['cpf']
        if('altura' in body):
            cliente_objeto.altura = body['altura']
        if('massa' in body):
            cliente_objeto.massa = body['massa']
        if('genero' in body):
            cliente_objeto.genero = body['genero']
        if('idade' in body):
            cliente_objeto.idade = body['idade']
        if('email' in body):
            cliente_objeto.email = body['email']
        if('telefone' in body):
            cliente_objeto.telefone = body['telefone']
        if('endereco' in body):
            cliente_objeto.endereco = body['endereco']
        
        db.session.add(cliente_objeto)
        db.session.commit()
        return gera_response(200, 'cliente', cliente_objeto.to_json(), 'Atualizado com sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_response(400, 'cliente', {}, 'Erro ao atualizar')

# deletar
@app.route('/cliente/<id_cliente>', methods=['DELETE'])
def deleta_cliente(id_cliente):
    cliente_objeto = Cliente.query.filter_by(id_cliente=id_cliente).first()

    try:
        db.session.delete(cliente_objeto)
        db.session.commit()
        return gera_response(200, 'cliente', cliente_objeto.to_json(), 'Deletado com sucesso')
    except Exception as e:
        print('Erro', e)
        return gera_response(400, 'cliente', {}, 'Erro ao deletar')


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')

app.run()