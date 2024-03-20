import string
import random
import hashlib, json, time

from datetime import datetime, timedelta
fake_victims = []
fake_histories = {1: [], 2: [], 3: [], 4: []}
from utile.data import connect_db, insert_data

#respect format suivant :
#table victims :
    # id → int ; id du ransomware enregistré en DB du serveur de clés
    # Os → string ;type de système victime "Windows" / "Linux" / "MacOS"
    # hash → string ;256 lettres / chiffres (pour le SHA256)
    # key → string ;512 caractères imprimables pour la clé de chiffrement
    # disk → list ;['C:', 'D:',...]

#table states :
    # id_states → int ;id de l'état
    # id_victim → int ;id de la victime
    # state → string ;« INITIALIZE » / « CRYPT » / « PENDING » / « DECRYPT » / « PROTECTED »
    # datetime : timestamp → int ;nombre de seconde depuis le 01/01/1970 à 00:00:00

#table encrypted :
    # id_encrypted → int ;id de l'état
    # id_victim → int ;id de la victime
    # datetime → int ;timestamp
    # nb_files → int ;nombre de fichiers chiffrés

#table decrypted :
    # id_decrypted → int ;id de l'état
    # id_victim → int ;id de la victime
    # datetime → int ;timestamp
    # nb_files → int ;nombre de fichiers déchiffrés
#_____________________________________________________
    # frequency → int ;fréquence d'émission en seconde
    # type → string ;type de système victime "WORKSTATION" / "SERVEUR"
    # message → string ;message envoyé pour rapporter le statut de déchiffrement
    # paths → list ;['\Users\*\Documents\*\', '\test\*\', '\temp\',...]
    # file_ext → list ;['.jpg', '.png', '.docx', '.xlsx', '.pptx', '.pdf', '.pst', '.ost']

def generer_victimes(n):
    for _ in range(n):
        os = random.choice(["Windows", "Linux", "MacOS"])
        hash = hashlib.sha256(str(random.random()).encode()).hexdigest()
        key = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=512))
        disks = json.dumps(random.sample(['C:', 'D:', 'E:', 'F:'], k=random.randint(1, 4)))
        yield (os, hash, disks, key)


def generer_etats(id_victimes):
    # Mise à jour de la liste pour s'arrêter à 'PENDING'
    etats_progressifs = [
        "INITIALIZE",
        "CRYPT",
        "PENDING"
    ]
    for id_victim in id_victimes:
        # Initialisation du timestamp de départ pour la séquence
        datetime_debut = int(time.time())

        for etat in etats_progressifs:
            etats = {
                "INITIALIZE": 1,
                "CRYPT": 2,
                "PENDING": 3
            }
            id_state = etats[etat]
            # Générer le timestamp pour chaque état, en incrémentant pour simuler le passage du temps
            datetime_ = datetime_debut
            yield (id_state, id_victim, datetime_, etat)

            # Incrémenter le timestamp de départ pour le prochain état
            # Cet incrément reflète le temps passé entre les états
            datetime_debut += 1034

def generer_encrypted_decrypted(id_victimes):
    for id_victim in id_victimes:
        datetime_ = int(time.time())  # Timestamp actuel
        nb_files = random.randint(1, 1000)  # Nombre de fichiers entre 1 et 1000
        yield (id_victim, datetime_, nb_files)


def inserer_victimes(conn, victimes):
    for victime in victimes:
        insert_data(conn, 'victims', ['os', 'hash', 'disks', 'key'], victime)


def inserer_etats(conn, etats):
    for etat in etats:
        insert_data(conn, 'states', ['id_states', 'id_victim', 'datetime', 'state'], etat)




def inserer_encrypted_decrypted(conn, donnees, table):
    # Les colonnes auto-incrémentées ne doivent pas être incluses
    items = ['id_victim', 'datetime', 'nb_files']

    for donnee in donnees:
        insert_data(conn, table, items, donnee)

def recuperer_id_victimes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id_victim FROM victims")
    return [row[0] for row in cursor.fetchall()]


def recuperer_id_victimes_par_etat(conn, etat):
    cursor = conn.cursor()
    cursor.execute("SELECT id_victim FROM states WHERE state = ?", (etat,))
    return [row[0] for row in cursor.fetchall()]

def generation_data_complet():
    conn = connect_db()
    # Génération et insertion des victimes
    victimes = list(generer_victimes(10))
    inserer_victimes(conn, victimes)


    # Récupération des ID des victimes (comme précédemment)
    id_victimes = recuperer_id_victimes(conn)
    # Génération et insertion des états
    etats = list(generer_etats(id_victimes))
    inserer_etats(conn, etats)

    # Après avoir inséré les états
    id_victimes_crypt = recuperer_id_victimes_par_etat(conn, "CRYPT")
    id_victimes_decrypt = recuperer_id_victimes_par_etat(conn, "DECRYPT")

    # Génération et insertion pour encrypted et decrypted en utilisant ces listes filtrées d'ID
    donnees_encrypted = list(generer_encrypted_decrypted(id_victimes_crypt))
    donnees_decrypted = list(generer_encrypted_decrypted(id_victimes_decrypt))

    inserer_encrypted_decrypted(conn, donnees_encrypted, "encrypted")
    inserer_encrypted_decrypted(conn, donnees_decrypted, "decrypted")

    print("Données insérées avec succès.")
    conn.close()

def main():
    generation_data_complet()

if __name__ == '__main__':
    main()
