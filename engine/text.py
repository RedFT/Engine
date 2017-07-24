import pygame as pg
import engine as en
import os


class Text:
    _fonts = {}
    _initialized = False

    @staticmethod
    def initialize():
        pg.font.init()
        Text._initialized = True
        en.GraphicalLogger.log("Initialized Pygame Fonts")

    @staticmethod
    def load_font(font_name, font_size):
        key = font_name + str(int(font_size))
        if key in Text._fonts.keys():
            return Text._fonts[key]

        res_dir = en.get_resources_directory()
        font_path = os.path.join(res_dir, 'fonts', font_name)
        f = pg.font.Font(font_path, font_size)

        Text._fonts[key] = f
        en.GraphicalLogger.log("Loaded font " + font_name + " with size " + str(font_size))
        return f

    @staticmethod
    def check_size(font_name, font_size, text):
        return Text.load_font(font_name, font_size).size(text)

    @staticmethod
    def check_width(font_name, font_size, text):
        return Text.load_font(font_name, font_size).get_width(text)

    @staticmethod
    def check_height(font_name, font_size, text):
        return Text.load_font(font_name, font_size).get_height(text)

    @staticmethod
    def create_text(font_name, font_size, text, aa=False, color=(0, 0, 0)):
        font = Text.load_font(font_name, font_size)
        f = font.render(text, aa, color)
        f.convert_alpha()
        return f

    @staticmethod
    def create_multiline_text(font_name, font_size, text, aa=False, color=(0, 0, 0)):
        lines = text.splitlines()
        line_surfs = []
        total_height = 0
        max_width = 0
        for l in lines:
            line = l.strip()
            if line == '':
                continue
            font_surf = Text.create_text(font_name, font_size, line, aa, color)
            total_height += font_surf.get_rect().height
            if font_surf.get_rect().width > max_width:
                max_width = font_surf.get_rect().width

            line_surfs.append(font_surf)

        current_y = 0
        multiline_surf = pg.Surface((max_width, total_height), pg.SRCALPHA)
        multiline_surf.convert_alpha()
        multiline_surf.fill((0, 0, 0, 0))
        for surf in line_surfs:
            multiline_surf.blit(surf, (0, current_y))
            current_y += surf.get_rect().height
        return multiline_surf
