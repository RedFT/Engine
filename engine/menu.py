import entity
import pubsub
import mouse

class Menu(entity.Entity):
    """A Menu object for storing 'selectable' labels."""
    def __init__(self, parent):
        super(Menu, self).__init__((0, 0))
        self.parent = parent # The object that contains an instance of this class
        self.cb_map = {} # "callback map" maps labels to callbacks + args

    def add(self, node, callback):
        super(Menu, self).add(node)
        self.cb_map[node] = callback

    def enter(self):
        super(Menu, self).enter()

    def exit(self):
        super(Menu, self).exit()
        pubsub.unsubscribe_to_all_messages(self)

    def update(self, dt):
        if mouse.was_pressed(0):
            click_pos = mouse.get_position()
            for child in self.children:
                if not child.rect.collidepoint(click_pos):
                    continue

                if child not in self.cb_map.keys():
                    continue

                self.cb_map[child](child)

        for child in self.children:
            child.update(dt)

    def draw(self):
        for child in self.children:
            child.draw()

    def notify(self, event, sender, data):
        pass
