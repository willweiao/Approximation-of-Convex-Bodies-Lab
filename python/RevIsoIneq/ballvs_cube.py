import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma


# === Introduction ===
"""
Here I want to compare the surface area and the volume of ball and cube, also called the isoperimetric quotient
"""

# === Functions  ===
def ball_surface_area(n):
    return 2 * np.pi**(n/2) / gamma(n/2)
def ball_volume(n):
    return np.pi**(n/2) / gamma(n/2 + 1)
def cube_surface_area(n):
    return 2 * n
def cube_volume(n):
    return 1

# === Computation ===
# Define range of dimensions
dims = np.arange(1, 24)
# Compute surface area, volume, and isoperimetric volume
vol_ball = np.array([ball_volume(n) for n in dims])
surf_ball = np.array([ball_surface_area(n) for n in dims])
vol_cube = np.array([cube_volume(n) for n in dims])
surf_cube = np.array([cube_surface_area(n) for n in dims])
ratio_ball= np.array([ball_surface_area(n)/ball_volume(n)**((n-1)/n) for n in dims])
ratio_cube= np.array([cube_surface_area(n)/cube_volume(n)**((n-1)/n) for n in dims])

# === Visualization ===
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot Volume
axes[0].plot(dims, vol_ball, label="Ball volume", color="red", linewidth=2)
axes[0].plot(dims, vol_cube, label="Cube volume", color="green", linewidth=2)
axes[0].set_xlabel("Dimension n")
axes[0].set_ylabel("Volume")
axes[0].set_title("Volume of unit ball and unit cube vs dimension")
axes[0].grid(True)
axes[0].legend()

# Plot surface areas
axes[1].plot(dims, surf_ball, label="Ball surface area", color="red", linewidth=2)
axes[1].plot(dims, surf_cube, label="Cube surface area", color="green", linewidth=2)
axes[1].set_xlabel("Dimension n")
axes[1].set_ylabel("Surface Area")
axes[1].set_title("Surface area of unit ball and unit cube vs dimension")
axes[1].grid(True)
axes[1].legend()

# Plot isoperimetric quotient comparison
axes[2].plot(dims, ratio_ball, label="Ball Isoperimetric Ratio", color="red", linewidth=2)
axes[2].plot(dims, ratio_cube, label="Cube Isoperimetric Ratio", color="green", linewidth=2)
axes[2].set_xlabel("Dimension n")
axes[2].set_ylabel("Isoperimetric Ratio")
axes[2].set_title("Isoperimetric Ratio of unit ball and unit cube vs dimension")
axes[2].grid(True)
axes[2].legend()

plt.tight_layout()
plt.show()