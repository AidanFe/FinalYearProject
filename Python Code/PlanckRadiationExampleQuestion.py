from math import exp as e
import matplotlib.pyplot as plt
import numpy as np

h=6.626*10**-34
k=1.38*10**-23
T=7000
c=3*10**8

fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Intensity')
ax.set_title('Estimating wavelength')
xpoints = np.array(90)
ypoints = np.array(((2*h*c**2)/90**5)*(1/(e((h*c)/(90*k*T))-1)))

for i in range(100,1100,10):
  l=(i*10**-9)
  B=((2*h*c**2)/l**5)*(1/(e((h*c)/(l*k*T))-1))
  xpoints = np.append(xpoints, l*10**9)
  ypoints = np.append(ypoints, B)
#  print("B",f'{float(f"{B:.2g}"):g}')
#  print("l",f'{float(f"{l:.2g}"):g}')
  
ax.plot(xpoints,ypoints)