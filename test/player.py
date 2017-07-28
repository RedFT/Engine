import constants as cn
import pygame as pg
import engine as en


class Player(en.Entity):
    def __init__(self, position):
        self.image = en.graphics.load_image("WalkingAnimationTemplate.png")
        self.image_out = self.image
        self.rect = self.image.get_rect()
        super(Player, self).__init__(position, self.rect.width, self.rect.height)
        self.animation = en.Animation(10)
        self.animation.load_animation_file("WalkingAnimationTemplate.json", cn.SCALE)
        self.rect = self.animation.get_new_frame_rect(0)

    def update(self, dt):
        print dt
        if (en.keyboard.is_held(pg.K_LEFT)):
            self.position[0] -= .1*dt
        if (en.keyboard.is_held(pg.K_RIGHT)):
            self.position[0] += .1*dt

        self.position[1] += .1*dt

        frame_rect=self.animation.get_new_frame_rect(dt)

        self.image_out = self.image.subsurface(frame_rect)
        self.rect[:2] = self.position
        return self

    def draw(self):
        en.graphics.draw_image(self.image_out, self.camera_coordinates)

    def notify(self, event, sender, data):
        pass
