import eel
from os import listdir
from os.path import join, isdir, basename, dirname
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED
from tkinter import Tk, filedialog
from services.API import fetch_movies, save_poster, search_by_imdbId, run_async
from services.DB import init_db, insert_one, insert_many, get_data, get_many, import_from
from constants import APP_ICON, DB_PATH, DOWNLOADS_PATH, EXPORT_NAME, POSTER_PATH, TEMP_PATH

init_db()

def init_progress(total: int, remaining: int):
    completed = total - remaining

    def update_progress():
        nonlocal completed
        completed += 1
        eel.update_progress(completed * 100 / total)()

    return update_progress


def openDialog(type: str, title: str):
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    root.iconbitmap(APP_ICON)
    root.attributes("-topmost", True)

    if type == 'folder':
        return filedialog.askdirectory(
            initialdir=DOWNLOADS_PATH, title=title)
    elif type == 'file':
        return filedialog.askopenfilename(
            defaultextension='.ms', filetypes=[('MovieSieve file', '*.ms')], initialdir=DOWNLOADS_PATH, title=title)

eel.init('web')


@eel.expose
def browse_movie_directory() -> str:
    """
        Open dialog for browsing movie directory.
        Default is `Downloads` directory.

        :return: Movie directory path
    """
    return openDialog('folder', "Select Movie Directory")


@eel.expose
def search_imdbId(imdb_id: str):
    """
        Retrieve movie data by searching for imdb_id
        :param str imdb_id: IMDb Id of the movie
    """
    return run_async(search_by_imdbId, imdb_id)

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

    result_movies.sort(key = lambda movie: movie['name'])
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
        Export posters and db as zip(.ms) file to the chosen directory
    """
    try:
        export_folder = openDialog("folder", "Select Export Folder")

        if export_folder:
            with ZipFile(join(export_folder, EXPORT_NAME), 'w', ZIP_DEFLATED) as zip_file:
                zip_file.write(DB_PATH, basename(DB_PATH))
                for poster_name in listdir(POSTER_PATH):
                    zip_file.write(join(POSTER_PATH, poster_name), join(basename(POSTER_PATH), poster_name))

            return {"message": 'Export Successful', "status": 'success'}
        return {"message": 'Export Cancelled', "status": 'cancel'}
    except Exception as error:
        print('EXPORT ERROR : ', error)
        return {"message": 'Export Failed', "status": 'error'}


@eel.expose
def import_data():
    """
        Extract .ms file and load posters and db
    """
    try:
        export_file = openDialog("file", "Select Export File")

        if export_file and export_file.endswith('.ms'):
            with ZipFile(export_file, 'r') as zip_file:
                for item in zip_file.namelist():
                    if item.startswith('Posters/'):
                        zip_file.extract(item, dirname(POSTER_PATH))
                    elif item == 'movies.db':
                        zip_file.extract(item, TEMP_PATH)

            import_from(join(TEMP_PATH, 'movies.db'))
            rmtree(TEMP_PATH)

            return {"message": 'Import Successful', "status": 'success'}
        return {"message": 'Import Cancelled', "status": 'cancel'}

    except Exception as error:
        print('IMPORT ERROR : ', error)
        return {"message": 'Import Failed', "status": 'error'}


eel.start('index.html')


# python -m eel MovieSieve.py web --onefile --noconsole --icon=favicon.ico