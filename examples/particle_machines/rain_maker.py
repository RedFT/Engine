import numpy as np
import engine as en


class RainMaker(en.particles.ParticleEmitter):
    def __init__(self, emit_rate, size, angle, hang_time, age_rate, fade_rate, move_speed, window_size):
        super(RainMaker, self).__init__(emit_rate, (0, 0))
        self.angle = angle
        self.window_size = window_size
        self.angle = angle
        self.size = size
        self.rect = [self.position[0]-size/2, self.position[1]-size/2, size, size]
        self.hang_time = hang_time
        self.age_rate = age_rate
        self.fade_rate = fade_rate
        self.move_speed = move_speed

        # shades of blue
        self.colors = [
            [100, 100, 240],
            [120, 110, 210],
            [140, 100, 220],
        ]

    def update(self, dt):
        super(RainMaker, self).update(dt)
        for p in self.particles:
            if p.position[0] > self.window_size[0]:
                p.set_pos((0, p.y))
        return self.particles

    def emit(self):
        # Get random parameters
        #random_size = np.random.randint(self.size, self.size + 1)
        random_size = 1
        random_x = np.random.randint(0, self.window_size[0])
        random_y = -np.random.randint(0, self.window_size[1]/2)
        deathtime = np.random.randint(self.hang_time - 100, self.hang_time + 100)
        random_color = self.colors[np.random.randint(0, 3)]
        direction = np.random.randint(self.angle - 5, self.angle + 5)

        # Setup behavior of particle
        behaviors = [
            en.particles.ParticleBehaviors.get_age_callback(self.age_rate),
            #en.particles.ParticleBehaviors.get_wind_callback(5, 30),
            en.particles.ParticleBehaviors.get_fade_callback(self.fade_rate),
            en.particles.ParticleBehaviors.get_movement_callback(self.move_speed, direction),
            en.particles.ParticleBehaviors.get_deathtime_callback(deathtime)
            ]

        # Create particle
        p = en.particles.Particle((random_x, random_y), random_size, random_color, behaviors)
        self.particles.append(p)
