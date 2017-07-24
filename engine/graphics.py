import engine as en
import pygame as pg
import os


class Graphics:
    _scale_factor=1
    _loaded_images = {}
    _sprite_sheets = {}
    _main_surface = None
    _clear_color = (255, 255, 255, 255)

    @staticmethod
    def initialize(window_size, caption, scale_factor=1):
        Graphics._main_surface = pg.display.set_mode(window_size)
        pg.display.set_caption(caption)
        Graphics._scale_factor = scale_factor
        en.GraphicalLogger.log("Graphics Setup")

    @staticmethod
    def load_image(filename):
        res_dir = en.get_resources_directory()
        os_filename = os.path.join(res_dir, filename)
        
        if os_filename in Graphics._loaded_images.keys():
            return Graphics._loaded_images[os_filename]


        en.GraphicalLogger.log("Loaded Image " + os_filename)
        image = pg.image.load(os_filename)
        image = image.convert_alpha()

        # resize
        if Graphics._scale_factor != 1:
            img_rect = image.get_rect()
            width = img_rect.width * Graphics._scale_factor
            height = img_rect.height * Graphics._scale_factor
            image = pg.transform.scale(image, (width, height))

        Graphics._loaded_images[os_filename] = image
        return image

    @staticmethod
    def draw_image(image, position):
        Graphics._main_surface.blit(image, position)

    @staticmethod
    def flip():
        pg.display.flip()

    @staticmethod
    def clear():
        Graphics._main_surface.fill(Graphics._clear_color)

    @staticmethod
    def set_clear_color(clear_color):
        Graphics._clear_color = clear_color

    @staticmethod
    def get_main_surface():
        return Graphics._main_surface
