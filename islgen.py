import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import random
from scipy.spatial import Voronoi
from noise import pnoise2

# Plot voronoi tesselation
def draw_2d_voronoi(vor, land):
  fig = plt.figure()
  plt.hold(True)

  # Mark the points
  plt.plot(vor.points[:,0], vor.points[:, 1], 'wo', markersize=2)
  
  # Mark the Voronoi vertices.
  plt.plot(vor.vertices[:,0], vor.vertices[:, 1], 'ko', markersize=6)
  
  for vpair in vor.ridge_vertices:
    if vpair[0] >= 0 and vpair[1] >= 0:
      v0 = vor.vertices[vpair[0]]
      v1 = vor.vertices[vpair[1]]
      # Draw a line from v0 to v1.
      plt.plot([v0[0], v1[0]], [v0[1], v1[1]], 'k', linewidth=2)
  
  plt.xlim([-0.25, 1.25])
  plt.ylim([-0.25, 1.25])

  for i, r in enumerate(vor.point_region):
    if land[i] == 1:
      polygon = [vor.vertices[v] for v in vor.regions[r]]
      plt.fill(*zip(*polygon), color="green")
  
  plt.hold(False)
  
  plt.show()

# Export to .obj file
def output_obj(vor, land):
  with open("mesh.obj", "w") as f :
    f.write("# OBJ file\n")
    for v in vor.vertices:
      f.write("v %.4f %.4f %.4f\n" % (v[0], 0, v[1]))
    for v in vor.vertices:
      f.write("vn %.0f %.0f %.0f\n" % (0, 1, 0))
    for p, l in enumerate(land):
      if l == 1:
        f.write("f")
        for i in vor.regions[vor.point_region[p]]:
          f.write(" %d" % (i + 1)) # vertices indexed-by-1 rather than 0
        f.write("\n")  

# Voronoi relaxation (Lloyd's Algorithm)
def relax(vor):
  points = [np.mean([vor.vertices[v] for v in vor.regions[r]], axis=0) for r in vor.point_region]
  return Voronoi(points)

# ============
# === MAIN ===
# ============

# Seed random number generators
try:               arg_seed = sys.argv[1]
except IndexError: arg_seed = time.clock()
try:               arg_points = int(sys.argv[2])
except IndexError: arg_points = 256
try:               arg_relax = int(sys.argv[3])
except IndexError: arg_relax = 4
try:               arg_span = int(sys.argv[4])
except IndexError: arg_span = 4

print("seed = " + str(arg_seed))
print("points = " + str(arg_points))
print("relax iterations = " + str(arg_relax))
print("span = " + str(arg_span))
random.seed(arg_seed)

# Generate relaxed voronoi tesselation
vor = Voronoi(np.random.rand(arg_points,2))
for i in range(0, arg_relax):
  vor = relax(vor)

# Assign subset of polygons to be part of island
land = np.zeros(len(vor.points))
for i, p in enumerate(vor.points):
  if (0 <= p[0] <= 1) and (0 <= p[1] <= 1) and -1 not in vor.regions[vor.point_region[i]]:
    arg_span = 4
    x, y = int(p[0]*255), int(p[1]*255)
    c = pnoise2(x*arg_span/256, y*arg_span/256)
    land[i] = c > 0.0 # 0.3*0.3*p.dot(p)

# Export as .obj file
output_obj(vor, land)

# Matplotlib print
draw_2d_voronoi(vor, land)
