import numpy as np
import matplotlib.pyplot as plt

# Set up the canvas
size = 500  # pixels
x = np.linspace(-1, 1, size)
y = np.linspace(-1, 1, size)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Define parameters for vibration
k = 20  # wave number controls frequency
m = 6   # angular mode (number of nodes around the circle)
n = 3   # radial mode (number of nodal circles)

# Calculate wave pattern using Bessel function approximation and angular modes
theta = np.arctan2(Y, X)
wave_pattern = np.sin(k * R) * np.cos(m * theta)

# Mask outside the circular plate
mask = R <= 1
wave_pattern[~mask] = 0

# Normalize and display
plt.figure(figsize=(6, 6))
plt.imshow(wave_pattern, cmap='inferno', extent=(-1, 1, -1, 1))
plt.axis('off')
plt.title("Simulated Cymatics Pattern", fontsize=14)
plt.show()
