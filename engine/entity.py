import pygame as pg
import engine as en

class Entity(en.Node):
    def __init__(self, position, width, height):
        super(Entity, self).__init__()
        self.position = list(position)
        self.rect = pg.Rect(list(position) + [width, height])
        self.camera_coordinate = position

    def update(self, dt):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def notify(self, event, sender, data):
        raise NotImplementedError
