from constants import ROOT_PATH, POSTER_PATH, APP_ICON
from os.path import join, isdir
from os import listdir, rmdir, remove

WHITELIST = [POSTER_PATH, join(POSTER_PATH, 'NA.png'), APP_ICON]

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
    web_directory = join(ROOT_PATH, 'web')

    for item in listdir(web_directory):
        delete_recursively(join(web_directory, item))

