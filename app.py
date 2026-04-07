import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ips', methods=['POST'])
def receive_ip():
    query = request.get_json(silent=True)
    received_ip = query.get('ip')

    if not query:
        return jsonify({"erro": "Corpo da requisição vazio ou Content-Type incorreto. Envie um JSON."}), 400
        
    
    if not received_ip:
        return jsonify({"erro": "O campo 'ip' é obrigatório"}), 400

    return jsonify({
        "mensagem": "Sucesso! A rota está funcionando.",
        "ip_que_voce_enviou": received_ip
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)