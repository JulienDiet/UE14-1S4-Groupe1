#import json
import utile.security as security
import pickle

# Variable globale
global config


def load_config(config_file='config/config.cfg', key_file='config/key.bin'):
    """
    Fonction permettant de charger la configuration au format JSON avec cryptage AES-GCM
    :param config_file: (str) Fichier d'enregistrement de la configuration
    :param key_file: (str) Fichier d'enregistrement de la clé de chiffrement AES-GCM
    :return: (dict) La configuration chargée
    """
    global config
    try:
        with open(key_file, 'rb') as f:
            key = f.read()
        with open(config_file, 'rb') as f:
            config = security.aes_decrypt(pickle.load(f), key)
    except FileNotFoundError:
        print("Fichiers de configuration introuvables, une nouvelle configuration va être créée")
        config = {}
    except Exception as e:
        print(f"Erreur lors du chargement de la configuration: {e}")
        config = {}
    return config


def save_config(config_file='config/config.cfg', key_file='config/key.bin'):
    """
    Fonction permettant de sauvegarder la configuration au format JSON avec cryptage AES-GCM
    :param config_file: (str) Fichier d'enregistrement de la configuration
    :param key_file: (str) Fichier d'enregistrement de la clé de chiffrement AES-GCM
    :return: néant
    """
    global config
    key = security.gen_key()
    try:
        with open(key_file, 'wb') as f:
            f.write(key)
        with open(config_file, 'wb') as f:
            pickle.dump(security.aes_encrypt(config, key), f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la configuration: {e}")


def get_config(setting):
    """
    Renvoie la valeur de la clé de configuration chargée en mémoire (voir fonction load_config ou
    configuration en construction)
    :param setting: (str) clé de configuration à retourner
    :return: valeur associée à la clé demandée
    """
    param = config.get(setting, None)
    if param is None:
        param = f"La clé {setting} n'existe pas dans la configuration courante"
    return param


def set_config(setting, value):
    """
    Initialise la valeur de la clé de configuration chargée en mémoire (voir fonction load_config ou
    configuration en construction)
    :param setting: (str) clé de configuration à retourner
    :param value: Valeur à enregistrer
    :return: Néant
    """
    config[setting] = value


def print_config():
    """
    Affiche la configuration en mémoire
    :return: Néant
    """
    for key, value in config.items():
        print(f"{key}: {value}")


def reset_config():
    """
    Efface la configuration courante en mémoire
    :return: Néant
    """
    config.clear()


def remove_config(setting):
    """
    Retire un paire de clé (setting) / valeur de la configuration courante en mémoire
    :param setting: la clé à retirer du la config courante
    :return: Néant
    """
    if setting in config:
        del config[setting]


def validate(msg):
    """
    Devamnde de confirmation par O ou N
    :param msg: (str) Message à afficher pour la demande de validation
    :return: (boolean) Validé ou pas
    """
    rep = input(msg).upper()
    while rep != 'O' and rep != 'N':
        rep = input("Réponse invalide, veuillez répondre par O ou N: ").upper()
    return True if rep == 'O' else False

