# Définition des messages
# List_victim messages
LIST_VICTIM_REQ = {'LIST_REQ': None} # Exemple, suite à compléter
LIST_VICTIM_RESP = {}
LIST_VICTIM_END = {}

# history messages
HISTORY_REQ = {}
HISTORY_RESP = {}
HISTORY_END = {}

# change_state message
CHANGE_STATE = {}

# initialize message
INITIALIZE_REQ = {}
INITIALIZE_KEY = {}
INITIALIZE_RESP = {}

# message_type
MESSAGE_TYPE = {
    'LIST_REQ': 'LIST_VICTIM_REQ',
    # à compléter
}


def set_message(select_msg, params=None):
    """
    Retourne le dictionnaire correspondant à select_msg et le complète avec params si besoin.
    :param select_msg: le message à récupérer (ex: LIST_VICTIM_REQ)
    :param params: les éventuels paramètres à ajouter au message
    :return: le message sous forme de dictionnaire
    """
    if select_msg.upper() == 'LIST_VICTIM_REQ':
        return LIST_VICTIM_REQ

    # à compléter

def get_message_type(message):
    """
    Récupère le nom correspondant au type de message (ex: le dictionnaire LIST_VICTIM_REQ retourne 'LIST_REQ')
    :param message: le dictionnaire représentant le message
    :return: une chaine correspondant au nom du message comme définit par le protocole
    """
