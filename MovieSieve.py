import eel
from requests import get
from os import path, listdir
from json import loads, dumps
import sqlite3
import tkinter
import tkinter.filedialog as filedialog


# Constants
ROOT = path.dirname(path.realpath(__file__))


def retrieve_data(movie):
    """
        Parses the movie name, year and retrieve movie details from OMDb API
        :param str movie: Name of the folder in 'Name (Year)' format
        :return: Movie details if possible, else None
    """
    try:
        uri = 'http://www.omdbapi.com/'
        key = '4048f127'

        name, year = movie.split('(')
        name = name.strip()
        year = year.replace(')', '').strip()

        params = {
            't': name,
            'y': year,
            'plot': 'full',
            'apikey': key
        }

        response = get(uri, params=params)
        data = response.json()

        if 'Error' in data:
            return None

        poster_url = data['Poster']
        # Download poster if available
        if poster_url != 'N/A':
            filename = '{}.jpg'.format(movie)
            response = get(poster_url)
            with open(path.join(ROOT, 'web', 'posters', filename), 'wb') as file:
                file.write(response.content)

        # Extract only the eeded movie attributes
        needed_keys = ['Rated', 'Genre', 'Released', 'Runtime', 'Director', 'Writer',
                    'Actors', 'Plot', 'Language', 'Country', 'Awards', 'imdbRating']
        data = {key: value for key, value in data.items() if key in needed_keys}

        return data
    except:
        # When no internet connection is available
        return 0


eel.init('web')


@eel.expose
def browse_movie_folder():
    """
        Open folder dialog in user's Downloads folder by default
        :return: Path of selected folder
    """
    root = tkinter.Tk()
    root.iconbitmap(path.join(ROOT, 'web', 'favicon.ico'))
    root.attributes("-topmost", True)
    root.withdraw()

    home = path.expanduser('~')
    folder_path = filedialog.askdirectory(initialdir=path.join(home, 'Downloads'), title="Select Movie Folder")
    return folder_path


@eel.expose
def add_movie(movie, data, poster_url):
    """
        Add movie to DB
        :param str movie: Movie name
        :param dict data: Movie details
        :param str poster_url: URL of the poster
        :return: status
    """
    try:
        genres = data['Genre']
        conn = sqlite3.connect(path.join(ROOT, 'web', 'movies.db'))
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO movies(folder_name, genres, data) VALUES(?, ?, ?)', (movie, genres, dumps(data)))
        conn.commit()
        cursor.close()
        conn.close()
    except:
        return False

    # Download poster if possible
    try:
        filename = '{}.jpg'.format(movie)
        response = get(poster_url)
        if response.status_code == 200:
            with open(path.join(ROOT, 'web', 'posters', filename), 'wb') as file:
                file.write(response.content)
    except:
        pass

    return True


@eel.expose
def get_movies(folder_path):
    """
        Find those movies from the given path, whose details are not in db. Then add details for those movies to the db.
        Once the above process has been completed. Return the list of all movies in the path along with errors if any.
        :param str folder_path: Path of the movie folder
        :return: dict {movies, errors}
    """

    # List of movies, for which info couldn't be found
    errors = []

    # Movies in Root
    movies_in_root = listdir(folder_path)
    if __file__ in movies_in_root:
        movies_in_root.remove(__file__)

    conn = sqlite3.connect(path.join(ROOT, 'web', 'movies.db'))
    cursor = conn.cursor()

    # Movies in DB
    records = cursor.execute(
        f'SELECT folder_name, genres FROM movies WHERE folder_name IN {tuple(movies_in_root)} ORDER BY folder_name').fetchall()
    movies_in_db = [record[0] for record in records]

    # Movies not added in DB
    movies_missing = set(movies_in_root).difference(set(movies_in_db))

    # Update progress
    total_count = len(movies_in_root)
    processed_count = total_count - len(movies_missing)
    completion_percentage = (processed_count / total_count) * 100
    eel.update_progress(completion_percentage)

    # If there are missing movies
    if movies_missing:
        # Try to retrieve details of missing movies
        for index, movie in enumerate(movies_missing):
            movie_data = retrieve_data(movie)

            #  If no internet, then add remainings movies to errors and terminate
            if movie_data == 0:
                errors.extend(list(movies_missing)[index:])
                eel.update_progress(100)
                break

            # Add to DB if retrieved
            if movie_data:
                genres = movie_data['Genre']
                cursor.execute(
                    'INSERT INTO movies(folder_name, genres, data) VALUES(?, ?, ?)', (movie, genres, dumps(movie_data)))
                conn.commit()

            else:
                # Add to errors in case of error
                errors.append(movie)

            # Update progress
            processed_count += 1
            completion_percentage = (processed_count / total_count) * 100
            eel.update_progress(completion_percentage)

        records = cursor.execute(
            f'SELECT folder_name, genres FROM movies WHERE folder_name IN {tuple(movies_in_root)} ORDER BY folder_name').fetchall()

    # Close cursor and Connection
    cursor.close()
    conn.close()

    return {
        'movies': records, 'errors': errors
    }


@eel.expose
def get_movie_data(movie):
    """
        Get details of the requested movie
        :param str movie: Folder name of the movie => Name (Year)
        :return: [Movie, Movie details(JSON), Cache-control]
    """
    conn = sqlite3.connect(path.join(ROOT, 'web', 'movies.db'))
    cursor = conn.cursor()
    data = cursor.execute(
        'SELECT data FROM movies WHERE folder_name=?', (movie,)).fetchone()[0]
    cursor.close()
    conn.close()

    return [movie, loads(data), False]


eel.start('index.html')
