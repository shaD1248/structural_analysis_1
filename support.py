from node import Node

class Support():
    def __init__(self, node: Node, cosine_matrix: list, rigidity: list):
        self.node = node
        self.cosine_matrix = cosine_matrix
        self.rigidity = rigidity
    
