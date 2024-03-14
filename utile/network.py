import socket
import time

# Constantes
HEADERSIZE = 10
LOCAL_IP = socket.gethostname()
PORT_SERV_CLES = 8381


def start_net_serv(ip=LOCAL_IP, port=PORT_SERV_CLES):
    """
    Démarre un socket qui écoute en mode "serveur" sur ip:port
    :param ip: l'adresse ip à utiliser
    :param port: le port à utilier
    :return: le socket créé en mode "serveur"
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Lie le socket à l'adresse et au port spécifiés
    server_socket.bind((ip, port))
    # Commence à écouter les connexions entrantes, avec une limite de 5 connexions en attente
    server_socket.listen(5)
    print(f"Serveur démarré sur {ip}:{port}")
    return server_socket




def connect_to_serv(ip=LOCAL_IP, port=PORT_SERV_CLES, retry=10):
    """
    Crée un socket qui tente de se connecter sur ip:port.
    En cas d'échec, tente une nouvelle connexion après retry secondes
    :param ip: l'adresse ip où se connecter
    :param port: le port de connexion
    :param retry: le nombre de seconde à attendre avant de tenter une nouvelle connexion
    :return: le socket créé en mode "client"
    """
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            print(f"Connected to {ip}:{port}")
            return client_socket
        except ConnectionRefusedError:
            print(f"Connection to {ip}:{port} refused. Retrying in {retry} seconds...")
            time.sleep(retry)
        except Exception as e:
            print(f"Error connecting to {ip}:{port}: {e}")
            return None


def send_message(s, msg={}):
    """
    Envoi un message sur le réseau
    :param s: (socket) pour envoyer le message
    :param msg: (dictionary) message à envoyer
    :return: Néant
    """
    if msg is None:
        msg = {}
    try:
        # Transforme le message de type dictionnaire en une séquence d'octets
        msg_bytes = bytes(str(msg), 'utf-8')

        # Envoie d'abord la longueur du message (en tant qu'en-tête de taille fixe)
        msg_length = len(msg_bytes)
        msg_length_bytes = bytes(f'{msg_length:<{HEADERSIZE}}', 'utf-8')
        s.send(msg_length_bytes)

        # Envoie ensuite le message réel
        s.send(msg_bytes)
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")


def receive_message(s):
    """
    Réceptionne un message sur le réseau
    :param s: (socket) pour réceptionner le message
    :return: (objet) réceptionné
    """
    try:
        # Recevoir d'abord la longueur du message
        msg_length_header = s.recv(HEADERSIZE)

        if not msg_length_header:
            # Si la longueur du message n'est pas reçue, cela signifie que la connexion a été fermée
            return None

        # Convertir l'en-tête de la longueur du message en un entier
        msg_length = int(msg_length_header.decode('utf-8').strip())

        # Recevoir le message réel en fonction de la longueur précédemment reçue
        msg = s.recv(msg_length)

        # Convertir le message en objet (dans ce cas, en dictionnaire)
        msg_dict = eval(msg.decode('utf-8'))

        return msg_dict
    except Exception as e:
        print(f"Erreur lors de la réception du message : {e}")
        return None


