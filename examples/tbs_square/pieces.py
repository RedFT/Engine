import engine as en
import pygame as pg
import numpy as np

import constants as cn

def generate_valid_move_cells(position, move_range):
    right = np.array([1, 0])
    down = np.array([0, 1])
    valid_move_cells = []
    for d in xrange(1, move_range+1):
        for a in xrange(1, d+1):
            b = d - a
            cell1 = a*right + b*down
            # reflect cell1 over vertical
            cell2 = cell1[::-1] * (-1, 1) + position
            # reflect cell1 over horizontal
            cell3 = cell1[::-1] * (1, -1) + position
            # reflect cell1 over diagonal
            cell4 = cell1 * (-1, -1) + position
            cell1 += position

            valid_move_cells.append(cell1)
            valid_move_cells.append(cell2)
            valid_move_cells.append(cell3)
            valid_move_cells.append(cell4)
    return valid_move_cells


class Piece(en.entity.Entity):
    def __init__(self, cell, move_range):
        self.position_in_px = np.array((cell[0] * cn.CELL_WIDTH, cell[1] * cn.CELL_HEIGHT), dtype=float)
        super(Piece, self).__init__(self.position_in_px, cn.CELL_WIDTH, cn.CELL_HEIGHT)
        self.cell_position = cell

        self.move_range = move_range
        self.valid_move_cells = generate_valid_move_cells(self.cell_position, self.move_range)

        self.move_speed = 10# number of frames to move over

        self.starting_point = None
        self.ending_point = None

        en.pubsub.subscribe(self, "cell_click")
        en.pubsub.subscribe(self, "move_piece")

    def lerp(self, current_position, pieces, A=None, B=None):
        if A is not None:
            self.starting_point = A.copy()
        if B is not None:
            self.ending_point = B.copy()

        if self.starting_point is None:
            return current_position
        if self.ending_point is None:
            return current_position

        if np.linalg.norm(current_position - self.ending_point) < .1:
            return current_position

        D = (np.array(self.ending_point)-self.starting_point)/pieces
        return current_position + D

    def update(self, dt):
        self.position_in_px = self.lerp(self.position_in_px, self.move_speed)
        self.rect[:2] = self.position_in_px

    def set_cell(self, cell):
        self.cell_position = cell
        self.lerp(self.position_in_px, self.move_speed,
            self.position_in_px,
            np.array(self.cell_position)*cn.CELL_SIZE)
        self.valid_move_cells = generate_valid_move_cells(self.cell_position, self.move_range)

    def notify(self, event, sender, data):
        if event == "cell_click":
            click_position = data
            if self.cell_position == click_position:
                en.pubsub.publish("selected", self)
        elif event == "move_piece":
            if self is not data[0]:
                return
            if not any(tuple(data[1])==tuple(cell) for cell in self.valid_move_cells):
                return
            self.set_cell(data[1])


class Warrior(Piece):
    def __init__(self, cell):
        super(Warrior, self).__init__(cell, 1)

    def draw(self):
        surf = en.graphics.get_main_surface()
        pad_x = cn.CELL_WIDTH/8
        pad_y = cn.CELL_HEIGHT/8

        draw_rect = pg.Rect(self.position_in_px[0]+pad_x, self.position_in_px[1]+pad_y,
            cn.CELL_WIDTH-2*pad_y, cn.CELL_HEIGHT-2*pad_y)
        pg.draw.rect(surf, (50, 130, 50),
            draw_rect, 5)


class Ranger(Piece):
    def __init__(self, cell):
        super(Ranger, self).__init__(cell, 3)

    def draw(self):
        surf = en.graphics.get_main_surface()
        pad_x = cn.CELL_WIDTH/8
        pad_y = cn.CELL_HEIGHT/8

        p1 = (cn.CELL_WIDTH/2, pad_y)
        p2 = (pad_x, cn.CELL_HEIGHT-pad_y)
        p3 = (cn.CELL_WIDTH-2*pad_x, cn.CELL_HEIGHT-pad_y)

        p1 += self.position_in_px#np.array(self.cell_position) * cn.CELL_SIZE
        p2 += self.position_in_px#np.array(self.cell_position) * cn.CELL_SIZE
        p3 += self.position_in_px#np.array(self.cell_position) * cn.CELL_SIZE

        lines = [p1, p2, p3]
        pg.draw.lines(surf, (130, 50, 50), True,
            lines, 5)


class Mage(Piece):
    def __init__(self, cell):
        super(Mage, self).__init__(cell, 2)

    def draw(self):
        surf = en.graphics.get_main_surface()
        pad_x = cn.CELL_WIDTH/8
        pad_y = cn.CELL_HEIGHT/8

        cell_center = np.array(cn.CELL_SIZE)/2
        cell_center += self.position_in_px.astype(np.int64)#np.array(self.cell_position) * cn.CELL_SIZE

        radius = (cn.CELL_WIDTH - 2 * pad_x)/2

        pg.draw.circle(surf, (130, 50, 50), cell_center,
            radius, 5)
