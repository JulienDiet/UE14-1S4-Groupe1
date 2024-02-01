import os
import sqlite3

DB_FILENAME = 'data/victims.sqlite'
SCHEMA_FILENAME = 'script/victims_schema.sql'

db_is_new = not os.path.exists(DB_FILENAME)

with sqlite3.connect(DB_FILENAME) as conn:
    if db_is_new:
        print('Creating schema')
        with open(SCHEMA_FILENAME, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)