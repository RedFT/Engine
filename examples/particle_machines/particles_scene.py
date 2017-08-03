import engine as en

from rain_maker import RainMaker
from smoke_machine import SmokeMachine

class ParticlesScene(en.scene.Scene):
    def __init__(self):
        super(ParticlesScene, self).__init__()

    def initialize(self):
        rain_maker = RainMaker(
            emit_rate=100,
            size=3,
            angle=90,
            hang_time=1000,
            age_rate=10,
            fade_rate=.02,
            move_speed=20,
            window_size=(640, 480)
        )

        self.add(rain_maker)
        smoke_machine = SmokeMachine(
            (100, 400),
            fade_rate=.03,
            grow_speed=.2,
            hang_time=2000,
            age_rate=10,
            move_speed=2
        )
        self.add(smoke_machine)

    def enter(self):
        super(ParticlesScene, self).enter()
        en.graphics.set_clear_color((10, 10, 50))

    def pause(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass
