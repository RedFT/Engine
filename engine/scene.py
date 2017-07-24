class Scene(object):
    def __init__(self):
        pass

    def initialize(self):
        raise NotImplementedError("Has not been implemented.")

    def update(self, dt):
        raise NotImplementedError("Has not been implemented.")

    def draw(self):
        raise NotImplementedError("Has not been implemented.")

    def pause(self):
        raise NotImplementedError("Has not been implemented.")

    def resume(self):
        raise NotImplementedError("Has not been implemented.")

    def exit(self):
        raise NotImplementedError("Has not been implemented.")
