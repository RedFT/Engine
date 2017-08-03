import numpy as np
import pygame as pg
import engine as en
import constants as cn

from board import Board
from pieces import Warrior, Ranger, Mage

from in_game_menu_scene import InGameMenuScene

class GameScene(en.scene.Scene):
    def __init__(self):
        super(GameScene, self).__init__()

    def initialize(self):
        tiles = en.tiled.load_tiles("board.json", cn.SCALE)
        board = Board(cn.BOARD_SIZE, tiles)
        warrior = Warrior((3, 3))
        ranger = Ranger((9, 9))
        mage = Mage((9, 0))

        self.add(board)
        self.add(warrior)
        self.add(ranger)
        self.add(mage)

    def update(self, dt):
        super(GameScene, self).update(dt)
        if en.keyboard.was_pressed(pg.K_ESCAPE):
            en.app.push_scene(InGameMenuScene())

    def pause(self):
        pass

    def resume(self):
        pass
