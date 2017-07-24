import pygame as pg
import engine as en
import numpy as np


class Particle:
    def __init__(self, position, size, color, stemit_rategies):
        self.x, self.y = self.pos = position
        self.color = color
        self.size = size
        self.alive = 0
        self.stemit_rategies = stemit_rategies
        self.alpha = 1.

    def kill(self):
        self.alive = -1

    def act(self):
        for s in self.stemit_rategies:
            s(self)


class ParticleBehaviours:
    @staticmethod
    def get_age_callback(amount):
        def _age(particle):
            particle.alive += amount
        return _age

    @staticmethod
    def get_fade_callback(amount):
        def _fade(particle):
            particle.alpha -= amount
        return _fade

    @staticmethod
    def get_movement_callback(speed, angle):
        rads = np.deg2rad(angle)
        dx = speed*np.cos(rads)
        dy = speed*np.sin(rads)
        def _movement(particle):
            particle.x += dx
            particle.y += dy
            particle.pos = (particle.x, particle.y)
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
        for_sure=int(emit_n)
        prob_of_last_particle = emit_n%1
        emit_last = np.random.uniform() < prob_of_last_particle
        num_to_emit = for_sure + emit_last
        for i in range(num_to_emit):
            self.emit()

        for p in self.particles:
            p.act()

        self.particles = [p for p in self.particles if p.alive > -1]

    def draw(self):
        raise NotImplementedError


class RainMaker(ParticleEmitter):
    def __init__(self, emit_rate, angle, window_size):
        super(RainMaker, self).__init__(emit_rate, (0, 0))
        self.angle = angle
        self.window_size = window_size

        # shades of blue
        self.colors = [
                [25, 25, 100],
                [40, 75, 125],
                [50, 20, 150],
                ]

    def emit(self):
        randsize = np.random.randint(1, 2)
        randx = np.random.randint(0, self.window_size[0])
        randy = np.random.randint(-self.window_size[1], 0)
        deathtime = np.random.randint(200, 300)
        randcolor = self.colors[np.random.randint(0, 3)]
        direction = np.random.randint(self.angle-5, self.angle+5)
        behaviors = [
                ParticleBehaviours.get_age_callback(10),  
                ParticleBehaviours.get_wind_callback(5, 30),  
                ParticleBehaviours.get_fade_callback(0.1),  
                ParticleBehaviours.get_movement_callback(20, direction),  
                ParticleBehaviours.get_deathtime_callback(deathtime)]  
        p=Particle((randx, randy), randsize, randcolor, behaviors)
        self.particles.append(p)

    def draw(self):
        for p in self.particles:
            if p.alpha < 0:
                continue
            s = pg.Surface((2*p.size, 2*p.size))
            s.convert_alpha()
            s.fill((255, 255, 255))
            s.set_colorkey((255, 255, 255))

            pg.draw.circle(s, p.color,
                    map(int, (p.size, p.size)), int(p.size))
            s.set_alpha(int(p.alpha*255))

            en.Graphics.draw_image(s, np.array(p.pos)-p.size)


class SmokeMachine(ParticleEmitter):
    def __init__(self, emit_rate, size, angle, hang_time, age_rate, fade_rate, position):
        super(SmokeMachine, self).__init__(emit_rate, position)
        self.angle=angle
        self.size=size
        self.hang_time=hang_time
        self.age_rate=age_rate
        self.fade_rate=fade_rate
        self.colors = [
                [120, 120, 120],
                [125, 125, 125],
                [130, 130, 130],
                ]

    def emit(self):
            randsize = np.random.randint(self.size-2, self.size+2)
            deathtime = np.random.randint(self.hang_time-100, self.hang_time+100)
            randcolor = self.colors[np.random.randint(0, 3)]
            direction = np.random.randint(self.angle-5, self.angle+5)
            behaviors = [
                    ParticleBehaviours.get_age_callback(self.age_rate),  
                    ParticleBehaviours.get_wind_callback(2, 30),  
                    ParticleBehaviours.get_fade_callback(self.fade_rate),  
                    ParticleBehaviours.get_grow_callback(0.08),  
                    ParticleBehaviours.get_movement_callback(7, direction),  
                    ParticleBehaviours.get_deathtime_callback(deathtime)]  
            p=Particle(self.position, randsize, randcolor, behaviors)
            self.particles.append(p)

    def draw(self):
        for p in self.particles:
            if p.alpha < 0:
                continue
            s = pg.Surface((2*p.size, 2*p.size))
            s.convert_alpha()
            s.fill((255, 255, 255))
            s.set_colorkey((255, 255, 255))

            pg.draw.circle(s, p.color,
                    map(int, (p.size, p.size)), int(p.size))
            s.set_alpha(int(p.alpha*255))


            en.Graphics.draw_image(s, np.array(p.pos)-p.size)

