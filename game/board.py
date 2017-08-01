import engine as en
import pygame as pg

import constants as cn

class InfoType:
    MOVE=1
    ATTACK=2

class Board(en.entity.Entity):
    def __init__(self, size):
        width = size[0]
        height = size[1]
        width_in_px = width * cn.CELL_SIZE[0]
        height_in_px = height  * cn.CELL_SIZE[1]
        super(Board, self).__init__((0, 0), width_in_px, height_in_px)

        self.width_in_cells = width
        self.height_in_cells = height

        self.selected_entity = None
        self.info_type = InfoType.MOVE

        en.pubsub.subscribe(self, "cell_click")
        en.pubsub.subscribe(self, "selected")

    def update(self, dt):
        mouse_pos = en.mouse.get_position()
        cell_x = mouse_pos[0] / cn.CELL_WIDTH
        cell_y = mouse_pos[1] / cn.CELL_HEIGHT

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
        surf = en.graphics.get_main_surface()

        for x in xrange(self.width_in_cells+1):
            pg.draw.line(surf, (255, 0, 0),
                (x*cn.CELL_WIDTH, 0),
                (x*cn.CELL_WIDTH, self.rect.bottom))

        for y in xrange(self.height_in_cells+1):
            pg.draw.line(surf, (255, 0, 0),
                (0, y*cn.CELL_HEIGHT),
                (self.rect.right, y*cn.CELL_HEIGHT))

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
        if event == "selected":
            if sender is self.selected_entity:
                self.selected_entity = None
            else:
                self.selected_entity = sender
