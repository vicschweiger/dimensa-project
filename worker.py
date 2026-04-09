import os, requests
from dotenv import load_dotenv
from pymongo import MongoClient
from celery import Celery
from celery.schedules import crontab

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.dimensa_project
ips_collection = db.ips

celery_app = Celery('dimensa_tasks', broker=os.getenv("CELERY_BROKER_URL"))
celery_app.conf.timezone = 'America/Sao_Paulo'

celery_app.conf.beat_schedule = {
    'fetch_and_update_ip_data_every_12_hours': {
        'task': 'fetch_and_update_ip_data',
        'schedule': crontab(hour='*/12', minute=0),
    },
}

@celery_app.task(name='fetch_and_update_ip_data')
def fetch_and_update_ip_data():
    print("Iniciando tarefa de atualizacao de dados IP...")
    ips = ips_collection.find()
    
    for item in ips:
        ip_address = item.get('ip')
        
        try:
            api_response = requests.get(f"https://ipwhois.app/json/{ip_address}")
            raw_data = api_response.json()
            
            if raw_data.get("success") is not False:
                new_data = {
                "ip": raw_data.get("ip"),
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

                ips_collection.update_one(
                    {"ip": ip_address}, 
                    {"$set": new_data}
                )

            print(f"Dados do IP {ip_address} atualizados com sucesso.")
        
        except Exception as e:
            print(f"Erro ao atualizar dados do IP {ip_address}: {str(e)}")

    return "Tarefa de atualizacao de dados IP concluida."