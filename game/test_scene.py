import numpy as np
import pygame as pg
import engine as en
import constants as cn


class TestScene(en.Scene):
    def __init__(self):
        super(TestScene, self).__init__()

    def initialize(self):
        self.camera = en.Camera(cn.WINDOW_SIZE)


    def update(self, dt):
        self.camera.update(dt)


    def draw(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
