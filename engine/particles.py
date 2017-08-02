import pygame as pg
import numpy as np

import graphics
import entity


class Particle(entity.Entity):
    def __init__(self, position, size, color, strategies):
        super(Particle, self).__init__(position, size, size)
        self.x, self.y = self.position
        self.color = color
        self.size = size
        self.rect = [self.x, self.y, size, size]
        self.alive = 0
        self.strategies = strategies
        self.alpha = 1.

    def set_pos(self, pos):
        self.x, self.y = self.position = pos
        self.rect[0]=self.x
        self.rect[1]=self.y

    def kill(self):
        self.alive = -1

    def update(self, dt):
        for s in self.strategies:
            s(self)


class ParticleBehaviors:
    def __init__(self):
        pass

    @staticmethod
    def get_age_callback(amount):
        def _age(particle):
            particle.alive += amount * (particle.alive != -1)
        return _age

    @staticmethod
    def get_fade_callback(amount):
        def _fade(particle):
            particle.alpha -= amount

        return _fade

    @staticmethod
    def get_movement_callback(speed, angle):
        rads = np.deg2rad(angle)
        dx = speed * np.cos(rads)
        dy = speed * np.sin(rads)

        def _movement(particle):
            particle.set_pos((particle.x+dx, particle.y+dy))

        return _movement

    @staticmethod
    def get_deathtime_callback(duration):
        def _deathtime(particle):
            if particle.alive > duration:
                particle.kill()

        return _deathtime

    @staticmethod
    def get_grow_callback(amount):
        def _grow(particle):
            particle.size += amount

        return _grow

    @staticmethod
    def get_wind_callback(move_amount, strength):
        def _wind(particle):
            if np.random.randint(0, 100) < strength:
                particle.x += move_amount

        return _wind


class ParticleEmitter(object):
    def __init__(self, emit_rate, position):
        self.particles = []
        self.emit_rate = emit_rate
        self.position = position

    def set_pos(self, pos):
        self.position = pos

    def get_number_to_emit_this_frame(self, dt):
        return self.emit_rate * dt / 1000.

    def emit(self):
        raise NotImplementedError

    def update(self, dt):
        emit_n = self.get_number_to_emit_this_frame(dt)
        for_sure = int(emit_n)
        prob_of_last_particle = emit_n % 1
        emit_last = np.random.uniform() < prob_of_last_particle
        num_to_emit = for_sure + emit_last
        for i in range(num_to_emit):
            self.emit()

        for p in self.particles:
            p.update(dt)

        self.particles = [p for p in self.particles if p.alive != -1]
        return self.particles

    def draw(self):
        for p in self.particles:
            if p.alpha < 0:
                p.kill()
            if p.alive == -1:
                continue

            s = pg.Surface((2 * p.size, 2 * p.size))
            s.convert_alpha()
            s.fill((255, 255, 255))
            s.set_colorkey((255, 255, 255))

            pg.draw.circle(s, p.color,
                           map(int, (p.size, p.size)), int(p.size))
            s.set_alpha(int(p.alpha * 255))

            draw_position = np.array(p.camera_coordinates)
            graphics.draw_image(s, draw_position - p.size)
