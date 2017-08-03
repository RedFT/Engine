if __name__ == '__main__':
    import engine as en
    from particles_scene import ParticlesScene
    en.app.initialize(
        (640, 420),
        "Particles Example",
        2,
        True)

    en.app.push_scene(ParticlesScene())
    en.app.main_loop()
