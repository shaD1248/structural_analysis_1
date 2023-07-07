import pandas as pd
from collection import Collection
from displacement import Displacement
import numpy as np
import rref


class Analyzer:
    def __init__(self, nodes: list, elements: list):
        self.nodes = nodes
        self.elements = elements

    def analyze(self):
        self.generate_displacements()
        self.transform_global_to_element_local()
        self.generate_stiffness_matrix()
        self.generate_partitioning_matrices()
        self.generate_forces_matrix()
        self.calculate_displacements()
        self.calculate_element_forces()
        self.print_results()

    def generate_displacements(self):
        displacements = []
        self.displacement_map = {'nodes': np.zeros([len(self.nodes), 6]), 'elements': np.zeros([len(self.elements), 12])}
        for node in self.nodes:
            i = node.id
            for j in range(0, 6):
                self.displacement_map['nodes'][i][j] = len(displacements)
                displacements.append(Displacement('node', i, j, node.rigidity_matrix[j] == 1))
        for element in self.elements:
            i = element.id
            for j in range(0, 12):
                if element.rigidity_matrix[j] == 1:
                    self.displacement_map['elements'][i][j] = -1
                else:
                    self.displacement_map['elements'][i][j] = len(displacements)
                    displacements.append(Displacement('element', i, j, False))
        self.displacements = Collection(displacements).list

    def transform_global_to_element_local(self):
        self.T = []
        for element in self.elements:
            i = element.id
            element_T = element.get_T()
            T = np.zeros([12, len(self.displacements)])
            for j in range(0, 12):
                displacement_id = int(self.displacement_map['elements'][i][j])
                if displacement_id >= 0:
                    T[j][displacement_id] = 1
                else:
                    member_end = j // 6
                    node = element.get_nodes()[member_end]
                    node_map = self.displacement_map['nodes'][node.id]
                    for k in range(0, 6):
                        displacement_id = int(node_map[k])
                        T[j][displacement_id] += element_T[j][6 * member_end + k]
            self.T.append(T)

    def generate_stiffness_matrix(self):
        self.element_K = []
        self.K = np.zeros([len(self.displacements), len(self.displacements)])
        for element in self.elements:
            i = element.id
            T = self.T[i]
            element_K = element.get_K()
            K = self.quad(T, element_K, T)
            self.element_K.append(K)
            self.K += K

    def generate_forces_matrix(self):
        P = np.zeros([len(self.displacements), 1])
        for node in self.nodes:
            i = node.id
            node_map = self.displacement_map['nodes'][i]
            for j in range(0, 6):
                displacement_id = int(node_map[j])
                P[displacement_id][0] = node.force[j]
        self.P = P

    def generate_partitioning_matrices(self):
        f = []
        s = []
        for displacement in self.displacements:
            i = displacement.id
            if displacement.supported:
                s.append(i)
            else:
                f.append(i)
        self.f = np.array([[1 * (i == f[j]) for j in range(0, len(f))] for i in range(0, len(self.displacements))])
        self.s = np.array([[1 * (i == s[j]) for j in range(0, len(s))] for i in range(0, len(self.displacements))])

    def calculate_displacements(self):
        Pf = np.transpose(self.f) @ self.P
        Kff = self.quad(self.f, self.K, self.f)
        Kfs = self.quad(self.f, self.K, self.s)
        Ksf = self.quad(self.s, self.K, self.f)
        Kss = self.quad(self.s, self.K, self.s)
        Ds = np.zeros([len(self.s[0]), 1])
        if np.linalg.matrix_rank(Kff) != len(Kff):
            self.inv_test(Kff)
        # Pf = Kff * Df + Kfs * Ds
        # Df = Kff^(-1) * (Pf - Kfs * Ds)
        invKff = np.linalg.inv(Kff)
        Df = invKff @ (Pf - Kfs @ Ds)
        # Ps = Ksf * Df + Kss * Ds
        Ps = Ksf @ Df + Kss @ Ds
        self.D = self.zero(self.f @ Df + self.s @ Ds)
        self.P = self.zero(self.K @ self.D)

    def inv_test(self, A):
        message = 'The stiffness matrix is singular. The structure is unstable.'
        eig = np.linalg.eig(A)
        x = [i for i in range(0, len(self.displacements))] @ self.f
        eigenvalues = self.zero(eig.eigenvalues)
        eigenvectors = []
        for i in range(0, len(eigenvalues)):
            if eigenvalues[i] == 0:
                eigenvectors.append(eig.eigenvectors[i])
        eigenvectors_rref, _, _ = rref.rref(np.array(eigenvectors))
        for eigenvector in eigenvectors_rref:
            message += '\n'
            for j in range(0, len(eigenvector)):
                component = eigenvector[j]
                if component != 0:
                    displacement_id = int(x @ [[int(k == j)] for k in range(0, len(self.f[0]))])
                    message += '\n+ ' + str(component) + ' * (' + self.displacements[displacement_id].__str__() + ')'
            message += ' = 0'
        raise Exception(message)

    def calculate_element_forces(self):
        self.element_P = []
        for element in self.elements:
            i = element.id
            K = element.get_K()
            P = self.zero(K @ self.T[i] @ self.D)
            self.element_P.append(P)

    def quad(self, S, A, T):
        return np.transpose(S) @ A @ T

    def zero(self, A):
        A[np.isclose(A, 0, atol=10e-6)] = 0
        return A

    def print_results(self):
        pd.set_option('display.max_columns', None)
        print('Nodes')
        displacement_range = range(0, len(self.displacements))
        displacement_data = np.array([[self.D[i][0], self.P[i][0]] for i in displacement_range])
        displacement_indices = [self.displacements[i].__str__() for i in displacement_range]
        df = pd.DataFrame(displacement_data, displacement_indices, ['Displacement', 'Force'])
        print(df)
        print('')
        print('Elements')
        element_range = range(0, len(self.elements))
        element_data = np.array([[self.element_P[i][j][0] for j in range(0, 12)] for i in element_range])
        element_columns = ['Force ' + str(j) for j in range(0, 12)]
        df = pd.DataFrame(element_data, element_range, element_columns)
        print(df)
