from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import pandas as pd
import io 
from send_display.utils import dtype_dict_customer, schema_validation


def deciĥer_file_contents_fernet(input_file, key):
    try:

        # Lire le contenu du fichier chiffré
        with open(input_file, "rb") as f:
            encrypted_contents = f.read()

        # Déchiffrer le contenu du fichier
        decrypted_contents = key.decrypt(encrypted_contents)
        data_stream = io.StringIO(decrypted_contents.decode('utf-8'))
        if input_file == "customers.bin":
            df = pd.read_csv(data_stream, sep=";", header=0, dtype=dtype_dict_customer, keep_default_na="")
        else:
            df = pd.read_csv(data_stream, sep=";", header=0, keep_default_na="")
        print(f"Le contenu du fichier a été déchiffré avec succès.")

    except Exception as e:
        print("Une erreur s'est produite lors du déchiffrement du contenu du fichier :", e)

    return df 


def encrypt_file_contents_fernet(input_file, prefix, key):
    try:
        # Créer un objet Fernet avec la clé fournie
        # Lire le contenu du fichier d'entrée
        with open(input_file, "rb") as f:
            file_contents = f.read()

        # Chiffrer le contenu du fichier
        encrypted_contents = key.encrypt(file_contents)


        print("content", encrypted_contents)
        # Écrire le contenu chiffré dans un fichier de sortie
        output_file = f"{prefix}.bin"
        with open(output_file, "wb") as f:
            f.write(encrypted_contents)

        print(f"Le contenu du fichier a été chiffré et écrit dans {output_file} avec succès.")
    except Exception as e:
        print("Une erreur s'est produite lors du chiffrement du contenu du fichier :", e)
    return output_file


def generate_keys():
    key = Fernet.generate_key()
    f = Fernet(key)
    # store the key to use later for decryption
    with open('service.key', 'wb') as f:
        f.write(key)



def load_key(key_file):
    try:
        # Charger la clé depuis le fichier ou la fournir directement
        with open(key_file, "rb") as f:
            key = f.read()

        # Créer un objet Fernet avec la clé chargée
        fernet = Fernet(key)

        print("Clé chargée avec succès.")
        return fernet
    except Exception as e:
        print("Une erreur s'est produite lors du chargement de la clé :", e)
        return None