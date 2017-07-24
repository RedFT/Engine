import pygame as pg
import engine as en
import numpy as np
import constants as cn


class Platform(object):
    def __init__(self, pos=(50, 0), size=(50, 10)):
        en.PubSub.subsribe(self, "collision")
        self.position = np.array(pos, dtype=float)
        self.size = np.array(size, dtype=float)
        self.width, self.height = self.size
        self.rect = np.concatenate([
            self.position-self.size/2, self.size])

    def notify(self, event, sender, data):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pg.draw.rect(en.Graphics.get_main_surface(), (0, 200, 0),
                     self.rect, 1)
