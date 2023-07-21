import util
from collection_item import CollectionItem
import math
from material import Material
from node import Node
import numpy as np
from section import Section


class Element(CollectionItem):
    def __init__(self,
                 node_0: Node,
                 node_1: Node,
                 section: Section = Section(1, 1, 1, 2),
                 material: Material = Material(200, 0.3),
                 theta: float = 0,
                 rigidity_int: int = 0b000111001111):
        self.node_0 = node_0
        self.node_1 = node_1
        self.L = math.dist(node_0.position, node_1.position)
        self.theta = theta
        self.calculate_cosine_matrix()

        self.section = section
        self.A = section.A
        self.I2 = section.I2
        self.I3 = section.I3
        self.J = section.J

        self.material = material
        self.E = material.E
        self.G = material.G

        self.rigidity_matrix = util.get_rigidity_matrix(rigidity_int, 12)

    def get_nodes(self):
        return [self.node_0, self.node_1]

    def calculate_cosine_matrix(self):
        x1 = self.node_0.position
        x2 = self.node_1.position
        X = [(x2[i] - x1[i]) / self.L for i in range(0, 3)]
        if abs(X[2]) != 1:
            Z = np.cross(X, [0, 0, 1])
            Z = Z / np.linalg.norm(Z)
        else:
            Z = [1, 0, 0]
        Y = np.cross(Z, X)
        theta_rad = math.radians(self.theta)
        cos = math.cos(theta_rad)
        sin = math.sin(theta_rad)
        self.cosine_matrix = np.matmul([[1, 0, 0], [0, cos, sin], [0, -sin, cos]], [X, Y, Z])

    # P V2 V3  T M2 M3
    # 0  1  2  3  4  5
    # 6  7  8  9 10 11
    def get_K(self):
        L = self.L
        A = self.A
        I3 = self.I3
        I2 = self.I2
        J = self.J
        E = self.E
        G = self.G
        K = np.zeros([12, 12])
        for k in [0, 1]:
            for l in [0, 1]:
                K[6 * k + 0][6 * l + 0] = (-1) ** (k + l) * A * E / L
                K[6 * k + 1][6 * l + 1] = (-1) ** (k + l) * 12 * E * I3 / L ** 3
                K[6 * k + 2][6 * l + 2] = (-1) ** (k + l) * 12 * E * I2 / L ** 3
                K[6 * k + 1][6 * l + 5] = (-1) ** (k + 0) * 6 * E * I3 / L ** 2
                K[6 * k + 2][6 * l + 4] = (-1) ** (k + 1) * 6 * E * I2 / L ** 2
                K[6 * k + 4][6 * l + 2] = (-1) ** (l + 1) * 6 * E * I2 / L ** 2
                K[6 * k + 5][6 * l + 1] = (-1) ** (l + 0) * 6 * E * I3 / L ** 2
                K[6 * k + 5][6 * l + 5] = (3 + (-1) ** (k + l)) * E * I3 / L
                K[6 * k + 4][6 * l + 4] = (3 + (-1) ** (k + l)) * E * I2 / L
                K[6 * k + 3][6 * l + 3] = (-1) ** (k + l) * G * J / L
        return K

    def get_T(self):
        T3 = self.cosine_matrix
        T = np.zeros([12, 12])
        for k in range(0, 4):
            for l in range(0, 3):
                for m in range(0, 3):
                    T[3 * k + l][3 * k + m] = T3[l][m]
        return T