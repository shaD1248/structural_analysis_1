import util
from collection_item import CollectionItem

class Node(CollectionItem):
    def __init__(self, position: list, force: list = [0, 0, 0, 0, 0, 0], rigidity_int: int = 0b111):
        self.position = position
        self.force = force
        self.rigidity_matrix = util.get_rigidity_matrix(rigidity_int, 6)
