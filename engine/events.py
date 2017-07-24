import pygame as pg
import keyboard


def handle_events(dt):
    got_quit = False
    keyboard.begin_new_frame(dt)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            got_quit = True
        elif event.type == pg.KEYUP:
            keyboard.register_key_up(event.key)

        elif event.type == pg.KEYDOWN:
            keyboard.register_key_down(event.key)

    return got_quit
