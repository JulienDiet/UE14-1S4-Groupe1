from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
#from Crypto.Util.Padding import pad, unpad
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
    salt = get_random_bytes(AES.block_size)
    private_key = sha256(key + salt).digest()
    cipher = AES.new(private_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(pickle.dumps(msg))
    return [cipher.nonce, salt, ciphertext, tag]


def aes_decrypt(msg, key):
    """
    Fonction de déchiffrement AES-GCM
    :param msg: (list) Liste des éléments nécessaires au déchiffrement --> [nonce, header, ciphertext, tag]
    :param key: (bytes) Clé de chiffrement
    :return: (dict) Message déchiffré sous forme de dictionnaire
    """
    nonce, salt, ciphertext, tag = msg[0], msg[1], msg[2], msg[3]
    private_key = sha256(key + salt).digest()
    cipher = AES.new(private_key, AES.MODE_GCM, nonce)
    return pickle.loads(cipher.decrypt_and_verify(ciphertext, tag))


def gen_key(size=256):
    """
    Fonction générant une clé de chiffrement
    :param size: (bits) taille de la clé à générer
    :return: (bytes) nouvelle clé de chiffrement
    """
    return get_random_bytes(size // 8)


def diffie_hellman_send_key(s_client):
    """
    Fonction d'échange de clé via le protocole de Diffie Hellman
    :param s_client: (socket) Connexion TCP du client avec qui échanger les clés
    :return: (bytes) Clé de 256 bits calculée
    """
    prime = getPrime(256)
    generate = randint(2, prime - 2)
    a = randint(2, prime - 2)
    alice = pow(generate, a, prime)
    network.send_message(s_client, {'p': prime, 'g': generate, 'A': alice})
    bob = network.receive_message(s_client)
    key = pow(bob['B'], a, prime)
    return sha256(key.to_bytes(32, 'big')).digest()


def diffie_hellman_recv_key(s_serveur):
    """
    Fonction d'échange de clé via le protocole de Diffie Hellman
    :param s_serveur: (socket) Connexion TCP du serveur avec qui échanger les clés
    :return: (bytes) Clé de 256 bits calculée
    """
    alice = network.receive_message(s_serveur)
    prime, generate = alice['p'], alice['g']
    b = randint(2, prime - 2)
    bob = pow(generate, b, prime)
    network.send_message(s_serveur, {'B': bob})
    key = pow(alice['A'], b, prime)
    return sha256(key.to_bytes(32, 'big')).digest()


key_test = gen_key()
print(key_test)
msg_test = {'test': 'test',
            'je': 'suis',
            'pas': 'bien'}
msg_encrypted = aes_encrypt(msg_test, key_test)
print(msg_encrypted)
msg_decrypted = aes_decrypt(msg_encrypted, key_test)
print(msg_decrypted)
