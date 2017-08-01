import numpy as np
import pygame as pg
import engine as en
import constants as cn

from board import Board
from pieces import Warrior, Ranger, Mage

class TestScene(en.Scene):
    def __init__(self):
        super(TestScene, self).__init__()

    def initialize(self):
        self.camera = en.Camera(cn.WINDOW_SIZE)
        self.board = Board(cn.BOARD_SIZE)
        self.camera.set_object_to_follow(self.board)
        self.warrior = Warrior((3, 3))
        self.ranger = Ranger((9, 9))
        self.mage = Mage((9, 0))


    def update(self, dt):
        self.camera.update(dt)
        self.board.update(dt)
        self.warrior.update(dt)
        self.ranger.update(dt)
        self.mage.update(dt)

        self.camera.translate(self.board)
        self.camera.translate(self.warrior)
        self.camera.translate(self.ranger)
        self.camera.translate(self.mage)


    def draw(self):
        self.board.draw()
        self.warrior.draw()
        self.ranger.draw()
        self.mage.draw()

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
