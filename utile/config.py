import json
import utile.security as security
import pickle

# Variable globale
config = {}


def load_config(config_file='config/config.cfg', key_file='config/key.bin'):
    """
    Fonction permettant de charger la configuration au format JSON avec cryptage AES-GCM
    :param config_file: (str) Fichier d'enregistrement de la configuration
    :param key_file: (str) Fichier d'enregistrement de la clé de chiffrement AES-GCM
    :return: (dict) La configuration chargée
    """

def save_config(config_file='config/config.cfg', key_file='config/key.bin'):
    """
    Fonction permettant de sauvegarder la configuration au format JSON avec cryptage AES-GCM
    :param config_file: (str) Fichier d'enregistrement de la configuration
    :param key_file: (str) Fichier d'enregistrement de la clé de chiffrement AES-GCM
    :return: néant
    """

def get_config(setting):
    """
    Renvoie la valeur de la clé de configuration chargée en mémoire (voir fonction load_config ou
    configuration en construction)
    :param setting: (str) clé de configuration à retourner
    :return: valeur associée à la clé demandée
    """

def set_config(setting, value):
    """
    Initialise la valeur de la clé de configuration chargée en mémoire (voir fonction load_config ou
    configuration en construction)
    :param setting: (str) clé de configuration à retourner
    :param value: Valeur à enregistrer
    :return: Néant
    """

def print_config():
    """
    Affiche la configuration en mémoire
    :return: Néant
    """

def reset_config():
    """
    Efface la configuration courante en mémoire
    :return: Néant
    """

def remove_config(setting):
    """
    Retire un paire de clé (setting) / valeur de la configuration courante en mémoire
    :param setting: la clé à retirer du la config courante
    :return: Néant
    """

def validate(msg):
    """
    Devamnde de confirmation par O ou N
    :param msg: (str) Message à afficher pour la demande de validation
    :return: (boolean) Validé ou pas
    """
