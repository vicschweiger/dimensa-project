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
app.json.sort_keys = False

@app.route('/ips', methods=['POST'])
def receive_ip():
    query = request.get_json(silent=True)
    received_ip = query.get('ip')

    if not query:
        return jsonify({"erro": "Corpo da requisição vazio."}), 400
        
    
    if not received_ip:
        return jsonify({"erro": "O campo 'ip' está vazio."}), 400
    
    saved_ip = ips_collection.find_one({"ip": received_ip})

    if saved_ip:
        return jsonify({"mensagem": f"O IP {received_ip} já existe no banco de dados."}), 200
    
    try:
        api_response = requests.get(f"https://ipwhois.app/json/{received_ip}")
        raw_data = api_response.json()
        
        if raw_data.get("success") is False:
             return jsonify({"erro": f"IP {received_ip} inválido ou não encontrado na API externa."}), 404

        cleared_data = {
            "ip": received_ip,
            "raw_data": raw_data,
            "data": {
                "type": raw_data.get("type"),
                "continent": raw_data.get("continent"),
                "continent_code": raw_data.get("continent_code"),
                "country": raw_data.get("country"),
                "country_code": raw_data.get("country_code"),
                "region": raw_data.get("region"),
                "region_code": raw_data.get("region_code"),
                "city": raw_data.get("city"),
                "capital": raw_data.get("capital") 
            }
        }

        ips_collection.insert_one(cleared_data)
        
        del cleared_data["_id"]

        return jsonify(cleared_data), 201
        
    except Exception as e:
        return jsonify({"erro": f"Erro de conexão com a API externa: {str(e)}"}), 500



@app.route('/ips', methods=['GET'])
def list_ips():
    page = request.args.get('page', 1, type=int)
    filter_ip = request.args.get('filter_ip', type=str)
    
    limit = 15
    gap = (page - 1) * limit
    
    query = {}

    if filter_ip:
        query["ip"] = {"$regex": f"^{filter_ip}"}
        
    db_results = ips_collection.find(query, {"_id": 0, "raw_data": 0}).skip(gap).limit(limit)
    
    ips_list = []
    for item in db_results:
        ips_list.append(item)
        
    return jsonify({
        "ips": ips_list
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)