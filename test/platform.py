import pygame as pg
import engine as en
import numpy as np


class Platform(en.Entity):
    def __init__(self, pos=(50, 0), size=(50, 10)):
        super(Platform, self).__init__(pos, size[0], size[1])
        en.pubsub.subscribe(self, "collision")
        self.rect = np.concatenate([self.position-np.array(size)/2, size])
        self.size = np.array(size)
        self.slow_amount = .003

    def notify(self, event, sender, data):
        if event == "collision" and self in data:
            other = data[0] if data[1] is self else data[1]
            from ball import Ball
            if type(other) == Ball:
                move_right = -1 if other.move_velocity > 0 else 1
                if abs(other.move_velocity) < self.slow_amount:
                    other.move_velocity = 0
                else:
                    other.move_velocity += .003*move_right
                return
            if type(other) is en.Particle:
                other.kill()

    def update(self, dt):
        return self

    def draw(self):
        new_rect = pg.Rect(self.rect)
        new_rect.x, new_rect.y = self.camera_coordinates - self.size/2
        pg.draw.rect(en.graphics.get_main_surface(), (0, 200, 0),
                     new_rect, 1)
