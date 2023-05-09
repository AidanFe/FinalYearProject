# importing libraries that will be used
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.integrate import quad as integrate
from numpy import exp

#R = N*kb
R = 8.3145 
# file containing data
filename = "si_c.txt"

# load data into array called experimental_data
# text file is space seperated, not CSV
experimental_data = np.loadtxt(filename, delimiter=" ",skiprows=0)

# extract temperature and heat capacity values into separate 1D arrays
T_values = experimental_data[:,0]
C_values = experimental_data[:,1]

# define function that returns the heat capacity in the Einstein
# model, at temperature T, for solid with Einstein temperature T_E

def einstein_C(T,T_E):
    C = 3.0 * R * (T_E/T)**2 * exp(T_E/T) / (exp(T_E/T) - 1.0)**2
    return C

# Use curve_fit to find the value of the Einstein temperature
# that best-fits the experimental data. Initial value is 200 K.
parameters, covariance = curve_fit(einstein_C, T_values, C_values, p0=[200.0])
standard_errors=np.sqrt(np.diag(covariance))
# This is the best-fit value for the Einstein temperature
T_Einstein=parameters[0]
print(F' The Einstein temperature is {T_Einstein:.2f}, standard error {standard_errors[0]:.2f}.')

# define function that returns the heat capacity in the Debye
# model, at temperature T, for solid with Debye temperature T_D
def debye_C(T, T_D):
    #create an array to be returned with the same size as T_values
    C = np.zeros_like(T)
    #for each temperature in T_values, find the heat capacity
    for i, T_i in enumerate(T):
        integrand = lambda x: x**4 * exp(x) / (exp(x) - 1.0)**2
        integral, error = integrate(integrand, 1.0e-6, T_D/T_i)
        C[i] = 9.0 * R * (T_i/T_D)**3 * integral
    return C

# Use curve_fit to find the value of the Debye temperature
# that best-fits the experimental data. Initial value is 200 K.
parameters, covariance = curve_fit(debye_C, T_values, C_values, p0=200)
standard_errors=np.sqrt(np.diag(covariance))
# This is the best-fit value for the Debye temperature
T_Debye=parameters[0]
print(F' The Debye temperature is {T_Debye:.2f}, standard error {standard_errors[0]:.2f}.')

#Plot results to be compared
plt.plot(T_values,C_values,'o',color='#00b3b3',label='Experiment')
plt.plot(T_values,einstein_C(T_values,T_Einstein),linestyle="-",linewidth=2,color='orange',label='Einstein model')
plt.plot(T_values,debye_C(T_values,T_Debye),linestyle="-",linewidth=2,color='brown',label='Debye model')
plt.legend()
plt.xlabel('Temperature / K')
plt.ylabel('Specific Heat Capacity / Jkg$^-$$^1$K$^-$$^1$')
plt.show()
