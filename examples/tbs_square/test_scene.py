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
        tiles = en.tiled.load_tiles("board.json", cn.SCALE)
        self.board = Board(cn.BOARD_SIZE, tiles)
        self.warrior = Warrior((3, 3))
        self.ranger = Ranger((9, 9))
        self.mage = Mage((9, 0))

        self.add(self.board)
        self.add(self.warrior)
        self.add(self.ranger)
        self.add(self.mage)

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
