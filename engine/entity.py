import pygame as pg
import node

class Entity(node.Node):
    def __init__(self, position):
        super(Entity, self).__init__()
        self.position = list(position)
        self.camera_coordinate = position

    def update(self, dt):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def notify(self, event, sender, data):
        raise NotImplementedError
