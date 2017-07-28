import pygame as pg

class Entity(object):
    def __init__(self, position, width, height):
        self.position = list(position)
        self.rect = pg.Rect(list(position) + [width, height])
        self.camera_coordinate = position

    def update(self, dt):
        pass

    def draw(self):
        pass

    def notify(self, event, sender, data):
        pass
