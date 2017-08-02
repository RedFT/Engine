if __name__ == '__main__':
    import engine as en
    import constants as cn
    from test_scene import TestScene
    app = en.app.App(cn.WINDOW_SIZE,
        cn.WINDOW_CAPTION,
        cn.SCALE,
        cn.SHOW_FPS)

    app.push_scene(TestScene())
    app.main_loop()
