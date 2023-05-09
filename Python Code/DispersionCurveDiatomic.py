import numpy as np
import matplotlib.pyplot as plt
#import math
import numpy.linalg as lin
import cmath

# Define constants
a = 1 # repeat length a
m = 1 # mass of first atom
M = 2 # mass of second atom
K = 1 # The spring constant
kvalues = np.linspace(-np.pi/a, np.pi/a, 1000) # wave vector range

# Calculate dispersion relation
wvalues1=[]
wvalues2=[]

for k in kvalues:
    #set up the matrix
    x=np.array([[2*K/m, -K/m*(1+cmath.exp(-1j*k*a))],[-K/M*(cmath.exp(1j*k*a)+1), 2*K/M]])
    w2,v=lin.eig(x) #find eigenvalues and eigenvectors
    wvalues1.append((w2[0])**0.5) #the eigenvalues are frequency squared
    wvalues2.append((w2[1])**0.5)
#print('E-value:', w)
#print('E-vector', v)

# Plot dispersion curve
plt.plot(kvalues, wvalues1)
plt.plot(kvalues, wvalues2)
plt.xlabel('Wave Vector / k')
plt.ylabel('Frequency')
#plt.title('Dispersion Curve for a Linear Chain of Atoms with Two Different Masses')
plt.show()
