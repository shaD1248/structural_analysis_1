from collection import Collection
from element import Element
from material import Material
from node import Node
from section import Section

steel = Material(200, 0.3)
test_data_sets = []
my_section = Section(1, 1, 1, 1)

# Data Set 0 (Single-element truss)

nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([1, 1, 0], [1, 1, 0, 0, 0, 0], 0o66),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o1717),
])
test_data_sets.append({'nodes': nodes, 'elements': elements})

# Data Set 1 (Triangle truss)

nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([1, 0, 0], [0, 0, 0, 0, 0, 0], 0o66),
    Node([0, 1, 0], [1, 0, 0, 0, 0, 0], 0o44),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o1717),
    Element(nodes.get(0), nodes.get(2), my_section, steel, 0, 0o1717),
    Element(nodes.get(1), nodes.get(2), my_section, steel, 0, 0o1717),
])
test_data_sets.append({'nodes': nodes, 'elements': elements})

# Data Set 2 (Tetrahedron truss)

nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([1, 0, 0], [0, 0, 0, 0, 0, 0], 0o66),
    Node([0, 1, 0], [0, 0, 0, 0, 0, 0], 0o44),
    Node([0, 0, 1], [1, 1, 0, 0, 0, 0], 0o00),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o1717),
    Element(nodes.get(0), nodes.get(2), my_section, steel, 0, 0o1717),
    Element(nodes.get(0), nodes.get(3), my_section, steel, 0, 0o1717),
    Element(nodes.get(1), nodes.get(2), my_section, steel, 0, 0o1717),
    Element(nodes.get(1), nodes.get(3), my_section, steel, 0, 0o1717),
    Element(nodes.get(2), nodes.get(3), my_section, steel, 0, 0o1717),
])
test_data_sets.append({'nodes': nodes, 'elements': elements})

# Data Set 3 (Cantilever)

nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([1, 0, 0], [0, 0, -1, 0, 0, 0], 0o00),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o7777),
])
test_data_sets.append({'nodes': nodes, 'elements': elements})

# Data Set 4 (3d Cantilever)

nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([1, 0, 0], [0, 0, 0, 0, 0, 0], 0o00),
    Node([1, 1, 0], [0, 0, 1, 0, 0, 0], 0o00),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o7777),
    Element(nodes.get(1), nodes.get(2), my_section, steel, 0, 0o7777),
])
test_data_sets.append({'nodes': nodes, 'elements': elements})

# Data Set 5 (Simply supported beam with a point force)

nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([5, 0, 0], [0, 0, -6, 0, 0, 0], 0o00),
    Node([10, 0, 0], [0, 0, 0, 0, 0, 0], 0o66),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o7717),
    Element(nodes.get(1), nodes.get(2), my_section, steel, 0, 0o1777),
])
test_data_sets.append({'nodes': nodes, 'elements': elements})
