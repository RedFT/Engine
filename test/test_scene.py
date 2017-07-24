import pygame as pg
import engine as en
import constants as cn

from ball import Ball
from platform import Platform


class TestScene(en.Scene):
    def __init__(self):
        pass

    def initialize(self):
        self.smoke_emitter = en.SmokeMachine(
            20,
            8,
            -90,
            1000,
            10,
            0.02,
            (cn.SCREEN_WIDTH / 2, cn.SCREEN_HEIGHT / 2))

        self.rain_emitter = en.RainMaker(
            400,
            90,
            (cn.SCREEN_WIDTH, cn.SCREEN_HEIGHT))
        self.ball = Ball((30, 30))
        self.platform1 = Platform((200, cn.SCREEN_HEIGHT - 40),
                                 (cn.SCREEN_WIDTH/2, 30))
        self.platform2 = Platform((400, cn.SCREEN_HEIGHT - 100),
                                 (cn.SCREEN_WIDTH/2, 30))

        self.ent_list = [
            self.ball,
            self.platform1,
            self.platform2,
        ]

    def update(self, dt):
        for ent in self.ent_list:
            ent.update(dt)

        self.rain_emitter.update(dt)

        self.smoke_emitter.update(dt)
        self.smoke_emitter.set_pos(self.ball.position)

        num_ents = len(self.ent_list)
        for i in xrange(num_ents-1):
            for j in xrange(i+1, num_ents):
                if pg.Rect(self.ent_list[i].rect).colliderect(self.ent_list[j].rect):
                    en.PubSub.publish("collision", self, [self.ent_list[i], self.ent_list[j]])


    def draw(self):
        for ent in self.ent_list:
            ent.draw()

        self.smoke_emitter.draw()
        self.rain_emitter.draw()

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
