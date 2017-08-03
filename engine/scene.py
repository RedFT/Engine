import pygame as pg

import app
import node
import graphics

class Scene(node.Node):
    def __init__(self):
        super(Scene, self).__init__()
        self.scene_surface = pg.Surface(app.get_screen_size())

    def initialize(self):
        # Create a scene_surface when overriding this
        raise NotImplementedError("Has not been implemented.")

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self):
        self.scene_surface.fill(graphics.get_clear_color())
        for child in self.children:
            child.draw()

    def pause(self):
        raise NotImplementedError("Has not been implemented.")

    def resume(self):
        raise NotImplementedError("Has not been implemented.")
