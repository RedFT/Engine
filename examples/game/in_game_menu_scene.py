import numpy as np
import pygame as pg
import engine as en
from . import constants as cn

class InGameMenuScene(en.scene.Scene):
    def __init__(self):
        super(InGameMenuScene, self).__init__()

    def initialize(self):
        resume_label = en.label.Label("Resume")
        options_label = en.label.Label("Options")
        quit_label = en.label.Label("Quit")

        resume_label.set_position((cn.SCREEN_WIDTH/2, 3*cn.SCREEN_HEIGHT/8))
        options_label.set_position((cn.SCREEN_WIDTH/2, 4*cn.SCREEN_HEIGHT/8))
        quit_label.set_position((cn.SCREEN_WIDTH/2, 5*cn.SCREEN_HEIGHT/8))

        resume_label.set_size(50)
        options_label.set_size(50)
        quit_label.set_size(50)

        menu = en.menu.Menu(self)
        menu.add(resume_label, self.on_resume_pressed)
        menu.add(options_label, self.on_options_pressed )
        menu.add(quit_label, self.on_quit_pressed)

        self.add(menu)

    def on_resume_pressed(self, label):
        en.app.pop_scene()

    def on_options_pressed(self, label):
        en.graphical_logger.log("Options Button Pressed")

    def on_quit_pressed(self, label):
        en.app.quit()

    def update(self, dt):
        super(InGameMenuScene, self).update(dt)
        if en.keyboard.was_pressed(pg.K_ESCAPE):
            en.app.pop_scene()

    def pause(self):
        pass

    def resume(self):
        pass
