import numpy as np
import matplotlib.pyplot as plt


##
# This program is to show the biggest n-polygon (which is also the best approximated n-polygon) in an ellipse is the regular polygon after
# the same affine transformation from circle to ellipse. This statement based on the fact that the regular n-polygon is the biggest polygon
# inside the circle, and still is after the affine transformation
## 

# === Hparas ===
n=7
a,b=2.0,1.0
theta=np.linspace(0, 2*np.pi, n, endpoint=False)

# === Setup ===
circle_polygon = np.stack([np.cos(theta), np.sin(theta)], axis=1)  # regular n-polygon in circle 
circle_polygon = np.vstack([circle_polygon,circle_polygon[0]])
A = np.array([[a, 0],[0, b]])  # sdp matrix of ellipse
ellipse_polygon = circle_polygon @ A.T
ellipse_polygon = np.vstack([ellipse_polygon, ellipse_polygon[0]])

# === Visualization ===
fig, axes = plt.subplots(1, 2, figsize=(10,5))

# circle and polygon
circle = plt.Circle((0,0), 1, edgecolor='blue', facecolor='none', label='Unit Circle')
axes[0].add_patch(circle)
axes[0].plot(*circle_polygon.T, 'o-', color='blue', label=f'{n}-gon in circle')
axes[0].set_title(f"Unit Circle with inscribed {n}-polygon")
axes[0].set_aspect('equal')


# ellipse and polygon
t = np.linspace(0, 2*np.pi, 500)
ellipse_x = a* np.cos(t)
ellipse_y = b* np.sin(t)
axes[1].plot(ellipse_x, ellipse_y, 'b', label= 'Ellipse')
axes[1].plot(*ellipse_polygon.T, 'o-', color= 'red', label=f'{n}-gon in ellipse')
axes[1].set_title(f"Ellipse with inscribed {n}-polygon")
axes[1].set_aspect('equal')

plt.show()

