from dotenv import load_dotenv
from os import getenv, path
from datetime import date
load_dotenv()

ROOT_PATH = path.dirname(path.realpath(__file__))
APP_ICON = path.join(ROOT_PATH, 'web', 'favicon.ico')
DOWNLOADS_PATH = path.join(path.expanduser('~'), 'Downloads')
POSTER_PATH = path.join(ROOT_PATH, 'web', 'Posters')
DB_PATH = path.join(ROOT_PATH, 'web', 'movies.db')
EXPORT_NAME = path.join(DOWNLOADS_PATH, f'MovieSieve_{date.today()}.ms')

API_ENDPOINT = 'http://www.omdbapi.com/'
API_KEY = getenv('API_KEY')
REQUIRED_MOVIE_PROPS = ['Rated', 'Genre', 'Released', 'Runtime', 'Director', 'Writer',
                        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'imdbRating']
