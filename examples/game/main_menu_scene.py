import numpy as np
import pygame as pg
import engine as en
import constants as cn

from game_scene import GameScene

class MainMenuScene(en.scene.Scene):
    def __init__(self):
        super(MainMenuScene, self).__init__()

    def initialize(self):
        start_label = en.label.Label("Start")
        options_label = en.label.Label("Options")
        quit_label = en.label.Label("Quit")

        start_label.set_position((cn.SCREEN_WIDTH/2, 3*cn.SCREEN_HEIGHT/8))
        options_label.set_position((cn.SCREEN_WIDTH/2, 4*cn.SCREEN_HEIGHT/8))
        quit_label.set_position((cn.SCREEN_WIDTH/2, 5*cn.SCREEN_HEIGHT/8))

        start_label.set_size(50)
        options_label.set_size(50)
        quit_label.set_size(50)

        menu = en.menu.Menu(self)
        menu.add(start_label, self.on_start_pressed)
        menu.add(options_label, self.on_options_pressed )
        menu.add(quit_label, self.on_quit_pressed)

        self.add(menu)

    def update(self, dt):
        super(MainMenuScene, self).update(dt)

    def on_start_pressed(self, label):
        en.app.push_scene(GameScene())

    def on_options_pressed(self, label):
        en.graphical_logger.log("Options Button Pressed")

    def on_quit_pressed(self, label):
        en.app.quit()

    def pause(self):
        pass

    def resume(self):
        pass
