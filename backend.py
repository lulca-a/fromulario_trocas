from flask import Flask, request, jsonify
from flask_cors import CORS

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
    lista.append(dados)

def enviar_email(dados):
    print('emal eviado para', email[dados['pessoa_1']])
    print('emal eviado para', email[dados['pessoa_2']])
    print('emal eviado para', email_admin)
    
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
            'turno_2':dados['turno_2']
        })
    
@app.route('/aprovar',methods=['POST'])
def aprovar():
    dados = 'read_db("id_troca")'
    dados['status_1'] = 'OK'
    dados['status_2'] = 'OK'
    dados['status_admin'] = 'OK'
    print('troca efetuada!')
    
app.run(debug= True)
