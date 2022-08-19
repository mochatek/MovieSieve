import eel
from os import listdir
from os.path import join, isdir, basename
from zipfile import ZipFile, ZIP_DEFLATED
from tkinter import Tk, filedialog
from services.API import fetch_movies, save_poster, run_async
from services.DB import init_db, insert_one, insert_many, get_data, get_many
from constants import APP_ICON, DB_PATH, DOWNLOADS_PATH, EXPORT_NAME, POSTER_PATH, ROOT_PATH

init_db()

def init_progress(total: int, remaining: int):
    completed = total - remaining

    def update_progress():
        nonlocal completed
        # eel.update_progress(completed * 100 / total)
        completed += 1

    return update_progress


eel.init('web')


@eel.expose
def browse_movie_directory() -> str:
    """
        Open dialog for browsing movie directory.
        Default is `Downloads` directory.

        :return: Movie directory path
    """
    root = Tk()
    root.iconbitmap(APP_ICON)
    root.attributes("-topmost", True)
    root.withdraw()

    movie_directory = filedialog.askdirectory(
        initialdir=DOWNLOADS_PATH, title="Select Movie Directory")
    return movie_directory


@eel.expose
def add_movie(folder_name: str, data: dict, poster_url: str) -> bool:
    """
        Add movie details to DB and save poster if available.
        :param str folder_name: Name of the movie folder => `Name (Year)`
        :param dict data: Movie details
        :param str poster_url: URL of the movie poster
        :return: {folder_name, genres}
    """
    insert_one(folder_name, data)
    try:
        run_async(save_poster, folder_name, poster_url)
    except Exception as error:
        print('ADD MOVIE ERROR : ', error)
    finally:
        return {'name': folder_name, 'genre': data.get('Genre')}


@eel.expose
def get_movies(movie_directory: str) -> dict:
    """
        Find those movies from the given path, whose details are not in db. Then add details for those movies to the db.
        Once the above process has been completed. Return the list of all movies in the path along with errors if any.
        :param str movie_directory: Path of the movie folder
        :return: dict {movies, errors}
    """

    all_movies = [folder_name for folder_name in listdir(movie_directory) if isdir(join(movie_directory, folder_name))]
    result_movies = get_many(all_movies)
    available_movies = (movie["name"] for movie in result_movies)
    missing_movies = set(all_movies).difference(set(available_movies))

    if missing_movies:
        update_progress = init_progress(len(all_movies), len(missing_movies))
        movies = run_async(fetch_movies, missing_movies, update_progress)

        fetched_movies = []

        for movie in movies:
            folder_name = movie.get('name')
            data = movie.get('data')
            if not data:
                result_movies.append({"name": folder_name, "genre": 'N/A'})
            else:
                fetched_movies.append((folder_name, data))
                result_movies.append({"name": folder_name, "genre": data.get('Genre')})

        insert_many(fetched_movies)

    return result_movies


@eel.expose
def get_movie_data(folder_name: str) -> list:
    """
        Get details of the requested movie
        :param str folder_name: Folder name of the movie => `Name (Year)`
    """
    return get_data(folder_name)


@eel.expose
def export_data():
    """
        Export posters and db as zip(.ms) file to the downloads directory
    """
    try:
        with ZipFile(EXPORT_NAME, 'w', ZIP_DEFLATED) as zip_file:
            zip_file.write(DB_PATH, basename(DB_PATH))
            for poster_name in listdir(POSTER_PATH):
                zip_file.write(join(POSTER_PATH, poster_name), join(basename(POSTER_PATH), poster_name))
    except Exception as error:
        print('EXPORT ERROR : ', error)
        return False
    else:
        return DOWNLOADS_PATH


@eel.expose
def import_data():
    """
        Extract .ms file and load posters and db
    """
    try:
        root = Tk()
        root.iconbitmap(APP_ICON)
        root.attributes("-topmost", True)
        root.withdraw()

        export_file = filedialog.askopenfilename(
            defaultextension='.ms', filetypes=[('MovieSieve file', '*.ms')], initialdir=DOWNLOADS_PATH, title="Select Export File")

        if export_file and export_file.endswith('.ms'):
            with ZipFile(export_file, 'r') as zip_file:
                zip_file.extractall(join(ROOT_PATH, 'web'))
    except Exception as error:
        print('EXPORT ERROR : ', error)
        return False
    else:
        return export_file

eel.start('index.html')


# python -m eel MovieSieve.py web --onefile --noconsole --icon=favicon.ico