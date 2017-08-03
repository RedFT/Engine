import graphics
import text
import entity
import app

class Label(entity.Entity):
    def __init__(self, text, font="Unique.ttf", size=16, position=(0, 0), color=(255, 255, 255), aa=True):
        super(Label, self).__init__(position)
        self.anchorx = 'center'
        self.anchory = 'center'

        # Some hold on to ctor args
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.aa = aa

        # Setup image and geometry
        self.image = None
        self.rect = None
        self.width = None
        self.height = None

        # Setup Drawing positions
        self.position = None
        self.draw_position = None

        # Fill in attributes
        self.regenerate_text()
        self.set_position(position)


    def set_position(self, position):
        self.position = position
        self.set_draw_position()

    def set_draw_position(self):
        self.draw_position = list(self.position)
        if self.anchorx == 'center':
            self.draw_position[0] -= self.width / 2
        if self.anchory == 'center':
            self.draw_position[1] -= self.height/ 2

        self.rect.x = self.draw_position[0]
        self.rect.y = self.draw_position[1]

    def set_size(self, size):
        self.size = size
        self.regenerate_text()
        self.set_draw_position()

    def set_font(self, font):
        self.font = font
        self.regenerate_text()
        self.set_draw_position()

    def regenerate_text(self):
        self.image = text.create_text(
            self.font,
            self.size,
            self.text,
            aa=self.aa,
            color=self.color)
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def update(self, dt):
        pass

    def draw(self):
        surf = app.get_current_scene().scene_surface
        surf.blit(self.image, self.draw_position)

    def notify(self, event, sender, data):
        pass
