import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import ConvexHull
from lownerjohn_ellipsoid import lownerjohn_inner, lownerjohn_outer


# === Description ===
"""
This program will show how to do affine transformation to convex bodies to make them in the John position, which is
when the transformed convex body has ball as their Lowner-John inner ellipsoid
"""

# === John Position ===
# Compute affine map: T(x) = C^-1(x - d)
def apply_john_normalization(x, C, d):
    C_inv = np.linalg.inv(C)
    return C_inv @ (x - d)

# Compute area of polygon given ordered vertices p
def polygon_area(vertices):
    vertices=np.array(vertices)
    x, y = vertices[:, 0], vertices[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

# === Main ===
if __name__ == '__main__':
    #Vertices of a polygon in 2D
    #p = [[0., 0.], [1., 3.], [5.5, 4.5], [7., 4.], [7., 1.], [3., -2.]]   # general convex body
    p = [[-4., 0.], [-3., 3.], [2., 3.], [3., 2.], [4., 0.], [3., -3.], [-2., -3.], [-3., -2.]]   # symmetric convex body
    nVerts = len(p)

    #The hyperplane representation of the same polytope
    A = [[-p[i][1] + p[i - 1][1], p[i][0] - p[i - 1][0]]
         for i in range(len(p))]
    b = [A[i][0] * p[i][0] + A[i][1] * p[i][1] for i in range(len(p))]

    Ci, di = lownerjohn_inner(A, b)

    # Apply to polygon
    norm_p = np.array([apply_john_normalization(pi, Ci, di) for pi in p])
    
    #The hyperplane representation of the normalized polytope
    AN = [[-norm_p[i][1] + norm_p[i - 1][1], norm_p[i][0] - norm_p[i - 1][0]]
         for i in range(len(norm_p))]
    bn = [AN[i][0] * norm_p[i][0] + AN[i][1] * norm_p[i][1] for i in range(len(norm_p))]

    Cin, din = lownerjohn_inner(AN, bn)

    # Area
    area_p=polygon_area(p)
    area_np=polygon_area(norm_p)

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Original
    axes[0].add_patch(patches.Polygon(p, fill=False, color="red", linewidth=2))
    theta = np.linspace(0, 2 * np.pi, 100)
    x_in = Ci[0][0] * np.cos(theta) + Ci[0][1] * np.sin(theta) + di[0]
    y_in = Ci[1][0] * np.cos(theta) + Ci[1][1] * np.sin(theta) + di[1]
    axes[0].plot(x_in, y_in, 'g', label='Original Inner ellipsoid')
    axes[0].set_title("Original")
    axes[0].axis('equal')
    axes[0].grid(True)
    axes[0].text(0.5, -0.1, f"Area = {area_p:.2f}", ha='center', va='top', transform=axes[0].transAxes, fontsize=12)

    # Normalized
    axes[1].add_patch(patches.Polygon(norm_p, fill=False, color="blue", linewidth=2))
    theta_n = np.linspace(0, 2 * np.pi, 100)
    x_in_n = Cin[0][0] * np.cos(theta_n) + Cin[0][1] * np.sin(theta_n) + din[0]
    y_in_n = Cin[1][0] * np.cos(theta_n) + Cin[1][1] * np.sin(theta_n) + din[1]
    axes[1].plot(x_in_n, y_in_n, 'g', label='Normalized Inner ellipsoid')
    axes[1].set_title("John Normalized")
    axes[1].axis('equal')
    axes[1].grid(True)
    axes[1].text(0.5, -0.1, f"Area = {area_np:.2f}", ha='center', va='top', transform=axes[1].transAxes, fontsize=12)

    plt.tight_layout()
    plt.show()