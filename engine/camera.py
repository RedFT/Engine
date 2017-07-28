import numpy as np


class Camera(object):
    def __init__(self, window_size, initial_position=(0, 0)):
        self.object_to_follow = None
        self.x, self.y = initial_position
        self.window_size = window_size
        self.lag = 10

    def set_object_to_follow(self, entity):
        self.object_to_follow = entity
        self.x = entity.position[0] - self.window_size[0]/2
        self.y = entity.position[1] - self.window_size[1]/2

    def follow_object(self):
        if self.object_to_follow is None:
            return

        destination_x = self.object_to_follow.position[0] - self.window_size[0]/2
        destination_y = self.object_to_follow.position[1] - self.window_size[1]/2

        distance_x = destination_x - self.x
        distance_y = destination_y - self.y

        if abs(distance_x / self.lag) > .1:
            self.x+= distance_x / self.lag
        else:
            self.x = destination_x

        if abs(distance_y / self.lag) > .1:
            self.y+= distance_y / self.lag
        else:
            self.y = destination_y


    def update(self, dt):
        self.follow_object()

    def translate(self, entity):
        entity.camera_coordinates = entity.position - np.array([self.x, self.y])
