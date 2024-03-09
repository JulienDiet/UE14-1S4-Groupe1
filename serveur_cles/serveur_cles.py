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

    # Attendre une connexion
    print("En attente de connexion...")
    network.connect_to_serv(network.LOCAL_IP,network.PORT_SERV_CLES,retry=10)
    print(f"Connexion de {network.LOCAL_IP} sur le port {network.PORT_SERV_CLES} acceptée")
    print("En attente de messages...")
    while True:
        client_socket, address = socket_server.accept()
        print(f"Connexion de {address} établie")
        msg = network.receive_message(client_socket)
        if msg is None:
            print("Aucun message reçu, connexion fermée.")
            client_socket.close()
            continue  # Skip further processing and wait for the next connection
        print(f"Message reçu: {msg}")
        print(f"Message de type: {message.get_message_type(msg)}")
        response_message = message.set_message(message.get_message_type(msg))
        if response_message is not None:
            print(f"Envoi d'un message de type {message.get_message_type(msg)}")
            network.send_message(client_socket, response_message)
            print("Message envoyé")
        else:
            print("Aucun message à envoyer.")
        client_socket.close()
        print("Connexion fermée")


if __name__ == '__main__':
    main()
