import sys


def get_resources_directory():
    try:
        p = sys._MEIPASS
    except AttributeError:
        p = "./resources" # use this if the app hasn't been packaged by pyinstaller
    return p
