import engine as en
import pygame as pg
import numpy as np

import time

import textwrap


# Depends on pygame.font
class GraphicalLogger:
    _log_queue = []
    _position = [0, 0]
    _text_life = 4000.  # in ms
    _num_char_per_line = 50
    _box_width = 0
    _initialized = False

    # Interpolate for a nice fading effect
    X = np.array([0, .1, .2, .3, .6, .8, 1])
    Y = np.array([0, 2, 1.5, 1, .3, .1, 0])
    _poly_v = np.polyfit(X, Y, 2)

    @staticmethod
    def initialize(position=(0, 0), width=100, text_life=1000.):
        GraphicalLogger._box_width = width
        # GraphicalLogger._num_char_per_line=10
        GraphicalLogger._text_life = text_life
        GraphicalLogger._position = position
        GraphicalLogger._initialized = True

    @staticmethod
    def log(message):
        text = str(time.strftime('%X')) + ": " + message
        # padding=10
        mult_line = textwrap.fill(text, GraphicalLogger._num_char_per_line)
        surf = en.Text.create_multiline_text("Unique.ttf", 16, mult_line,
                                             aa=True, color=(100, 100, 220))
        GraphicalLogger._log_queue.append([surf, 0.])
        return

    @staticmethod
    def update(dt):
        GraphicalLogger._log_queue = [
            [surf, queue + dt]
            for surf, queue in GraphicalLogger._log_queue
            if (queue + dt) < GraphicalLogger._text_life
        ]

    @staticmethod
    def draw():
        current_y = 0
        for surf, time in reversed(GraphicalLogger._log_queue):
            t = time / GraphicalLogger._text_life
            alph = np.polyval(GraphicalLogger._poly_v, np.array([t]))
            alpha = max(min(1., alph), 0) * 255

            s = pg.Surface(surf.get_size(), pg.SRCALPHA)
            s.fill((255, 255, 255, alpha))
            s.blit(surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

            en.Graphics.draw_image(s,
                                   (GraphicalLogger._position[0], GraphicalLogger._position[1] + current_y))
            current_y += surf.get_rect().height + 5
