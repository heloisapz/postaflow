import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:5000/api/enviar')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def proxy_enviar():
    """
    Recebe os dados da tela e faz o encaminhamento para o backend.
    """
    dados_usuario = request.get_json()
    
    try:
        resposta = requests.post(BACKEND_URL, json=dados_usuario, timeout=5)
        return (jsonify(resposta.json()), resposta.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao contactar o backend: {e}")
        return jsonify({"erro": "Não foi possível comunicar com o serviço de backend"}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)