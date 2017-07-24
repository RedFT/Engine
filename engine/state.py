class State(object):
    def __init__(self, owner):
        self.owner = owner

    def enter(self):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

