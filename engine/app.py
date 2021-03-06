import pygame as pg
import engine as en

class AppParams:
        game_clock = pg.time.Clock()
        screen_width = None
        screen_height = None
        screen_size = None
        caption = None
        scale = None
        show_fps = None
        show_scene_stack = None

def initialize(screen_size=(640, 420), caption="App", scale=1, show_fps=True, show_scene_stack=True):
    AppParams.screen_width, AppParams.screen_height = AppParams.screen_size = screen_size
    AppParams.caption = caption
    AppParams.scale = scale
    AppParams.show_fps = show_fps
    AppParams.show_scene_stack = show_scene_stack

    # initialize pygame
    pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    pg.init()
    AppParams.game_clock = pg.time.Clock()

    en.graphical_logger.initialize((5, 5), AppParams.screen_width/ 2, 4000)
    en.text.initialize()

    # initialize graphics stuff
    en.graphics.initialize(AppParams.screen_size, AppParams.caption, AppParams.scale)
    en.graphics.set_clear_color((200, 200, 200))

    # create scene stack
    AppParams.scenes = []

def get_current_scene():
    return AppParams.scenes[-1]

def get_screen_size():
    return AppParams.screen_size

def push_scene(scene):
    if AppParams.scenes != []:
        AppParams.scenes[-1].exit()

    AppParams.scenes.append(scene)
    AppParams.scenes[-1].initialize()
    AppParams.scenes[-1].enter()

def pop_scene():
    popped_scene = AppParams.scenes.pop()
    popped_scene.exit()
    AppParams.scenes[-1].enter()

def pop_to_scene(index):
    if len(AppParams.scenes) <= index:
        raise IndexError

    if AppParams.scenes != []:
        AppParams.scenes[-1].exit()

    AppParams.scenes = AppParams.scenes[:index+1]
    AppParams.scenes[-1].enter()

def main_loop():
    if AppParams.scenes == []:
        print("No scenes on scene stack")

    while AppParams.scenes:
        dt= AppParams.game_clock.tick(60)

        # Event Handling
        got_quit = en.events.handle_events(dt)
        if got_quit:
            quit()

        # Game Logic
        AppParams.scenes[-1].update(dt)
        en.graphical_logger.update(dt)

        # Handle Messages in Message Queue
        en.pubsub.handle_messages(dt)

        # Game Rendering
        AppParams.scenes[-1].draw()

        en.graphics.draw_image(AppParams.scenes[-1].scene_surface,
            (0, 0))

        # Some debugging text on screen
        if AppParams.show_fps:
            fps = AppParams.game_clock.get_fps()
            fps_surf = en.text.create_text('Unique.ttf', 16, "%.2ffps" % (int(fps)), aa=True)
            en.graphics.draw_image(fps_surf, (AppParams.screen_width - fps_surf.get_rect().width, 0))

        if AppParams.show_scene_stack:
            current_x = 0
            current_y = AppParams.screen_height - en.text.check_height('Unique.ttf', 16, 'test')
            for scene in AppParams.scenes:
                scene_name = "_" + scene.__class__.__name__ + "_"
                scene_name_surf = en.text.create_text('Unique.ttf', 16, scene_name, aa=True)

                text_rect = scene_name_surf.get_rect()
                #pg.draw.rect(scene_name_surf, (200, 200, 200), text_rect, 1)
                en.graphics.draw_image(scene_name_surf, (current_x, current_y))

                current_y -= text_rect.height

        # Draw Logger
        en.graphical_logger.draw()

        en.graphics.flip()
        en.graphics.clear()

def quit():
    pg.quit()
    exit(0)

if __name__ == "__main__":
    app = App()
    app.main_loop()
