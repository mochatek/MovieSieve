from os import listdir
from os.path import join, basename, dirname, exists
from tkinter import Tk, filedialog
from zipfile import ZipFile, ZIP_DEFLATED
from constants import WEB_PATH, DOWNLOADS_PATH, TEMP_PATH, POSTER_PATH, DB_FILE, ICON_FILE, APP_DATA_FILE


def open_dialog(type: str, title: str):
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    root.iconbitmap(ICON_FILE)
    root.attributes("-topmost", True)

    if type == 'folder':
        return filedialog.askdirectory(
            initialdir=DOWNLOADS_PATH, title=title)
    elif type == 'file':
        return filedialog.askopenfilename(
            defaultextension='.ms', filetypes=[('MovieSieve file', '*.ms')], initialdir=DOWNLOADS_PATH, title=title)


def export_to(export_file: str):
    with ZipFile(export_file, 'w', ZIP_DEFLATED) as zip_file:
        zip_file.write(DB_FILE, basename(DB_FILE))
        for poster_name in listdir(POSTER_PATH):
            zip_file.write(join(POSTER_PATH, poster_name), join(basename(POSTER_PATH), poster_name))


def import_from(export_file: str):
    with ZipFile(export_file, 'r') as zip_file:
        if export_file == APP_DATA_FILE:
            zip_file.extractall(WEB_PATH)
        else:
            for item in zip_file.namelist():
                if item.startswith('Posters/'):
                    zip_file.extract(item, dirname(POSTER_PATH))
                elif item == 'movies.db':
                    zip_file.extract(item, TEMP_PATH)


def init_app_data():
    if exists(APP_DATA_FILE):
        import_from(APP_DATA_FILE)


# def persist_app_data(route: str, websockets: list):
#     try:
#         export_to(APP_DATA_FILE)
#     except Exception as error:
#         print('EXPORT APP_DATA ERROR : ', error)
#     finally:
#         if not websockets:
#             exit()


def close_splash_screen():
    try:
        import pyi_splash
        pyi_splash.close()
    except:
        pass