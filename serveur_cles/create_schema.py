import os
import sqlite3

# Chemin absolu vers le répertoire contenant ce script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemins absolus vers la base de données et le fichier de schéma
DB_PATH = os.path.join(BASE_DIR, './data/victims.sqlite')
SCHEMA_PATH = os.path.join(BASE_DIR, './script/victims_schema.sql')

# S'assurer que le répertoire 'data' existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
with sqlite3.connect(DB_PATH) as conn:
    # Vérification si le fichier de schéma SQL existe
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Le fichier de schéma SQL '{SCHEMA_PATH}' est introuvable.")

    print('Creating schema')
    # Lecture et exécution du script SQL pour créer le schéma de base de données
    with open(SCHEMA_PATH, 'rt', encoding='utf-8') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    print('Schema created successfully')

print('Database and schema setup is complete.')