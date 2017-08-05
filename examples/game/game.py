if __name__ == '__main__':
    import engine as en
    from . import constants as cn
    from .main_menu_scene import MainMenuScene

    en.app.initialize(cn.WINDOW_SIZE,
        cn.WINDOW_CAPTION,
        cn.SCALE,
        cn.SHOW_FPS)

    en.app.push_scene(MainMenuScene())
    en.app.main_loop()
