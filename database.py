import sqlite3

DB_NAME = 'database.db'

conn = sqlite3.connect(DB_NAME)

# conn.cursor().execute('''
# CREATE TABLE IF NOT EXISTS users
#     (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL,
#         email TEXT UNIQUE NOT NULL,
#         address TEXT NOT NULL,
#         phone TEXT NOT NULL
#     )
# ''')
conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
