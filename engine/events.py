import pygame as pg
import keyboard
import mouse


def handle_events(dt):
    got_quit = False
    keyboard.begin_new_frame(dt)
    mouse.begin_new_frame(dt)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            got_quit = True
        elif event.type == pg.KEYUP:
            keyboard.register_key_up(event.key)

        elif event.type == pg.KEYDOWN:
            keyboard.register_key_down(event.key)

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse.register_mouse_press(event.button-1)

        elif event.type == pg.MOUSEBUTTONUP:
            mouse.register_mouse_release(event.button-1)

        elif event.type == pg.MOUSEMOTION:
            mouse.register_mouse_motion(pg.mouse.get_pos())

    return got_quit
