import pygame as pg
import engine as en
import os

class TextParams:
    fonts = {}


def initialize():
    pg.font.init()


def load_font(font_name, font_size):
    key = font_name + str(int(font_size))
    if key in TextParams.fonts.keys():
        return TextParams.fonts[key]

    res_dir = en.get_resources_directory()
    font_path = os.path.join(res_dir, 'fonts', font_name)
    f = pg.font.Font(font_path, font_size)

    TextParams.fonts[key] = f
    en.graphical_logger.log("Loaded font " + font_name + " with size " + str(font_size))
    return f


def check_size(font_name, font_size, text):
    return load_font(font_name, font_size).size(text)


def check_height(font_name, font_size, text):
    return load_font(font_name, font_size).get_height()


def create_text(font_name, font_size, text, aa=False, color=(0, 0, 0)):
    font = load_font(font_name, font_size)
    f = font.render(text, aa, color)
    return f


def create_multiline_text(font_name, font_size, text, aa=False, color=(0, 0, 0)):
    lines = text.splitlines()
    line_surfs = []
    total_height = 0
    max_width = 0
    for l in lines:
        line = l.strip()
        if line == '':
            continue
        font_surf = create_text(font_name, font_size, line, aa, color)
        total_height += font_surf.get_rect().height
        if font_surf.get_rect().width > max_width:
            max_width = font_surf.get_rect().width

        line_surfs.append(font_surf)

    current_y = 0
    multiline_surf = pg.Surface((max_width, total_height), pg.SRCALPHA)
    multiline_surf.fill((0, 0, 0, 0))
    for surf in line_surfs:
        multiline_surf.blit(surf, (0, current_y))
        current_y += surf.get_rect().height
    return multiline_surf
