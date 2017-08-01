import pygame as pg
import engine as en

import constants as cn

from hello import Hello


class App:
    def __init__(self):
        # initialize pygame
        pg.init()
        self.game_clock = pg.time.Clock()

        en.graphical_logger.initialize((5, 5), cn.SCREEN_WIDTH / 2, 4000)
        en.text.initialize()

        # initialize graphics stuff
        en.graphics.initialize(cn.WINDOW_SIZE, cn.WINDOW_CAPTION, cn.SCALE)
        en.graphics.set_clear_color((200, 200, 200))

        # create scene stack
        self.scenes = [Hello()]
        self.scenes[-1].initialize()

    def main_loop(self):
        while self.scenes:
            dt= self.game_clock.tick(30)

            # Event Handling
            got_quit = en.events.handle_events(dt)
            if got_quit or en.keyboard.was_pressed(pg.K_ESCAPE):
                break

            # Game Logic
            self.scenes[-1].update(dt)
            en.graphical_logger.update(dt)

            # Game Rendering
            self.scenes[-1].draw()

            # Some debugging text on screen
            fps = self.game_clock.get_fps()
            fps_surf = en.text.create_text('Unique.ttf', 16, "%.2ffps" % (int(fps)), aa=True)
            en.graphics.draw_image(fps_surf, (cn.SCREEN_WIDTH - fps_surf.get_rect().width, 0))

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
