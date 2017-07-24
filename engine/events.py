import pygame as pg
from keyboard import Keyboard


class Input:
    @staticmethod
    def handle_events(dt):
        got_quit = False
        Keyboard.begin_new_frame(dt)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                got_quit = True
            elif event.type == pg.KEYUP:
                Keyboard.register_key_up(event.key)

            elif event.type == pg.KEYDOWN:
                Keyboard.register_key_down(event.key)

        return got_quit
