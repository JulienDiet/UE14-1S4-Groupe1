import socket
from datetime import datetime
import utile.network as network
import utile.message as message
'''import utile.security as security
import utile.config as config
#import utile.input as my_input'''


# Constantes
IP_SERV_CONSOLE = socket.gethostname()
PORT_SERV_CONSOLE = 8381


def affichage_menu():
    print("")
    print("============================================================================")
    print("============================================================================")
    print("1) Liste de victimes du ransomware")
    print("2) Historiques des états d'une victime")
    print("3) Renseigner le payement de rançon d'une victime")
    print("4) Quitter")


def affichage_liste_victimes():

    print("")
    print("")
    print("LISTING DES VICTIMES DU RANSOMWARE")
    print("____________________________________________________________________________")
    # Envoi de la requête
    s = network.connect_to_serv(network.LOCAL_IP, network.PORT_SERV_CLES, retry=10)
    msg = message.set_message("LIST_VICTIM_REQ")
    network.send_message(s, msg)
    response = network.receive_message(s)
    print(response)
    # Réception de la réponse
    msg = network.receive_message(s)
    if msg is None:
        print("Aucun message reçu.")
        return
    print(f"Message reçu: {msg}")
    print(f"Message de type: {message.get_message_type(msg)}")
    # Extraction des données
    data = message.get_message_data(msg)
    print(f"Data: {data}")
    # Affichage des données
    for victime in data:
        print(f"{victime['id']:<4}{victime['hash']:<12}{victime['type']:<12}{victime['disques']:<12}{victime['statut']:<10}{victime['nb_fichiers']}")



def affichage_historique_etat_victimes():
    print("")
    print("")
    print("HISTORIQUE DES ETATS D'UNE VICTIME")
    print("__________________________________")
    choix_victime = input("Entrez le numéro de la victime : ")

def affichage_payement_rancon():
    print("")
    print("")
    print("RENSEIGNER LE PAYEMENT DE RANCON D'UNE VICTIME")
    print("______________________________________________")
    choix_victime = input("Entrez le numéro de la victime : ")
    montant = input("Entrez le montant payé : ")
    date_payement = input("Entrez la date du payement : ")
    print(f"Le payement de {montant} a été enregistré pour la victime {choix_victime} le {date_payement}.")



def main():
    continuer = True
    while continuer:
        affichage_menu()
        choix_user = input("Votre choix : ")
        if choix_user == "1":
            affichage_liste_victimes()
        elif choix_user == "2":
            affichage_historique_etat_victimes()
        elif choix_user == "3":
            affichage_payement_rancon()
        elif choix_user == "4":
            print("Au revoir")
            continuer = False
        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")
    exit(0)

if __name__ == '__main__':
    main()
