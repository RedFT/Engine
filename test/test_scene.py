import numpy as np
import pygame as pg
import engine as en
import constants as cn

from ball import Ball
from platform import Platform


class TestScene(en.Scene):
    def __init__(self):
        super(TestScene, self).__init__()

    def initialize(self):
        self.camera = en.Camera(cn.WINDOW_SIZE)
        self.smoke_emitter = en.particle_machines.SmokeMachine(
            20,
            8,
            -90,
            1000,
            40,
            0.06,
            (cn.SCREEN_WIDTH / 2, cn.SCREEN_HEIGHT / 2))
        self.rain_emitter = en.particle_machines.RainMaker(
            20,
            1,
            80,
            1000,
            20,
            .015,
            (cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT))

        self.ball = Ball((100, 30))
        platform1 = Platform((200, cn.SCREEN_HEIGHT - 40),
                                  (cn.SCREEN_WIDTH / 2, 30))
        platform2 = Platform((400, cn.SCREEN_HEIGHT - 100),
                                  (cn.SCREEN_WIDTH / 2, 30))

        self.ent_list = [
            self.ball,
            platform1,
            platform2]
        self.world = [
            self.ball,
            platform1,
            platform2,
            self.rain_emitter,
            self.smoke_emitter]

        self.camera.set_object_to_follow(self.ball)

        self.minimap_size = np.array(en.graphics.get_main_surface().get_size()) / cn.SCALE
        self.minimap_surface = pg.Surface(en.graphics.get_main_surface().get_size())
        self.minimap = pg.Surface(self.minimap_size)

    def update(self, dt):
        self.objects_to_translate = []
        for obj in self.world:
            to_draw = obj.update(dt)
            if type(to_draw) == list:
                self.objects_to_translate += to_draw
            else:
                self.objects_to_translate += [to_draw]

        self.smoke_emitter.set_pos(self.ball.position)

        self.camera.update(dt)
        for ent in self.objects_to_translate:
            self.camera.translate(ent)

        all_ent_rects = [obj.rect for obj in self.objects_to_translate]
        for ent in self.ent_list:
            for idx in pg.Rect(ent.rect).collidelistall(all_ent_rects):
                if ent is self.objects_to_translate[idx]:
                    continue
                en.pubsub.publish("collision", self, [ent, self.objects_to_translate[idx]])


    def draw(self):
        for ent in self.world:
            ent.draw()

        for obj in self.ent_list:
            pg.draw.rect(self.minimap_surface, (0, 0, 255), map(int, obj.rect), 5)

        pg.transform.scale(self.minimap_surface, self.minimap_size, self.minimap)

        self.minimap.set_alpha(160)
        en.graphics.draw_image(self.minimap,
                               (cn.SCREEN_WIDTH-self.minimap_size[0],
                                cn.SCREEN_HEIGHT-self.minimap_size[1]))
        self.minimap_surface.fill((0, 0, 0))


    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
