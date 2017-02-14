import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import random
from scipy.spatial import Voronoi
from noise import pnoise2
import math
from matplotlib.widgets import CheckButtons

# ============
# === MAIN ===
# ============

# Seed random number generators
try:               arg_points = int(sys.argv[1])
except IndexError: arg_points = 256
try:               arg_relax = int(sys.argv[2])
except IndexError: arg_relax = 4
try:               arg_span = int(sys.argv[3])
except IndexError: arg_span = 4
try:               arg_seed = sys.argv[4]
except IndexError: arg_seed = time.clock()

print("points = " + str(arg_points))
print("relax iterations = " + str(arg_relax))
print("span = " + str(arg_span))
print("seed = " + str(arg_seed))
random.seed(arg_seed)

# Generate relaxed voronoi tesselation
vor = Voronoi(np.random.rand(arg_points,2))
for i in range(0, arg_relax):
  # Voronoi relaxation (Lloyd's Algorithm)
  vor = Voronoi([np.mean([vor.vertices[v] for v in vor.regions[r]], axis=0) for r in vor.point_region])

# Assign subset of polygons to be part of island
land = np.zeros(len(vor.points))
for i, p in enumerate(vor.points):
  if (0 <= p[0] <= 1) and (0 <= p[1] <= 1) and -1 not in vor.regions[vor.point_region[i]]:
    arg_span = 4
    x, y = int(p[0]*255), int(p[1]*255)
    c = pnoise2(x*arg_span/256, y*arg_span/256)
    land[i] = c > 0.3*0.3*p.dot(p) 

# ===========================
# === Export as .obj file ===
# ===========================

with open("mesh.obj", "w") as f :
  f.write("# OBJ file\n")
  for v in vor.vertices:
    f.write("v %.4f %.4f %.4f\n" % (v[0], 0, v[1]))
  for p, l in enumerate(land):
    if l == 1:
      point = vor.points[p]
      region = vor.regions[vor.point_region[p]]
      f.write("f")
      for vi in region:
        f.write(" %d" % (vi + 1)) # vertices indexed-by-1 rather than 0
      f.write("\n")  

# ====================
# === PLOT VORONOI ===
# ====================

fig, ax = plt.subplots()

def fill_polygons(vor, land):
  for i, r in enumerate(vor.point_region):
    if land[i] == 1:
      polygon = [vor.vertices[v] for v in vor.regions[r]]
      ax.fill(*zip(*polygon), color="green")

def plot_voronoi(vor, land):
  plt.hold(True)
  
  # Mark the points
  ax.plot(vor.points[:,0], vor.points[:, 1], 'wo', markersize=4, picker=8)
  fig.canvas.mpl_connect('pick_event', onpick)
    
  # Mark the Voronoi vertices.
  ax.plot(vor.vertices[:,0], vor.vertices[:, 1], 'ko', markersize=6)
    
  for vpair in vor.ridge_vertices:
    if vpair[0] >= 0 and vpair[1] >= 0:
      v0 = vor.vertices[vpair[0]]
      v1 = vor.vertices[vpair[1]]
      # Draw a line from v0 to v1.
      ax.plot([v0[0], v1[0]], [v0[1], v1[1]], 'k', linewidth=2)
    
  ax.set_xlim([-0.25, 1.25])
  ax.set_ylim([-0.25, 1.25])
  
  fill_polygons(vor, land)
  
  plt.hold(False)
  plt.show()

def onpick(event):
  ind = event.ind
  land[ind] = 1-land[ind]
  #ax.clear()
  plot_voronoi(vor, land)
  fig.canvas.draw()

plot_voronoi(vor, land)
