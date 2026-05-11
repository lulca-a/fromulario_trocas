import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import secrets

load_dotenv()

EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_ADMIN = os.getenv('EMAIL_ADMIN', 'admin@email.com.br')

if not EMAIL_FROM or not EMAIL_PASSWORD:
    raise RuntimeError('Defina EMAIL_FROM e EMAIL_PASSWORD no arquivo .env para enviar emails')

pessoas = ['João','Maria','Carlos']
campos  =['pessoa_1','pessoa_2','dia_1','dia_2','turno_1','turno_2']

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
    assunto = f'Troca ({dados["id_troca"]}): {dados["pessoa_1"]}_{dados["turno_1"]}-{dados["dia_1"]} // {dados["pessoa_2"]}_{dados["turno_2"]}-{dados["dia_2"]}'

    link_email_1 = f'http://127.0.0.1:5000/aprovar?id={dados["id_troca"]}&token={dados["token_1"]}'
    link_email_2 = f'http://127.0.0.1:5000/aprovar?id={dados["id_troca"]}&token={dados["token_2"]}'
    link_email_admin = f'http://127.0.0.1:5000/aprovar?id={dados["id_troca"]}&token={dados["token_admin"]}'

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.set_debuglevel(1)
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)

            # pessoa 1
            msg1 = EmailMessage()
            msg1['Subject'] = assunto
            msg1['From'] = EMAIL_FROM
            msg1['To'] = EMAIL_FROM  # depois troca
            msg1.set_content(f'Aprove sua troca:\n{link_email_1}')
            smtp.send_message(msg1)

            # pessoa 2
            msg2 = EmailMessage()
            msg2['Subject'] = assunto
            msg2['From'] = EMAIL_FROM
            msg2['To'] = EMAIL_FROM  # depois troca
            msg2.set_content(f'Aprove sua troca:\n{link_email_2}')
            smtp.send_message(msg2)

            # admin
            msg3 = EmailMessage()
            msg3['Subject'] = assunto
            msg3['From'] = EMAIL_FROM
            msg3['To'] = EMAIL_ADMIN
            msg3.set_content(f'Aprove a troca:\n{link_email_admin}')
            smtp.send_message(msg3)

        print('emails enviados com sucesso')

    except Exception as e:
        print('ERRO AO ENVIAR EMAIL:', e)

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
    id_encontrado = False          
    for i in lista:
        if i['id_troca'] != id:
             continue
        
        id_encontrado = True

        if token == i['token_1']:
            if i['status_1'] == 'OK':
                print('já aprovado')
                return jsonify({'mensagem':'Token já aprovado anteriormente'})
            else:
                i['status_1'] = 'OK'
            print('id', id, 'token', token, 'status_1', i['status_1'])
            return jsonify({'mensagem':'Token 1 aprovado com sucesso'})

        elif token == i['token_2']:
            if i['status_2'] == 'OK':
                print('já aprovado')
                return jsonify({'mensagem':'Token já aprovado anteriormente'})
            else:
                i['status_2'] = 'OK'
            print('id', id, 'token', token, 'status_2', i['status_2'])
            return jsonify({'mensagem':'Token 2 aprovado com sucesso'})
        
        elif token == i['token_admin']:
            if i['status_admin'] == 'OK':
                print('já aprovado')
                return jsonify({'mensagem':'Token já aprovado anteriormente'})
            else:
                i['status_admin'] = 'OK'
            print('id', id, 'token', token, 'status_admin', i['status_admin'])
            return jsonify({'mensagem':'Token admin aprovado com sucesso'})      
        else:
            print('token inválido')
            return jsonify({'mensagem':'Token inválido'})
        
    if not id_encontrado:
        print('id não encontrado')
        return jsonify({'mensagem':'ID da troca não encontrado'})
app.run(debug= True)
