import numpy as np
import pygame as pg
import engine as en
import constants as cn
from pytmx.util_pygame import  load_pygame as load_tmx_surfaces


class TiledScene(en.Scene):
    def __init__(self):
        super(TiledScene, self).__init__()

    def initialize(self):
        self.tmxdata = load_tmx_surfaces(en.get_resources_directory() + "/island.tmx")

    def update(self, dt):
        pass

    def draw(self):
        for layer in self.tmxdata.visible_layers:
            for tile in layer.tiles():
                position = np.array(tile[:2])
                surf = tile[2]
                en.graphics.draw_image(surf, position * 32 * 2)

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
