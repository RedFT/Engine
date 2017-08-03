import engine as en
import pygame as pg
import os


class GraphicsParams:
    main_surface = None
    scale_factor = None
    scale_factor = None
    loaded_images = None
    sprite_sheets = None
    clear_color = None


def initialize(window_size, caption, scale_factor=1):
    GraphicsParams.main_surface = pg.display.set_mode(window_size)
    GraphicsParams.scale_factor = scale_factor
    GraphicsParams.scale_factor = scale_factor
    GraphicsParams.loaded_images = {}
    GraphicsParams.sprite_sheets = {}
    GraphicsParams.clear_color = (255, 255, 255, 255)

    pg.display.set_caption(caption)


def load_image(filename):
    res_dir = en.get_resources_directory()
    os_filename = os.path.join(res_dir, filename)

    if os_filename in GraphicsParams.loaded_images.keys():
        return GraphicsParams.loaded_images[os_filename]

    en.graphical_logger.log("Loaded Image " + os_filename)
    image = pg.image.load(os_filename)
    image = image.convert_alpha()

    # resize
    if GraphicsParams.scale_factor != 1:
        en.graphical_logger.log("Resizing image by factor of " + str(GraphicsParams.scale_factor))
        img_rect = image.get_rect()
        width = img_rect.width * GraphicsParams.scale_factor
        height = img_rect.height * GraphicsParams.scale_factor
        image = pg.transform.scale(image, (width, height))

    GraphicsParams.loaded_images[os_filename] = image
    return image


def draw_image(image, position):
    GraphicsParams.main_surface.blit(image, position)


def flip():
    pg.display.flip()


def clear():
    GraphicsParams.main_surface.fill(GraphicsParams.clear_color)


def set_clear_color(clear_color):
    GraphicsParams.clear_color = clear_color

def get_clear_color():
    return GraphicsParams.clear_color

def get_main_surface():
    return GraphicsParams.main_surface
