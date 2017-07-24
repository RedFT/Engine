import engine as en
import pygame as pg
import numpy as np

import time

import textwrap


class GraphicalLoggerParams:
    def __init__(self):
        pass

    log_queue = None
    num_chars_per_line = None
    box_width = None
    text_life = None
    position = None
    padding = None


def initialize(position=(0, 0), width=100, text_life=1000., chars_per_line=50, padding=10):
    GraphicalLoggerParams.log_queue = []
    GraphicalLoggerParams.num_char_per_line = chars_per_line
    GraphicalLoggerParams.box_width = width
    GraphicalLoggerParams.text_life = text_life
    GraphicalLoggerParams.position = position
    GraphicalLoggerParams.padding = padding

    # Interpolate for a nice fading effect
    X = np.array([0, .1, .2, .3, .6, .8, 1])
    Y = np.array([0, 2, 1.5, 1, .3, .1, 0])
    fade_curve = np.polyfit(X, Y, 2)
    GraphicalLoggerParams.fade_curve = fade_curve


def log(message):
    pad = GraphicalLoggerParams.padding
    text = str(time.strftime('%X')) + ": " + message
    mult_line = textwrap.fill(text, GraphicalLoggerParams.num_char_per_line)
    surf = en.text.create_multiline_text("Unique.ttf", 16, mult_line,
                                         aa=True, color=(100, 100, 220))
    GraphicalLoggerParams.log_queue.append([surf, 0.])
    return


def update(dt):
    GraphicalLoggerParams.log_queue = [
        [surf, queue + dt]
        for surf, queue in GraphicalLoggerParams.log_queue
        if (queue + dt) < GraphicalLoggerParams.text_life
    ]


def draw():
    current_y = 0
    for surf, time in reversed(GraphicalLoggerParams.log_queue):
        t = time / GraphicalLoggerParams.text_life
        alph = np.polyval(GraphicalLoggerParams.fade_curve, np.array([t]))
        alpha = max(min(1., alph), 0) * 255

        s = pg.Surface(surf.get_size(), pg.SRCALPHA)
        s.fill((255, 255, 255, alpha))
        s.blit(surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

        en.graphics.draw_image(s,
                               (GraphicalLoggerParams.position[0], GraphicalLoggerParams.position[1] + current_y))
        current_y += surf.get_rect().height + 5
