import sys


def get_resources_directory():
    try:
        p = sys._MEIPASS
    except AttributeError:
        p = "./resources"
    return p
