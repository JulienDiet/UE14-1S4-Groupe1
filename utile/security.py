from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getPrime
from random import randint
from hashlib import sha256
import utile.network as network
import pickle


def aes_encrypt(msg, key):
    """
    Fonction de chiffrement AES-GCM
    :param msg: (dict) Message au format de dictionnaire à chiffrer
    :param key: (bytes) Clé de chiffrement
    :return: (list) Liste des éléments nécessaires au déchiffrement --> [nonce, header, ciphertext, tag]
    """

def aes_decrypt(msg, key):
    """
    Fonction de déchiffrement AES-GCM
    :param msg: (list) Liste des éléments nécessaires au déchiffrement --> [nonce, header, ciphertext, tag]
    :param key: (bytes) Clé de chiffrement
    :return: (dict) Message déchiffré sous forme de dictionnaire
    """


def gen_key(size=256):
    """
    Fonction générant une clé de chiffrement
    :param size: (bits) taille de la clé à générer
    :return: (bytes) nouvelle clé de chiffrement
    """


def diffie_hellman_send_key(s_client):
    """
    Fonction d'échange de clé via le protocole de Diffie Hellman
    :param s_client: (socket) Connexion TCP du client avec qui échanger les clés
    :return: (bytes) Clé de 256 bits calculée
    """


def diffie_hellman_recv_key(s_serveur):
    """
    Fonction d'échange de clé via le protocole de Diffie Hellman
    :param s_serveur: (socket) Connexion TCP du serveur avec qui échanger les clés
    :return: (bytes) Clé de 256 bits calculée
    """
