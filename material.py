class Material:
    def __init__(self, E: float, nu: float):
        self.E = E
        self.nu = nu
        self.G = E / 2 / (1 + nu)
