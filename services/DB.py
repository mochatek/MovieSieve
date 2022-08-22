from sqlite3 import connect
from json import dumps, loads
from constants import DB_FILE


def clean_genre(genres):
    return ''.join(genre.strip().capitalize() for genre in genres.split(',') if genre.strip())

def construct_values(folder_name, data):
    return (folder_name, clean_genre(data.get('Genre', '')) or 'N/A', dumps(data))

def marshal_response(movies):
    return [{"name": folder_name, "genre": genre} for folder_name, genre in movies]

def init_db():
    conn = connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, folder_name TEXT UNIQUE, genres TEXT, data BLOB)')
    conn.commit()
    cursor.close()
    conn.close()


def insert_one(folder_name: str, data: dict):
    conn = connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO movies(folder_name, genres, data) VALUES(?, ?, ?)', construct_values(folder_name, data))
    conn.commit()
    cursor.close()
    conn.close()


def insert_many(movies: list):
    conn = connect(DB_FILE)
    cursor = conn.cursor()
    values = tuple((construct_values(folder_name, data) for folder_name, data in movies))
    cursor.executemany('INSERT INTO movies(folder_name, genres, data) VALUES(?, ?, ?)', values)
    conn.commit()
    cursor.close()
    conn.close()


def get_data(folder_name: str):
    conn = connect(DB_FILE)
    cursor = conn.cursor()
    movie_data = cursor.execute('SELECT data FROM movies WHERE folder_name=?', (folder_name,)).fetchone()[0]
    cursor.close()
    conn.close()
    return loads(movie_data)


def get_many(folder_names):
    conn = connect(DB_FILE)
    cursor = conn.cursor()
    movies = cursor.execute(
        "SELECT folder_name, genres FROM movies WHERE folder_name IN ({seq})".format(seq=','.join(['?']*len(folder_names))), tuple(folder_names)).fetchall()
    cursor.close()
    conn.close()
    return marshal_response(movies)


def insert_from(temp_db):
    conn = connect(temp_db)
    cursor = conn.cursor()
    imported_records = cursor.execute('SELECT folder_name, genres, data FROM movies').fetchall()
    cursor.close()
    conn.close()

    if len(imported_records):
        conn = connect(DB_FILE)
        cursor = conn.cursor()
        cursor.executemany('INSERT OR IGNORE INTO movies(folder_name, genres, data) VALUES(?, ?, ?)', tuple(imported_records))
        conn.commit()
        cursor.close()
        conn.close()