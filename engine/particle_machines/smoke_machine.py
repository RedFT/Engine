import numpy as np
import pygame as pg

from engine.engine import particles


class SmokeMachine(particles.ParticleEmitter):
    def __init__(self, emit_rate, size, angle, hang_time, age_rate, fade_rate, position):
        super(SmokeMachine, self).__init__(emit_rate, position)
        self.angle = angle
        self.size = size
        self.hang_time = hang_time
        self.age_rate = age_rate
        self.fade_rate = fade_rate
        self.colors = [
            [120, 120, 120],
            [125, 125, 125],
            [130, 130, 130],
        ]

    def emit(self):
        random_size = np.random.randint(self.size, self.size + 4)
        death_time = np.random.randint(self.hang_time - 100, self.hang_time + 100)
        rand_color = self.colors[np.random.randint(0, 3)]
        direction = np.random.randint(self.angle - 5, self.angle + 5)
        behaviors = [
            particles.ParticleBehaviors.get_age_callback(self.age_rate),
            particles.ParticleBehaviors.get_wind_callback(2, 30),
            particles.ParticleBehaviors.get_fade_callback(self.fade_rate),
            particles.ParticleBehaviors.get_grow_callback(0.08),
            particles.ParticleBehaviors.get_movement_callback(7, direction),
            particles.ParticleBehaviors.get_deathtime_callback(death_time)]
        p = particles.Particle(self.position, random_size, rand_color, behaviors)
        self.particles.append(p)
