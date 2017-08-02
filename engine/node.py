class Node(object):
    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)

    def enter(self):
        pass

    def exit(self):
        self.children = []
