import pygame as pg
import engine as en
import numpy as np
from platform import Platform
import constants as cn


class Ball(en.Entity):
    class FallingState(en.State):
        def __init__(self, owner):
            super(Ball.FallingState, self).__init__(owner)
            self.enter()

        def enter(self):
            pass

        def update(self, dt):
            if en.keyboard.is_held(pg.K_LEFT):
                self.owner.move_velocity -= self.owner.move_acceleration
            if en.keyboard.is_held(pg.K_RIGHT):
                self.owner.move_velocity += self.owner.move_acceleration

            if self.owner.move_velocity > 1:
                self.owner.move_acceleration = 1
            if self.owner.move_velocity < -1:
                self.owner.move_acceleration = -1

            self.owner.position[0] += self.owner.move_velocity * dt
            self.owner.fall_velocity += self.owner.gravity[1] * dt
            self.owner.set_y(
                self.owner.position[1] + self.owner.fall_velocity * dt)

    class JumpingState(en.State):
        def __init__(self, owner):
            super(Ball.JumpingState, self).__init__(owner)
            self.initial_velocity = np.array([self.owner.move_velocity, self.owner.jump_velocity])
            self.initial_position = self.owner.position.copy()
            self.jump_duration = .0

        def enter(self):
            self.initial_velocity = np.array([self.owner.move_velocity, self.owner.jump_velocity])
            self.initial_position = self.owner.position.copy()
            self.jump_duration = .0

        def calculate_new_motion_parameters(self):
            # Projectile Motion
            new_pos = .5 * self.owner.gravity * self.jump_duration ** 2
            new_pos += self.initial_velocity * self.jump_duration
            new_pos += self.initial_position

            self.owner.set_position(new_pos)
            return new_pos

        def update(self, dt):
            self.jump_duration += dt
            self.calculate_new_motion_parameters()

    class StandingState(en.State):
        def __init__(self, owner):
            super(Ball.StandingState, self).__init__(owner)
            self.guessed_height = self.owner.position[1]

        def enter(self):
            self.guessed_height = self.owner.position[1]

        def update(self, dt):
            if en.keyboard.is_held(pg.K_LEFT):
                self.owner.move_velocity -= self.owner.move_acceleration
            if en.keyboard.is_held(pg.K_RIGHT):
                self.owner.move_velocity += self.owner.move_acceleration

            if self.owner.move_velocity > 1:
                self.owner.move_acceleration = 1
            if self.owner.move_velocity < -1:
                self.owner.move_acceleration = -1

            self.owner.position[0] += self.owner.move_velocity * dt

            if en.keyboard.was_pressed(pg.K_SPACE):
                en.pubsub.publish("jumped", self)
                return

            self.owner.fall_velocity += self.owner.gravity[1] * dt
            self.owner.position[1] += self.owner.fall_velocity * dt

            if abs(self.owner.position[1] - self.guessed_height) > 2:
                en.pubsub.publish("fell", self)
                return
            self.guessed_height = self.owner.position[1]


    def __init__(self, pos=(0, 0)):
        en.pubsub.subscribe(self, "jumped")
        en.pubsub.subscribe(self, "collision")
        en.pubsub.subscribe(self, "fell")

        self.radius = 20
        self.position = np.array(pos, dtype=float)
        self.rect = np.concatenate([self.position - self.radius,
                                    [2 * self.radius, 2 * self.radius]])
        self.jump_velocity = -.4
        self.move_velocity = 0
        self.move_acceleration = .01
        self.fall_velocity = 0
        self.gravity = np.array([0, .001])
        self.init_pos = self.position.copy()
        self.init_vel = np.array([0, 0])

        self.standing_state = Ball.StandingState(self)
        self.jumping_state = Ball.JumpingState(self)
        self.falling_state = Ball.FallingState(self)
        self.state = self.standing_state

    def notify(self, event, sender, data):
        if event == "jumped" and sender is self.standing_state:
            en.graphical_logger.log("Ball Jumped")
            self.state = self.jumping_state
            self.state.enter()
        elif event == "collision" and self in data:
            other = data[0] if data[1] is self else data[1]
            if type(other) is en.Particle:
                return

            self.fall_velocity = 0
            self.set_y(other.rect[1] - self.radius)
            self.state = self.standing_state
            self.state.enter()
            en.pubsub.publish("landed", self)
        elif event == "fell" and sender is self.standing_state:
            en.graphical_logger.log("Ball Fell")
            self.state = self.falling_state
            self.state.enter()

    def set_position(self, new_pos):
        self.position = new_pos
        self.rect[0] = self.position[0] - self.radius
        self.rect[1] = self.position[1] - self.radius

    def set_y(self, new_y):
        self.position[1] = new_y
        self.rect[1] = self.position[1] - self.radius

    def set_x(self, new_x):
        self.position[0] = new_x
        self.rect[0] = self.position[0] - self.radius

    def update(self, dt):
        self.state.update(dt)
        self.rect[0] = self.position[0] - self.radius
        self.rect[1] = self.position[1] - self.radius
        return self

    def draw(self):
        new_rect = pg.Rect(self.rect)
        new_rect[0] = self.camera_coordinates[0]-self.rect[2]/2
        new_rect[1] = self.camera_coordinates[1]-self.rect[3]/2
        pg.draw.circle(en.graphics.get_main_surface(), (255, 0, 0),
                       map(int, self.camera_coordinates), self.radius)
        pg.draw.rect(en.graphics.get_main_surface(), (255, 0, 0),
                     new_rect, 1)
