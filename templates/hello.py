import engine as en
import constants as cn


class Hello(en.Scene):
    def initialize(self):
        self.hello_text_surf = en.Text.create_text("Unique.ttf", 20, "Hello World", True, (200, 150, 100))

    def update(self, dt):
        pass

    def draw(self):
        en.Graphics.draw_image(self.hello_text_surf,
                               (cn.SCREEN_WIDTH/2-self.hello_text_surf.get_width()/2,
                               cn.SCREEN_HEIGHT/2-self.hello_text_surf.get_height()/2))

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
