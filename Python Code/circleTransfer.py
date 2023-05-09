#import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage.morphology as morph

#Parameters
startTemp = 10
diam = 99  # Number of grid points
iterations = 200
alpha = 2 # Thermal diffusivity [m^2 s^-1]

dx = 1
dt = (dx ** 2)/(4 * alpha)
gamma = (alpha * dt) / (dx ** 2)

dT = 100 # Temperature added each time step

# Initialize the temperature array
T = np.empty((iterations, diam+1, diam+1))
T.fill(0)

vapourTemp = 800 #temperature of vapourisation [K]

#Create circle
xx, yy = np.mgrid[:diam+1, :diam+1]
circle = (xx - diam/2) ** 2 + (yy - diam/2) ** 2
T[:,:,:] = (startTemp)*(circle < ((diam/2)**2))

def findSurface(Tk):
    
    #circle is defined as any cell where the temp is greater than 0
    circleMaskK = Tk > 0
    inner = morph.binary_erosion(Tk)
    incidentMaskK = circleMaskK & ~inner
    
    return circleMaskK, incidentMaskK 

circleMask, incidentMask = np.zeros_like(T), np.zeros_like(T, dtype=bool)
#Converting circle mask from boolean to binary to use in calculate(u) to
#prevent contribution from background pixels

circleMask[0], incidentMask[0] = findSurface(T[0])
circleMask[0] = 1*circleMask[0]

# Comment out the line below to turn off inital heat on the circumference
#T[0,incidentMask[0]] = T[0,incidentMask[0]] + 1000

def calculate(T):
    for k in range(0, iterations-1, 1):
        
        # Comment out the lines below to turn off adding heat each interation
        T[k,incidentMask[k]] = T[k,incidentMask[k]] + dT
        
        # Holds exposed pixels at fixed temperature
        #T[k, incidentMask[k]] = 300
        
        for i in range(1, diam, dx): #iterate through y
            for j in range(1, diam, dx): #iterate through x
                if (circleMask[k][i,j] == 1):
                    #Count number of adjacent cells that are part of the circle
                    adjacent = circleMask[k][i+1][j] + circleMask[k][i-1][j] 
                    + circleMask[k][i][j-1] + circleMask[k][i][j+1]
                    T[k + 1, i, j] = gamma * (T[k][i+1][j]*circleMask[k][i+1][j] 
                    + T[k][i-1][j]*circleMask[k][i-1][j] + T[k][i][j+1]*circleMask[k][i][j+1]
                    + T[k][i][j-1]*circleMask[k][i][j-1] - adjacent*T[k][i][j]*circleMask[k][i][j])
                    + T[k][i][j]*circleMask[k][i][j]
      
        # Comment out the 2 lines below to turn off ablation
        vapourised = T[k+1] > vapourTemp
        T[k+1:,vapourised] = 0
        circleMask[k+1], incidentMask[k+1] = findSurface(T[k+1])
        circleMask[k+1] = 1*circleMask[k+1]
    return T

# Do the calculation here
T = calculate(T)

#Plots every time step
for i in range(0,iterations):
    fig = plt.figure(dpi=300)
    #plt.imshow(T[i], cmap='hot', interpolation='nearest',vmin=273+startTemp-15, vmax=347)
    plt.imshow(T[i], cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.show()
