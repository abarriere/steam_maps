import sqlite3

def init_db():
    """
    Initialise la base de données SQLite en créant la table `saved_places` si elle n'existe pas.
    """
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gid TEXT UNIQUE,
            latitude TEXT,
            longitude TEXT,
            name TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_places(places):
    """
    Enregistre une liste de lieux dans la base de données.
    :param places: Liste de tuples (gid, latitude, longitude, name, address)
    """
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT OR IGNORE INTO saved_places (gid, latitude, longitude, name, address)
        VALUES (?, ?, ?, ?, ?)
    """, places)
    conn.commit()
    conn.close()

def load_places():
    """
    Charge tous les lieux enregistrés dans la base de données.
    :return: Liste de tuples (gid, latitude, longitude, name, address)
    """
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("SELECT gid, latitude, longitude, name, address FROM saved_places")
    data = cursor.fetchall()
    conn.close()
    return data

def delete_place(gid):
    """
    Supprime un lieu de la base de données en fonction de son GID.
    :param gid: Identifiant unique du lieu (GID)
    """
    conn = sqlite3.connect("places.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_places WHERE gid = ?", (gid,))
    conn.commit()
    conn.close()