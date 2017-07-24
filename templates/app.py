import numpy as np
import pygame as pg
import engine as en
import constants as cn

from templates.hello import Hello

class App:
    def __init__(self):
        # initialize pygame
        pg.init()
        self.game_clock = pg.time.Clock()

        # initialize graphics stuff
        en.Graphics.initialize(cn.WINDOW_SIZE, cn.WINDOW_CAPTION, cn.SCALE)
        en.Graphics.set_clear_color((200, 200, 200))
        en.Text.initialize()

        en.GraphicalLogger.initialize((5, 5), cn.SCREEN_WIDTH/2, 4000)

        self.scenes = []
        # create scene stack
        s1=Hello()
        s1.initialize()
        self.scenes.append(s1)


    def main_loop(self):
        while self.scenes:
            dt = self.game_clock.tick(30)

            # Event Handling
            got_quit = en.Input.handle_events(dt) 
            if got_quit:
                break

            if en.Keyboard.was_pressed(pg.K_ESCAPE): # convenient
                break

            # Game Logic
            self.scenes[-1].update(dt)
            en.GraphicalLogger.update(dt)

            # Game Rendering
            self.scenes[-1].draw()

            fps=self.game_clock.get_fps()
            fps_surf = en.Text.create_text('Unique.ttf', 16, "%.2ffps"%(int(fps)), aa=True)
            en.Graphics.draw_image(fps_surf, (cn.SCREEN_WIDTH-fps_surf.get_rect().width, 0))

            # Draw Logger
            en.GraphicalLogger.draw()

            en.Graphics.flip()
            en.Graphics.clear()
        self.quit()

    def quit(self):
        pg.quit()


if __name__ == "__main__":
    app = App()
    app.main_loop()

