from os import name as Platform
from os.path import join
from typing import Callable, List
from aiohttp import ClientSession
from aiofiles import open
from asyncio import run, gather, Lock
from constants import API_ENDPOINT, API_KEY, POSTER_PATH, REQUIRED_MOVIE_PROPS


def generate_api_params(folder_name: str):
    name, year = map(lambda x: x.replace(')', '').strip(),
                     folder_name.split('('))
    return {
        't': name,
        'y': year,
        'plot': 'full',
        'apikey': API_KEY
    }


def validate_api_data(data: dict):
    assert data.get('Response', 'False') == 'True'
    assert 'Error' not in data


def generate_poster_path(folder_name: str):
    filename = f'{folder_name}.jpg'
    return join(POSTER_PATH, filename)


def extract_required_details(data: dict, include_poster = False):
    details = {key: value for key, value in data.items() if key in REQUIRED_MOVIE_PROPS}
    if include_poster:
        details['Poster'] = data.get('Poster', '')
    return details


async def save_poster(folder_name: str, poster_url: str):
    try:
        if poster_url and poster_url != 'N/A':
            async with ClientSession() as session:
                async with session.get(poster_url) as poster_response:
                    image_data = await poster_response.read()
                    async with open(generate_poster_path(folder_name), 'wb') as image:
                        await image.write(image_data)
    except Exception as error:
        print(f'SAVE POSTER ERROR ({folder_name}) : ', error)
    finally:
        return {}


async def fetch_movie(folder_name: str, session: ClientSession, lock: Lock, update_progress: Callable = None):
    movie = {'name': folder_name, 'data': None}

    try:
        async with session.get(API_ENDPOINT, params=generate_api_params(folder_name)) as api_response:
            assert api_response.status == 200
            movie_details = await api_response.json()
            validate_api_data(movie_details)
            movie['data'] = extract_required_details(movie_details)

        await save_poster(folder_name, movie_details.get('Poster', None))
    except Exception as error:
        print(f'FETCH MOVIE ERROR ({folder_name}) : ', error)
    finally:
        async with lock:
            update_progress and update_progress()
        return movie


async def fetch_movies(folder_names: List[str], update_progress: Callable):
    lock = Lock()
    async with ClientSession() as session:
        movies = await gather(*(fetch_movie(folder_name, session, lock, update_progress) for folder_name in folder_names))
    return movies


async def search_by_imdbId(imdb_id: str):
    try:
        data = None
        params = {
                'i': imdb_id,
                'apikey': API_KEY
            }
        async with ClientSession() as session:
            async with session.get(API_ENDPOINT, params=params) as api_response:
                assert api_response.status == 200
                movie_details = await api_response.json()
                validate_api_data(movie_details)
                data = extract_required_details(movie_details, True)
    except Exception as error:
        print(f'SEARCH MOVIE ERROR ({imdb_id}) : ', error)
    finally:
        return data


def run_async(function: Callable, *args):
    if Platform == 'nt':
        from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    return run(function(*args))