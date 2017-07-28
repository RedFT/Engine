import numpy as np
import pygame as pg
import engine as en
import constants as cn


def get_my_loader(filename, flags, **kwargs):
    return en.graphics.load_image


class TiledScene(en.Scene):
    def __init__(self):
        super(TiledScene, self).__init__()

    def initialize(self):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
