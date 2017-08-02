if __name__ == '__main__':
    import engine as en
    import constants as cn
    from test_scene import TestScene
    en.app.initialize(cn.WINDOW_SIZE,
        cn.WINDOW_CAPTION,
        cn.SCALE,
        cn.SHOW_FPS)

    en.app.push_scene(TestScene())
    en.app.main_loop()
