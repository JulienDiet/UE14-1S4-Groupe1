import socket

# Constantes
HEADERSIZE = 10
LOCAL_IP = socket.gethostname()
PORT_SERV_CLES = 8380


def start_net_serv(ip=LOCAL_IP, port=PORT_SERV_CLES):
    """
    Démarre un socket qui écoute en mode "serveur" sur ip:port
    :param ip: l'adresse ip à utiliser
    :param port: le port à utilier
    :return: le socket créé en mode "serveur"
    """


def connect_to_serv(ip=LOCAL_IP, port=PORT_SERV_CLES, retry=60):
    """
    Crée un socket qui tente de se connecter sur ip:port.
    En cas d'échec, tente une nouvelle connexion après retry secondes
    :param ip: l'adresse ip où se connecter
    :param port: le port de connexion
    :param retry: le nombre de seconde à attendre avant de tenter une nouvelle connexion
    :return: le socket créé en mode "client"
    """



def send_message(s, msg=b''):
    """
    Envoi un message sur le réseau
    :param s: (socket) pour envoyer le message
    :param msg: (dictionary) message à envoyer
    :return: Néant
    """



def receive_message(s):
    """
    Réceptionne un message sur le réseau
    :param s: (socket) pour réceptionner le message
    :return: (objet) réceptionné
    """


