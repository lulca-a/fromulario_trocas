from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets

pessoas = ['João','Maria','Carlos']
campos  =['pessoa_1','pessoa_2','dia_1','dia_2','turno_1','turno_2']
email = {'João':'email@email.com',
          'Maria':'email@email.com',
          'Carlos':'email@email.com'}
email_admin = 'admin@email.com.br'

app = Flask(__name__)
CORS(app)

lista = []#futuramente será substituído um banco de dados estruturado
def salvar_troca(dados):
          dados['id_troca'] = len(lista)+1
          dados['status_1'] = 'pendente'
          dados['status_2'] = 'pendente'
          dados['status_admin'] = 'pendente'
          dados['token_1'] = secrets.token_urlsafe(16)
          dados['token_2'] = secrets.token_urlsafe(16)
          dados['token_admin'] = secrets.token_urlsafe(16)
          lista.append(dados)

def enviar_email(dados):
    link_email_1 = f'http://127.0.0.1:5000/aprovar?id={dados["id_troca"]}&token={dados["token_1"]}' 
    link_email_2 = f'http://127.0.0.1:5000/aprovar?id={dados["id_troca"]}&token={dados["token_2"]}'
    link_email_admin = f'http://127.0.0.1:5000/aprovar?id={dados["id_troca"]}&token={dados["token_admin"]}'

    print('emal eviado para', email[dados['pessoa_1']], 'com o link', link_email_1)
    print('emal eviado para', email[dados['pessoa_2']], 'com o link', link_email_2)
    print('emal eviado para', email_admin, 'com o link', link_email_admin)

@app.route('/trocas',methods = ['GET'])
def read_troca():
    return jsonify(lista)
    
@app.route('/troca',methods=['POST'])
def troca():
    dados = request.json
    for campo in campos:
        if not dados.get(campo):
            return jsonify({'mensagem' : f'{campo} não preenchido'})
            
    salvar_troca(dados)
    enviar_email(dados)
    
    return jsonify({
            'id_troca':dados['id_troca'],
            'pessoa_1':dados['pessoa_1'],
            'dia_1':dados['dia_1'], 
            'turno_1':dados['turno_1'],
            'pessoa_2':dados['pessoa_2'],
            'dia_2':dados['dia_2'],
            'turno_2':dados['turno_2'],
            'status_1':dados['status_1'],
            'status_2':dados['status_2'],
            'status_admin':dados['status_admin'],          
        })
    
@app.route('/aprovar',methods=['GET'])
def aprovar():
    id = int(request.args.get('id'))
    token = request.args.get('token')          
    for i in lista:
        if i['id_troca'] == id:
            if token == i['token_1']:
                i['status_1'] = 'OK'
                print('id', id, 'token', token, 'status_1', i['status_1'])
                break
            elif token == i['token_2']:
                i['status_2'] = 'OK'
                print('id', id, 'token', token, 'status_2', i['status_2'])
                break
            elif token == i['token_admin']:
                i['status_admin'] = 'OK'
                print('id', id, 'token', token, 'status_admin', i['status_admin'])
                break
    return jsonify({'mensagem' :'troca efetuada'})
    
app.run(debug= True)
