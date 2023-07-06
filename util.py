import numpy as np

def get_rigidity_matrix(r: int, n: int):
    return [np.sign(r & (2 ** i)) for i in range(0, n)]
