import pygame as pg
import engine as en



class App:
    def __init__(self, screen_size=(640, 420), caption="App", scale=1, show_fps=True):
        self.screen_width, self.screen_height = self.screen_size = screen_size
        self.caption = caption
        self.scale = scale
        self.show_fps = show_fps

        # initialize pygame
        pg.init()
        self.game_clock = pg.time.Clock()

        en.graphical_logger.initialize((5, 5), self.screen_width/ 2, 4000)
        en.text.initialize()

        # initialize graphics stuff
        en.graphics.initialize(self.screen_size, self.caption, self.scale)
        en.graphics.set_clear_color((200, 200, 200))

        # create scene stack
        self.scenes = []

    def push_scene(self, scene):
        self.scenes.append(scene)
        self.scenes[-1].initialize()

    def pop_scene(self):
        return self.scenes.pop()


    def main_loop(self):
        if self.scenes == []:
            print "No scenes on scene stack"

        while self.scenes:
            dt= self.game_clock.tick(30)

            # Event Handling
            got_quit = en.events.handle_events(dt)
            if got_quit or en.keyboard.was_pressed(pg.K_ESCAPE):
                break

            # Game Logic
            self.scenes[-1].update(dt)
            en.graphical_logger.update(dt)

            # Handle Messages in Message Queue
            en.pubsub.update(dt)

            # Game Rendering
            self.scenes[-1].draw()

            # Some debugging text on screen
            if self.show_fps:
                fps = self.game_clock.get_fps()
                fps_surf = en.text.create_text('Unique.ttf', 16, "%.2ffps" % (int(fps)), aa=True)
                en.graphics.draw_image(fps_surf, (self.screen_width - fps_surf.get_rect().width, 0))

            # Draw Logger
            en.graphical_logger.draw()

            en.graphics.flip()
            en.graphics.clear()
        self.quit()

    def quit(self):
        pg.quit()


if __name__ == "__main__":
    app = App()
    app.main_loop()
