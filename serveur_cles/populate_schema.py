import string
import random
import time
import sqlite3
from datetime import datetime
fake_victims = []
fake_histories = {1: [], 2: [], 3: [], 4: []}
# Supposons que le module utile.data contient des fonctions nécessaires
from utile.data import connect_db, insert_data

def simulate_key(length=0):
    letters = ".éèàçùµ()[]" + string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def simulate_hash(length=0):
    letters = string.hexdigits
    return ''.join(random.choice(letters) for i in range(length))

def generate_fake_victims(num_victims):
    for _ in range(num_victims):
        os = simulate_key(10)
        hash = simulate_hash(64)
        disks = simulate_key(10)
        key = simulate_key(32)
        fake_victims.append((os, hash, disks, key))

def generate_fake_history(fake_histories, num_records, table_name):
    for victim_id in range(1, len(fake_victims) + 1):
        for _ in range(num_records):
            datetime_entry = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if table_name == 'states':
                state = random.choice(['infected', 'decrypted'])
                fake_histories[victim_id].append((victim_id, datetime_entry, state))
            else:  # 'decrypted' or 'encrypted'
                nb_files = random.randint(1, 100)
                fake_histories[victim_id].append((victim_id, datetime_entry, nb_files))

def main():
    # Connexion à la base de données
    conn = connect_db()

    # Génération de données factices pour la table 'victims'
    generate_fake_victims(4)  # Générer 4 victimes factices

    # Insertion des données factices dans la table 'victims'
    for victim in fake_victims:
        insert_data(conn, 'victims', ['os', 'hash', 'disks', 'key'], victim)

    # Génération et insertion des données factices pour les tables 'decrypted', 'states', 'encrypted'
    for table_name in ['decrypted', 'states', 'encrypted']:
        generate_fake_history(fake_histories, 5, table_name)  # Générer 5 enregistrements par victime

        # Insertion des données factices dans la base de données
        for victim_id, histories in fake_histories.items():
            for history in histories:
                if table_name == 'states':
                    insert_data(conn, table_name, ['id_victim', 'datetime', 'state'], history)
                else:  # 'decrypted' or 'encrypted'
                    insert_data(conn, table_name, ['id_victim', 'datetime', 'nb_files'], history)

    # Fermeture de la connexion à la base de données
    conn.close()

if __name__ == '__main__':
    main()
