import graphical_logger

class Node(object):
    def __init__(self):
        self.children = []

    def add(self, node):
        self.children.append(node)

    def enter(self):
        #graphical_logger.log("Entering " + self.__class__.__name__)
        for child in self.children:
            child.enter()

    def exit(self):
        #graphical_logger.log("Exiting " + self.__class__.__name__)
        for child in self.children:
            child.exit()
