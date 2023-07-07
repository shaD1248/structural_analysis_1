# Structural Analysis Problem Solver

Structural Analysis Problem Solver allows you to define an analysis problem and solve it. The problem consists of a
collection of Nodes, and a collection of Elements. The goal of the Solver is to find the reaction and Element forces
given the external forces and support conditions.

## Notations

### Node

```Node([x, y, z], [Fx, Fy, Fz, Mx, My, Mz], r)```

#### Properties

```x, y, z``` Position of Node\
```Fx, Fy, Fz, Mx, My, Mz``` External force exerted on Node in global coordinates\
```r``` Rigidity flag of Node in global coordinates

### Element

```Element(n0, n1, S, M, theta, r)```

#### Properties

```n0, n1``` Nodes at the ends of Element\
```S``` Cross-section of Element (assumed prismatic)\
```M``` Material of Element (assumed prismatic)\
```theta``` Angle by which the cross-section is rotated\
```r``` Rigidity flag of Element in local coordinates

### Sections

>(To be added)

## Analysis parameters

### Force and displacement directions

#### Nodes

The force/displacement space of each Node is a 6-dimensional vector field, with the following basis axes:

0. Translational x-axis in global coordinate system
1. Translational y-axis in global coordinate system
2. Translational z-axis in global coordinate system
3. Rotational x-axis in global coordinate system
4. Rotational y-axis in global coordinate system
5. Rotational z-axis in global coordinate system

#### Elements

The force/displacement space of each Element is a 12-dimensional vector field, with the following basis axes:

0. Translational x-axis at Node 0 in local coordinate system (_axial direction; the direction from Node 0 to Node 1_)
1. Translational y-axis at Node 0 in local coordinate system (_shear direction; the cross product of local z and local
   x, rotated about local x by ```theta```_)
2. Translational z-axis at Node 0 in local coordinate system (_shear direction; the normalized cross product of local x
   and global z if they are not parallel, the global z itself otherwise, rotated about local x by ```theta```_)
3. Rotational x-axis at Node 0 in local coordinate system (_torsional direction_)
4. Rotational y-axis at Node 0 in local coordinate system (_flexural direction_)
5. Rotational z-axis at Node 0 in local coordinate system (_flexural direction_)
6. Translational x-axis at Node 1 in local coordinate system
7. Translational y-axis at Node 1 in local coordinate system
8. Translational z-axis at Node 1 in local coordinate system
9. Rotational x-axis at Node 1 in local coordinate system
10. Rotational y-axis at Node 1 in local coordinate system
11. Rotational z-axis at Node 1 in local coordinate system

### Rigidity flags

The rigidity flag, ```r```, of a Node or an Element is defined as $\displaystyle r=\sum_{i=0}^{n-1} r_i\cdot2^i$, where
$r_i$ is $1$ if the Node is supported or the Element is connected to the joint at the corresponding end in the direction
of $i$-th axis, and $0$ otherwise.

Note that all 6 dimensions of each Node must be constrained by either a support or an Element. Likewise, all 12
dimensions of each Element must be constrained by a joint. Other cases of geometric instabilities must be prevented when
you define an analysis problem. Otherwise, the structure will be unstable and fail to support the loads.

_In case you are confused with rotational instability of Nodes or axial/torsional instability of usual truss or frame
Elements in a specific problem, and you are not sure how to define supports and joints, I would suggest you to begin
with fixing all Nodes rotationally in all directions you have already fixed them translationally, and to fix all
Elements axially and torsionally at both ends as well. Of course, this is not a general recommendation, but only for
those who are new to defining 3-dimensional truss and frame problems._

#### Examples

* Nodes
    * Free Nodes: ```r = 0b000000 = 0o00 = 0```
    * Nodes with roller and pin supports
        * Supported in translational and rotational x-axis: ```r = 0b001001 = 0o11 = 9```
        * Supported in translational and rotational y-axis: ```r = 0b010010 = 0o22 = 18```
        * Supported in translational and rotational z-axis: ```r = 0b100100 = 0o44 = 36```
        * Supported in translational and rotational x-axis and rotational y-axis: ```r = 0b001011 = 0o13 = 11```
        * Supported in translational and rotational x-axis and y-axis: ```r = 0b011011 = 0o33 = 27```
        * Supported in translational and rotational x-, y-, and z-axis: ```r = 0b111111 = 0o77 = 63```
* Elements
    * Hinged at both ends, with independently stable joints: ```r = 0b001111001111 = 0o1717```
    * Fixed at Node 0 and free at Node 1: ```r = 0b111111111111 = 0o7777```

## Result

The result of the analysis is printed in the console when the Solver runs. It contains the displacement of and forces
exerted on each Node, including the reaction forces, in global coordinates, and the member forces in local coordinates.

## Solution

### Theory
#### Assumptions
* Static analysis (zero acceleration and relative speed)
* Equilibrium rather than stability (ignoring buckling, vibration, etc.)
* Linear elasticity of material
* Linearized displacements (assuming high stiffness, ignoring higher-order displacements)
* Negligibility of shear deformations
#### Method
The Direct Stiffness Method is implemented in this solution.
### Implementation
#### Solver's problem definition domain
* Node-element problems
* Rectilinear prismatic elements
* No initial strains
* No thermal strains
* No inclined restraints
* No loads between nodes
* No spring supports or joints, except definable as rectilinear elements
* No other constraints between displacements or forces

## Example

### Code

```
from analyzer import Analyzer
from collection import Collection
from element import Element
from material import Material
from node import Node
from section import Section

steel = Material(200, 0.3)
my_section = Section(1, 1, 1, 1)
nodes = Collection([
    Node([0, 0, 0], [0, 0, 0, 0, 0, 0], 0o77),
    Node([1, 0, 0], [0, 0, -1, 0, 0, 0], 0o00),
])
elements = Collection([
    Element(nodes.get(0), nodes.get(1), my_section, steel, 0, 0o7777),
])
analysis = Analyzer(nodes.list, elements.list)
analysis.analyze()
```

### Result

```
Nodes
                          Displacement  Force
displacement 0 of node 0      0.000000    0.0
displacement 1 of node 0      0.000000    0.0
displacement 2 of node 0      0.000000    1.0
displacement 3 of node 0      0.000000    0.0
displacement 4 of node 0      0.000000   -1.0
displacement 5 of node 0      0.000000    0.0
displacement 0 of node 1      0.000000    0.0
displacement 1 of node 1      0.000000    0.0
displacement 2 of node 1     -0.001667   -1.0
displacement 3 of node 1      0.000000    0.0
displacement 4 of node 1      0.002500    0.0
displacement 5 of node 1      0.000000    0.0

Elements
   Force 0  Force 1  Force 2  Force 3  Force 4  Force 5  Force 6  Force 7  \
0      0.0      1.0      0.0      0.0      0.0      1.0      0.0     -1.0   
   Force 8  Force 9  Force 10  Force 11  
0      0.0      0.0       0.0       0.0  
```
