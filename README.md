# Structural Analysis Problem Solver

Structural Analysis Problem Solver allows you to define an analysis problem and solve it. The problem consists of a
collection of Nodes, and a collection of Elements. The goal of the Solver is to find the reaction and element forces
given the external forces and support conditions.

## Notations

### Node

```Node([x, y, z], [Fx, Fy, Fz, Mx, My, Mz], r)```

#### Properties

```x, y, z``` Position of node\
```Fx, Fy, Fz, Mx, My, Mz``` Force exerted on node in global coordinates\
```r``` Rigidity flag of node in global coordinates

### Element

```Element(n0, n1, S, M, theta, r)```

#### Properties

```n0, n1``` Nodes at the ends of element\
```S``` Cross-section of element (assumed prismatic)\
```M``` Material of element (assumed prismatic)\
```theta``` Angle by which the cross-section is rotated\
```r``` Rigidity flag of element in local coordinates

## Analysis parameters

### Force and displacement directions

#### Nodes

The force/displacement space of each node is a 6-dimensional vector field, with the following basis axes:

0. Translational x-axis in global coordinate system
1. Translational y-axis in global coordinate system
2. Translational z-axis in global coordinate system
3. Rotational x-axis in global coordinate system
4. Rotational y-axis in global coordinate system
5. Rotational z-axis in global coordinate system

#### Elements

The force/displacement space of each element is a 12-dimensional vector field, with the following basis axes:

0. Translational x-axis at node 0 in local coordinate system (_axial direction; the direction from node 0 to node 1_)
1. Translational y-axis at node 0 in local coordinate system (_shear direction; the cross product of local z and local
   x, rotated about local x by ```theta```_)
2. Translational z-axis at node 0 in local coordinate system (_shear direction; the normalized cross product of local x
   and global z if they are not parallel, the global z itself otherwise, rotated about local x by ```theta```_)
3. Rotational x-axis at node 0 in local coordinate system (_torsional direction_)
4. Rotational y-axis at node 0 in local coordinate system (_flexural direction_)
5. Rotational z-axis at node 0 in local coordinate system (_flexural direction_)
6. Translational x-axis at node 1 in local coordinate system
7. Translational y-axis at node 1 in local coordinate system
8. Translational z-axis at node 1 in local coordinate system
9. Rotational x-axis at node 1 in local coordinate system
10. Rotational y-axis at node 1 in local coordinate system
11. Rotational z-axis at node 1 in local coordinate system

### Rigidity flags

The rigidity flag, ```r```, of a Node or an Element is defined as $\sum_{i=0}^{n-1} r_i\cdot2^i$, where $r_i$ is $1$ if the
Node is supported or the Element is connected to the joint at the corresponding end in the direction of $i$-th axis, and
$0$ otherwise.

Note that all 6 dimensions of each Node must be constrained by either a support or an element. Likewise, all 12
dimensions of each Element must be constrained by a joint. Other cases of geometric instabilities must be prevented when
you define an analysis problem. Otherwise, the structure will be unstable and fail to support the loads.

_In case you are confused with rotational instability of nodes or axial/torsional instability of usual truss or frame
elements in a specific problem, and you are not sure how to define supports and joints, I would suggest you to begin
with fixing all nodes rotationally in all directions you have already fixed them translationally, and to fix all
elements axially and torsionally at both ends as well. Of course, this is not a general recommendation, but only for
those who are new to defining 3-dimensional truss and frame problems._

#### Examples

* Nodes
    * Free Nodes: ```r = 0b000000 = 0o00 = 0```
    * Nodes with roller and pin supports
        * Fixed in translational and rotational x-axis: ```r = 0b001001 = 0o11 = 9```
        * Fixed in translational and rotational y-axis: ```r = 0b010010 = 0o22 = 18```
        * Fixed in translational and rotational z-axis: ```r = 0b100100 = 0o44 = 36```
        * Fixed in translational and rotational x-axis and rotational y-axis: ```r = 0b001011 = 0o13 = 11```
        * Fixed in translational and rotational x-axis and y-axis: ```r = 0b011011 = 0o33 = 27```
        * Fixed in translational and rotational x-, y-, and z-axis: ```r = 0b111111 = 0o77 = 63```
* Elements
    * Hinged at both ends, with independently stable joints: ```r = 0b001111001111 = 0o1717```
    * Fixed at Node 0 and free at Node 1: ```r = 0b111111111111 = 0o7777```

## Result

The result of the analysis is printed in the console when the Solver runs. It contains the displacement of and forces
exerted on each node, including the reaction forces, in global coordinates, and the member forces in local coordinates.