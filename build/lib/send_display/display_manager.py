import os
import json
import argparse
from datetime import datetime

import pandas as pd
from jsonschema import validate
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests

# Importations personnalisées
from send_display.cipher import encrypt_file_contents_fernet, deciĥer_file_contents_fernet, load_key, generate_keys
from send_display.flight import Flight
from send_display.utils import schema_validation


retry_strategy = {
    'total': 3,           # Nombre total de tentatives
    'connect': 3,         # Nombre de tentatives de connexion
    'read': 3,            # Nombre de tentatives de lecture
    'backoff_factor': 0.5 # Facteur de backoff entre les tentatives (facultatif)
}



def put_with_retry(url, data=None, headers=None, retry_strategy=None):
    session = requests.Session()

    # Créer un objet Retry avec la stratégie de réessai spécifiée
    if retry_strategy:
        retry = Retry(
            total=retry_strategy['total'],
            connect=retry_strategy['connect'],
            read=retry_strategy['read'],
            backoff_factor=retry_strategy['backoff_factor']
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

    # Effectuer la requête PUT avec réessai
    response = session.put(url, data=data, headers=headers)

    return response


def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"Le fichier a été renommé de {old_name} à {new_name}")
    except FileNotFoundError:
        print(f"Le fichier {old_name} n'existe pas")
    except PermissionError:
        print(f"Permission refusée pour renommer le fichier {old_name}")
    except Exception as e:
        print(f"Une erreur s'est produite: {e}")




def rename_all(name=None):
	files  = os.listdir()
	if "customers.csv" in files and "purchases.csv" in files:
		rename_file("customers.csv", "{}_customers.csv".format(name))
		rename_file("purchases.csv", "{}_purchases.csv".format(name))
	else:
		print("file missing or already renamed")



def send_data_to_api(url=None, token="1234", flight_number=None):

        #flight_time = datetime(2024, 5, 20, 14, 30)
        flight_time = datetime.now()
        flight1 = Flight(flight_number, flight_time)
        rename_all(flight1.name)
        files = os.listdir()
        if "service.key" in files:
            key = load_key("service.key")
        else:
            generate_keys()
            key = load_key("service.key")


        customers_filename = "{}_customers.csv".format(flight1.name)
        purchases_filename = "{}_purchases.csv".format(flight1.name)


        customers_filename_bin = encrypt_file_contents_fernet(customers_filename, "customers", key)
        purchases_filename_bin = encrypt_file_contents_fernet(purchases_filename, "purchases", key)


        purchases_df  = deciĥer_file_contents_fernet(purchases_filename_bin, key)
        customers_df  = deciĥer_file_contents_fernet(customers_filename_bin, key)


        df = pd.merge(purchases_df , customers_df , on='customer_id')

        df['title'] = df['title'].replace({1: 'Female', 2: 'Male'})
        df['title'] = df['currency'].replace({"USD": 'dollars', "EUR": 'euros'})

        grouped = df.groupby('customer_id')

        body = []

        for customer_id, group_index in grouped.groups.items():
            customer = {"purchases": []}
            element = df.loc[group_index]
            customer["salutation"] = element.iloc[0]["title"]
            customer["last_name"] = element.iloc[0]["lastname"]
            customer["first_name"] = element.iloc[0]["firstname"]    
            customer["email"] = element.iloc[0]["email"] 
            for index, row in element.iterrows():
                purchase = {}
                purchase["product_id"] = row["product_id"]
                purchase["price"] = row["price"]
                purchase["currency"] = row["currency"]
                purchase["quantity"] = row["quantity"]
                purchase["purchased_at"] = row["date"]
                customer["purchases"].append(purchase)
            body.append(customer)

        try:
            validate(instance=body, schema=schema_validation)
        
        except Exception as e:
            print(e)
            return     

        # URL de l'API
        # En-têtes HTTP
        headers = {"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(token)  # Ajoutez votre token d'authentification si nécessaire
                    }

        # Conversion des données en JSON
        data = json.dumps(body)

        # Requête PUT
        # Effectuer la requête PUT avec réessai
        response = put_with_retry(url, data=json.dumps(data), headers=headers, retry_strategy=retry_strategy)

        # Vérifier le code de statut de la réponse
        if response.status_code == 200:
            print("Requête réussie :", response.json())
        else:
            print("Erreur :", response.status_code)

def main():
    parser = argparse.ArgumentParser(description='Update customer information via PUT request.')
    parser.add_argument('--url', type=str, help='API endpoint URL')
    parser.add_argument('--flight', type=str, help='FLIGHT number')
    args = parser.parse_args()
    token = os.environ['AUTH_TOKEN']
    send_data_to_api(url=args.url, token=token, flight_number=args.flight)

if __name__ == '__main__':
    main()