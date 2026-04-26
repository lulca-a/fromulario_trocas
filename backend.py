from flask import Flask, request, jsonify
from flask_cors import CORS

pessoas = ['João','Maria','Carlos']
campos  =['pessoa_1','pessoa_2','dia_1','dia_2','turno_1','turno_2']

app = Flask(__name__)
CORS(app)
lista = []

@app.route('/troca',methods=['POST'])
def salvar_troca(dados):
    dados['id_troca'] = len(lista)+1
    lista.append(dados)

def troca():
    dados = request.json
    for campo in campos:
        if not dados.get(campo):
            return jsonify({'mensagem' : f'{campo} não preenchido'})
            
    salvar_troca(dados)
    
    return jsonify({
            'id_troca':dados['id_troca'],
            'pessoa_1':dados['pessoa_1'],
            'dia_1':dados['dia_1'], 
            'turno_1':dados['turno_1'],
            'pessoa_2':dados['pessoa_2'],
            'dia_2':dados['dia_2'],
            'turno_2':dados['turno_2']
        })
app.run(debug= True)
