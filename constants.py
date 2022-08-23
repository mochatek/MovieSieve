import sys
from os.path import join, dirname, abspath, expanduser
from datetime import date
from dotenv import get_key

if getattr(sys, 'frozen', False):
    EXE_PATH = abspath(dirname(sys.executable))
elif __file__:
    EXE_PATH = abspath(dirname(__file__))
APP_DATA_FILE = join(EXE_PATH, 'MovieSieve.data')

DATA_PATH = getattr(sys, '_MEIPASS', abspath(dirname(__file__)))
DOWNLOADS_PATH = join(expanduser('~'), 'Downloads')
WEB_PATH = join(DATA_PATH, 'web')
POSTER_PATH = join(WEB_PATH, 'Posters')
TEMP_PATH = join(WEB_PATH, 'temp')
ENV_FILE = join(WEB_PATH, '.env')
ICON_FILE = join(WEB_PATH, 'favicon.ico')
SPLASH_FILE = join(WEB_PATH, 'splash.png')
DB_FILE = join(WEB_PATH, 'movies.db')
EXPORT_NAME = f'MovieSieve_{date.today()}.ms'

API_ENDPOINT = 'http://www.omdbapi.com/'
API_KEY = get_key(ENV_FILE, 'API_KEY')
REQUIRED_MOVIE_PROPS = ['Rated', 'Genre', 'Released', 'Runtime', 'Director', 'Writer',
                        'Actors', 'Plot', 'Language', 'Country', 'Awards', 'imdbRating']

CHROME_FLAGS = ['--disable-sync', '--incognito', '--no-experiments', '--disable-background-mode']