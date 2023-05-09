import numpy as np
import matplotlib.pyplot as plt

def transfer():
    # Create a figure to display the temperature distribution
    fig, ax = plt.subplots()
    for k in range(0, iterations-1, 1):
        for i in range(1, ny-1, 1):
            for j in range(1, nx-1, 1):
                T[k + 1, i, j] = gamma * (T[k][i+1][j] + T[k][i-1][j] + T[k][i][j+1] + T[k][i][j-1] - 4*T[k][i][j]) + T[k][i][j]
     
    for i in range(0,iterations):
        #plt.imshow(T[i], cmap='hot', interpolation='nearest',vmin=0, vmax=100)
        plt.imshow(T[i], cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.show()

# Define the parameters
nx = 100  # Number of grid points in x direction
ny = 100  # Number of grid points in y direction
iterations = 100

alpha = 2
dx = 1
 
dt = (dx ** 2)/(4 * alpha)
gamma = (alpha * dt) / (dx ** 2)

# Initialize the temperature array
T = np.empty((iterations,ny, nx))
T.fill(0)

# Set the boundary conditions
T[0, 1:-1, 1] = 1000.0  # Left boundary
transfer()

# Initialize the temperature array
T = np.empty((iterations,ny, nx))
T.fill(0)

# Set the boundary conditions
T[0, 1, 1:-1] = 1000.0  # Top boundary
T[0, -2, 1:-1] = 1000.0  # Bottom boundary
T[0, 1:-1, 1] = 1000.0  # Left boundary
T[0, 1:-1, -2] = 1000.0  # Right boundary
transfer()
