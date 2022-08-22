from os import listdir, rmdir, remove
from os.path import join, isdir
from constants import WEB_PATH, POSTER_PATH, ICON_FILE, ENV_FILE

WHITELIST = (POSTER_PATH, join(POSTER_PATH, 'NA.png'), ENV_FILE, ICON_FILE)

def delete_recursively(path):
    if not isdir(path):
        if path not in WHITELIST:
            remove(path)
    else:
        for item in listdir(path):
            delete_recursively(join(path, item))
        if path not in WHITELIST:
            rmdir(path)

if __name__ == '__main__':
    for item in listdir(WEB_PATH):
        delete_recursively(join(WEB_PATH, item))

