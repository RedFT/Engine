import engine as en


class Scene(en.Node):
    def __init__(self):
        super(Scene, self).__init__()

    def initialize(self):
        raise NotImplementedError("Has not been implemented.")

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self):
        for child in self.children:
            child.draw()

    def pause(self):
        raise NotImplementedError("Has not been implemented.")

    def resume(self):
        raise NotImplementedError("Has not been implemented.")

    def exit(self):
        raise NotImplementedError("Has not been implemented.")
