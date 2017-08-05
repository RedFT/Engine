import engine as en
import pygame as pg
from . import constants as cn

class InfoType:
    MOVE=1
    ATTACK=2

class Board(en.entity.Entity):
    def __init__(self, size, tiles=None):
        super(Board, self).__init__((0, 0))

        self.tiles = tiles
        width = size[0]
        height = size[1]
        width_in_px = width * cn.CELL_SIZE[0]
        height_in_px = height  * cn.CELL_SIZE[1]
        self.rect = pg.Rect(0, 0, width_in_px, height_in_px)

        self.width_in_cells = width
        self.height_in_cells = height

        self.selected_entity = None
        self.info_type = InfoType.MOVE

    def enter(self):
        en.pubsub.subscribe(self, "cell_click")
        en.pubsub.subscribe(self, "selected")

    def exit(self):
        en.pubsub.unsubscribe_to_all_messages(self)

    def update(self, dt):
        mouse_pos = en.mouse.get_position()
        cell_x = mouse_pos[0] // cn.CELL_WIDTH
        cell_y = mouse_pos[1] // cn.CELL_HEIGHT

        if en.mouse.was_pressed(0):
            self.info_type = InfoType.MOVE
            clicked_cell = (cell_x, cell_y)

            if cell_x < self.width_in_cells and cell_y < self.height_in_cells:
                en.pubsub.publish("move_piece", self, (self.selected_entity, clicked_cell))
                en.pubsub.publish("cell_click", self, clicked_cell)

        if en.mouse.was_pressed(2):
            self.info_type = InfoType.ATTACK
            clicked_cell = (cell_x, cell_y)
            en.pubsub.publish("cell_click", self, clicked_cell)


    def draw(self):
        surf = en.app.get_current_scene().scene_surface
        map_height = self.tiles['height']
        map_width = self.tiles['width']
        for i, tile in enumerate(self.tiles['data']):
            x = (i % cn.BOARD_WIDTH) * cn.CELL_WIDTH
            y = (i // cn.BOARD_WIDTH) * cn.CELL_WIDTH

            rect = self.tiles['rects'][tile]
            tile_img = self.tiles['image'].subsurface(rect)
            surf.blit(tile_img, (x, y))

        # Draw available moves if an entity is selected
        if self.selected_entity:
            if self.info_type == InfoType.MOVE:
                draw_rect = self.selected_entity.rect
                pg.draw.rect(surf, (255, 0, 255),
                    draw_rect, 2)

                for cell in self.selected_entity.valid_move_cells:
                    pg.draw.rect(surf, (0, 255, 0),
                        (cell[0] * cn.CELL_WIDTH,
                         cell[1] * cn.CELL_HEIGHT,
                         cn.CELL_WIDTH, cn.CELL_HEIGHT),
                         2)
            elif self.info_type == InfoType.ATTACK:
                draw_rect = self.selected_entity.rect
                pg.draw.rect(surf, (255, 0, 255),
                    draw_rect, 2)

                for cell in self.selected_entity.valid_move_cells:
                    pg.draw.rect(surf, (255, 0, 0),
                        (cell[0] * cn.CELL_WIDTH,
                         cell[1] * cn.CELL_HEIGHT,
                         cn.CELL_WIDTH, cn.CELL_HEIGHT),
                         4)


    def notify(self, event, sender, data):
        if event == "cell_click":
            if not self.selected_entity:
                return
            if data != self.selected_entity.cell_position:
                self.selected_entity = None

        elif event == "selected":
            if sender is self.selected_entity:
                self.selected_entity = None
            else:
                self.selected_entity = sender
