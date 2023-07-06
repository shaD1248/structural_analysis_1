from collection import Collection
from element import Element
from material import Material
from node import Node
from section import Section

steel = Material(200, 0.3)
test_data_sets = []
my_section = Section(1, 1, 1, 1)

#
# Defining data sets:
#
# 1.    Node([x, y, z], [Fx, Fy, Fz, Mx, My, Mz], r) is a node at point (x, y, z), on which a force (Fx, Fy, Fz) and a
#       moment (Mx, My, My) is exerted. r is the rigidity flag, equal to Σ(r(i) * 2^i), where r(i) is 1 if the node has
#       a support in direction i, and 0 otherwise.
#
# 2.    Element(n0, n1, S, M, theta, r) is an element with ends at nodes n0 and n1. Its cross section is S and it is of
#       material M. theta determines the angle by which the section should be rotated about the axis of the element.
#       r is the rigidity flag, equal to Σ(r(i) * 2^i), where r(i) is 1 if the direction i of the element is restrainted
#       to the corresponding node, and 0 otherwise.
#
# 3.    Directions:
#       a) Nodes:
#           0.  translational x in global coordinate system
#           1.  translational y in global coordinate system
#           2.  translational z in global coordinate system
#           3.  rotational x in global coordinate system
#           4.  rotational y in global coordinate system
#           5.  rotational z in global coordinate system
#       b) Elements:
#           0.  translational x at node 0 in local coordinate system (axial direction; the direction from node 0 to node
#               1)
#           1.  translational y at node 0 in local coordinate system (shear direction; the cross product of local z and
#               local x, rotated about local x by theta)
#           2.  translational z at node 0 in local coordinate system (shear direction; the normalized cross product of
#               local x and global z if they are not parallel, the global z itself otherwise, rotated about local x by
#               theta)
#           3.  rotational x at node 0 in local coordinate system (torsional direction)
#           4.  rotational y at node 0 in local coordinate system (flexural direction)
#           5.  rotational z at node 0 in local coordinate system (flexural direction)
#           6.  translational x at node 1 in local coordinate system
#           ...
#           11. rotational z at node 1 in local coordinate system
#
# 4.    Guide to define rigidity flags: In case you are confused with rotational unstability of nodes or axial/torsional
#       unstability of elements, I suggest to fix all nodes rotationally in all directions you have already fixed them
#       translationally, and to fix all elements axially and torsionally at both ends as well. Of counrse, this is not
#       the only way to define stable boundary conditions.
#       a) Nodes (supports):
#           1. Roller,
#               fixed in global x:          r = 0b001001 = 0o11 = 9
#               fixed in global y:          r = 0b010010 = 0o22 = 18
#               fixed in global z:          r = 0b100100 = 0o44 = 36
#               fixed in global y and z:    r = 0b110110 = 0o66 = 54
#           2. Fixed or pinned (hinged):    r = 0b111111 = 0o77 = 63
#       b) Elements (joints):
#           1. Truss member with independently stable joints:
#                                           r = 0b001111001111 = 0o1717 = 975
#           2. Cantilever with free end or fixed-end beam:
#                                           r = 0b111111111111 = 0o7777 = 4095
#

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
    Node([1, 0, 0], [0, 0, 1, 0, 0, 0], 0o00),
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
