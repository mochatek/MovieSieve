from dotenv import get_key
from os.path import join, dirname, realpath, expanduser
from datetime import date

ROOT_PATH = dirname(realpath(__file__))
ENV_FILE = join(ROOT_PATH, 'web', '.env')
APP_ICON = join(ROOT_PATH, 'web', 'favicon.ico')
DOWNLOADS_PATH = join(expanduser('~'), 'Downloads')
POSTER_PATH = join(ROOT_PATH, 'web', 'Posters')
DB_PATH = join(ROOT_PATH, 'web', 'movies.db')
TEMP_PATH = join(ROOT_PATH, 'web', 'temp')
EXPORT_NAME = join(DOWNLOADS_PATH, f'MovieSieve_{date.today()}.ms')

API_ENDPOINT = 'http://www.omdbapi.com/'
API_KEY = get_key(ENV_FILE, 'API_KEY')
REQUIRED_MOVIE_PROPS = ['Rated', 'Genre', 'Released', 'Runtime', 'Director', 'Writer',
                        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'imdbRating']