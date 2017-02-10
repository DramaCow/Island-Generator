# Island-Generator
Produces a .obj file mesh to aid in semi-procedurally generated islands for games.

## Winding Order
Winding order may be incorrect for some of the polygons. To correct in blender:
```
in edit mode: ctlr + shift + n
```

## Extrude
Add depth in blender as follows:
```
in edit mode: a + a + e
```

## Before Export 
### ngons to triangles
You can select all the faces and go to Mesh> Faces> Triangulate Faces in the 3D View header (or just press Ctrl+T for the same effect) while in Edit Mode.

### Unity Winding Order
Unity uses the reverse winding order of blender. In edit mode, select all faces and press "flip direction" under shading on the left-hand side panel.

## In Unity
Attach a concave (default) "mesh collider" to the default child of the object in order to enable collisions.
Island can be scaled by scaling the parent object.
**Use THICK RAYCASTS (diameter=1) with a* pathfinding to let AI get close to the edge.**
