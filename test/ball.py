import pygame as pg
import engine as en
import numpy as np
import constants as cn


class Ball(object):
    class FallingState(en.State):
        def __init__(self, owner):
            super(Ball.FallingState, self).__init__(owner)
            self.enter()

        def enter(self):
            pass

        def update(self, dt):
            if en.Keyboard.is_held(pg.K_LEFT):
                self.owner.move_velocity -= self.owner.move_acceleration
            if en.Keyboard.is_held(pg.K_RIGHT):
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
            if en.Keyboard.is_held(pg.K_LEFT):
                self.owner.move_velocity -= self.owner.move_acceleration
            if en.Keyboard.is_held(pg.K_RIGHT):
                self.owner.move_velocity += self.owner.move_acceleration

            if self.owner.move_velocity > 1:
                self.owner.move_acceleration = 1
            if self.owner.move_velocity < -1:
                self.owner.move_acceleration = -1

            self.owner.position[0] += self.owner.move_velocity * dt

            if en.Keyboard.was_pressed(pg.K_SPACE):
                en.PubSub.publish("jumped", self)
                return

            self.owner.fall_velocity += self.owner.gravity[1] * dt
            self.owner.position[1] += self.owner.fall_velocity * dt

            if abs(self.owner.position[1] - self.guessed_height) > 2:
                en.PubSub.publish("fell", self)
                return
            self.guessed_height = self.owner.position[1]


    def __init__(self, pos=(0, 0)):
        en.PubSub.subsribe(self, "jumped")
        en.PubSub.subsribe(self, "collision")
        en.PubSub.subsribe(self, "fell")

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
            self.state = self.jumping_state
            self.state.enter()
        elif event == "collision" and self in data:
            other = data[0] if data[1] is self else data[1]
            self.fall_velocity = 0
            self.set_y(other.rect[1] - self.radius)
            self.state = self.standing_state
            self.state.enter()
            en.PubSub.publish("landed", self)
        elif event == "fell" and sender is self.standing_state:
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

    def draw(self):
        pg.draw.circle(en.Graphics.get_main_surface(), (255, 0, 0),
                       map(int, self.position), self.radius)
        pg.draw.rect(en.Graphics.get_main_surface(), (255, 0, 0),
                     self.rect, 1)
