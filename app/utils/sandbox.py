import matplotlib.pyplot as plt
import numpy as np

# This function is a placeholder to demonstrate the concept of transforming coordinates
# and does not represent a real transformation for the Schwarzschild spacetime.


def transform_coordinates(r):
    # Example transformation: arctan(r) to bring infinity to a finite value
    return np.arctan(r)


# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(-np.pi/2, np.pi/2)
ax.set_ylim(-np.pi/2, np.pi/2)

# Draw radial null geodesics as straight lines
r = np.linspace(0, np.inf, 1000)
for constant in np.linspace(-3, 3, 15):
    ax.plot(transform_coordinates(r), transform_coordinates(r) + constant, 'b')
    ax.plot(transform_coordinates(r), -
            transform_coordinates(r) + constant, 'b')

# Customize the plot
ax.set_title('Simplified Penrose Diagram')
ax.set_xlabel('Transformed Space')
ax.set_ylabel('Transformed Time')

plt.show()
