import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.dimensa_project
ips_collection = db.ips

app = Flask(__name__)

@app.route('/ips', methods=['POST'])
def receive_ip():
    query = request.get_json(silent=True)
    received_ip = query.get('ip')

    if not query:
        return jsonify({"erro": "Corpo da requisição vazio."}), 400
        
    
    if not received_ip:
        return jsonify({"erro": "O campo 'ip' está vazio."}), 400
    
    ips_collection.insert_one({"ip": received_ip})  

    return jsonify({
        "mensagem": "Sucesso! O banco de dados foi conectado e salvou o IP corretamente.",
        "ip_que_voce_enviou": received_ip
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)