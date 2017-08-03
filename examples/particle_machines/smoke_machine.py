import numpy as np
import engine as en

class SmokeMachine(en.particles.ParticleEmitter):
    def __init__(self, position, emit_rate=10, size=5, angle=-90, hang_time=1000, age_rate=25, fade_rate=.1, move_speed=5, grow_speed=.08):
        super(SmokeMachine, self).__init__(emit_rate, position)
        self.angle = angle
        self.size = size
        self.hang_time = hang_time
        self.age_rate = age_rate
        self.fade_rate = fade_rate
        self.move_speed = move_speed
        self.grow_speed = grow_speed
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
            en.particles.ParticleBehaviors.get_age_callback(self.age_rate),
            en.particles.ParticleBehaviors.get_wind_callback(2, 30),
            en.particles.ParticleBehaviors.get_fade_callback(self.fade_rate),
            en.particles.ParticleBehaviors.get_grow_callback(self.grow_speed),
            en.particles.ParticleBehaviors.get_movement_callback(self.move_speed, direction),
            en.particles.ParticleBehaviors.get_deathtime_callback(death_time)]
        p = en.particles.Particle(self.position, random_size, rand_color, behaviors)
        self.particles.append(p)
