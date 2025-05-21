import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import ConvexHull
from lownerjohn_ellipsoid import lownerjohn_inner, lownerjohn_outer


# === Description ===
"""
The chapter about john ellipsoid: https://people.math.sc.edu/howard/notes/john.pdf
The Algorithm designed by Mosek which I directly used here: https://docs.mosek.com/11.0/pythonfusion/case-studies-ellipsoids.html
"""

# === STEP 1: interactive input ===
"""
When input a polygon, avoid making an abnormal one, e.g. too sharp at one end or very flat as a whole, which will lead to 
issues in visualization.
"""

plt.ion()  
fig, ax = plt.subplots()
ax.set_title("Live Polygon Construction")
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_xticks(np.arange(-10, 11, 1))
ax.set_yticks(np.arange(-10, 11, 1))
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)

# get the input points
points = []
while True:
    s = input("Enter x y (or press Enter to finish): ").strip()
    if s == "":
        break
    try:
        x, y = map(float, s.split())
        points.append([x, y])
        pts_np = np.array(points)
        ax.clear()
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xticks(np.arange(-10, 11, 1))
        ax.set_yticks(np.arange(-10, 11, 1))
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.plot(pts_np[:, 0], pts_np[:, 1], 'ro-', linewidth=1.5)
        for i, pt in enumerate(pts_np):
            ax.text(pt[0]+0.1, pt[1]+0.1, f'{i+1}')
        plt.draw()
        plt.pause(0.1)
    except Exception as e:
        print("Invalid input. Please enter two numbers like: 1 2")

plt.show(block=False)

plt.ioff()
plt.close()

points = np.array(points)
print(f"Collected {len(points)} points.")

# === STEP 2: get convex hull and order vertices ===
hull = ConvexHull(points)
p = points[hull.vertices][::-1].tolist()
nVerts = len(p)
#print(p)

# === STEP 3: build Ax ≤ b ===
A = [[-p[i][1] + p[i - 1][1], p[i][0] - p[i - 1][0]]
     for i in range(len(p))]
b = [A[i][0] * p[i][0] + A[i][1] * p[i][1] for i in range(len(p))]

# === STEP 4: compute ellipsoids ===
Po, co = lownerjohn_outer(p)
Ci, di = lownerjohn_inner(A, b)

# === STEP 5: Visualization ===
#Polygon
fig = plt.figure()
ax = fig.add_subplot(111)
ax.add_patch(patches.Polygon(p, fill=False, color="red", linewidth=2, label='Polygon'))
#The inner ellipse
theta = np.linspace(0, 2 * np.pi, 100)
x_in = Ci[0][0] * np.cos(theta) + Ci[0][1] * np.sin(theta) + di[0]
y_in = Ci[1][0] * np.cos(theta) + Ci[1][1] * np.sin(theta) + di[1]
ax.plot(x_in, y_in,'g', label='Inner ellipsoid')

xs2_in = np.sqrt(2) * (x_in - di[0]) + di[0]
ys2_in = np.sqrt(2) * (y_in - di[1]) + di[1]
ax.plot(xs2_in, ys2_in, 'c--', label='sqrt(2) * Inner Ellipsoid')

x2_in = 2 * (x_in - di[0]) + di[0]
y2_in = 2 * (y_in - di[1]) + di[1]
ax.plot(x2_in, y2_in, 'c--', label='2 * Inner Ellipsoid')
#The outer ellipse
margin = 10
x_out, y_out = np.meshgrid(
    np.linspace(co[0] - margin, co[0] + margin, 500),
    np.linspace(co[1] - margin, co[1] + margin, 500)
)
ax.contour(x_out, y_out, (Po[0][0] * x_out + Po[0][1] * y_out - co[0])**2 + (Po[1][0] * x_out + Po[1][1] * y_out - co[1])**2, [1])

#x_min = min(di[0], co[0]) - margin
#x_max = max(di[0], co[0]) + margin
#y_min = min(di[1], co[1]) - margin
#y_max = max(di[1], co[1]) + margin

#ax.set_xlim(x_min, x_max)
#ax.set_ylim(y_min, y_max)
ax.relim()
ax.autoscale_view()
ax.set_aspect('equal', adjustable='box')

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.grid(True)
ax.set_title("Polygon with Inner and Outer Ellipsoids")
plt.show()
