from matplotlib import pyplot
import numpy as np


def visualize(elements, analysis, sight):
    element_original_shapes = []
    element_deformed_shapes = []
    for element in elements:
        original_shape = get_original_shape(element)
        deformed_shape = get_deformed_shape(element, analysis)
        element_original_shapes.append(original_shape)
        element_deformed_shapes.append(deformed_shape)
    plot(element_original_shapes, sight, 'black')
    plot(element_deformed_shapes, sight, 'red')
    pyplot.show()


def get_original_shape(element):
    return [np.transpose([element.get_nodes()[j].position]) for j in [0, 1]]


def get_deformed_shape(element, analysis):
    node_0 = element.get_nodes()[0]
    T = element.cosine_matrix
    element_P = analysis.element_P[element.id]
    element_D = analysis.element_D[element.id]
    V_2 = element_P[1]
    V_3 = element_P[2]
    M_2 = element_P[4]
    M_3 = element_P[5]
    d0_0 = element_D[0]
    d1_0 = element_D[1]
    d2_0 = element_D[2]
    d4_0 = element_D[4]
    d5_0 = element_D[5]
    d6_0 = element_D[6]
    shape = []
    n = 10
    magnifier = 5
    for i in range(0, n + 1):
        x = i / n * element.L
        d_i = np.array([
            magnifier * d0_0 + i / n * (element.L + magnifier * (d6_0 - d0_0)),
            magnifier * (d1_0 + d5_0 * x + (-M_3 * x ** 2 / 2 + V_2 * x ** 3 / 6) / element.E / element.I3),
            magnifier * (d2_0 - d4_0 * x + (-M_2 * x ** 2 / 2 + V_3 * x ** 3 / 6) / element.E / element.I2)
        ])
        shape.append(np.transpose(np.array([node_0.position])) + np.transpose(T) @ d_i)
    return shape


def plot(shapes, sight, color):
    for shape in shapes:
        projected_shape = [sight @ point for point in shape]
        pyplot.plot(
            np.array([point[0] for point in projected_shape]),
            np.array([point[1] for point in projected_shape]),
            color=color
        )
