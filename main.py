import numpy as np

# import initial data
from data import *

# import temperature and pressure functions
from thermo_props import *

# Function Temp calculates the temperature, given the pressure
T_evap = Temp(P_evap)
T_cond = Temp(P_cond)

# Vector T: divide the temperature in small parts, correspondig to sections of the tube
# the 3/4 factor is arbitrary, to avoid the sections of the tube to become too small
T = np.linspace(T_cond, T_evap,int((T_cond - T_evap)*3/4))

# calculate the pressure for each temperature
P = Press(T)

# thermodynamical properties
v_l, v_v, h_l, h_v, mu_l, mu_v = Props(T,P)

# empty vectors
n = np.size(P)
V = np.zeros((1,n))
h = np.zeros((1,n))
A = np.zeros((1,n))
B = np.zeros((1,n))
C = np.zeros((1,n))
x = np.zeros((1,n))
v = np.zeros((1,n))
mu = np.zeros((1,n))
Vm = np.zeros((1,n))
f = np.zeros((1,n))
delta_L = np.zeros((1,n))
L = np.zeros((1,n))

V[0,0] = v_l[0]*Q
h[0,0] = h_l[0]

def diameter(v_l, v_v, h_l, h_v, h, Q, V, d, Area, m_dot, P):

    for i in range(n):
        if i<(n-1):
            # Coefficients of the quality polynomium
            A[0,i+1] = 0.5*Q**2*(v_v[i+1] - v_l[i+1])**2
            B[0,i+1] = (h_v[i+1] - h_l[i+1])*1000 + v_l[i+1]*(v_v[i+1] - v_l[i+1])*Q**2
            C[0,i+1] = (h_l[i+1] - h[0,i])*1000 + 0.5*Q**2*(v_l[i+1]**2) - 0.5*(V[0,i]**2)
            # Roots
            # Only the first one is used since the second one is negative (no physical meaning)
            x[0,i+1] = np.roots([A[0,i+1],B[0,i+1],C[0,i+1]])[1]

            # Properties in the section
            h = h_l + x*(h_v - h_l)
            v = v_l + x*(v_v - v_l)
            mu = mu_l + x*(mu_v - mu_l)

            # Average velocity and friction factor
            V = v*Q
            Vm[0,i+1] = 0.5*(V[0,i+1] + V[0,i])
            f[0,i+1] = 0.33/(Vm[0,i+1]*d/(v[0,i+1]*mu[0,i+1]*10**-6))**0.25

            # delta_L: length of the section of the tube
            delta_L[0,i+1] = (d*2*v[0,i+1]/(f[0,i+1]*Vm[0,i+1]**2))*((P[i] - P[i+1])*10**5 - m_dot*(V[0,i+1] - V[0,i])/Area)
            if delta_L[0,i+1] < 0:
                print('Select another diameter.') # In case of blocked flow
                break
            else:
                L[0,i+1] = delta_L[0,i+1] + L[0,i] # Add delta_L to the total length of the tube
                L_final = L[0,-1]

    return L_final

# Calling the function
L_final = diameter(v_l, v_v, h_l, h_v, h, Q, V, d, Area, m_dot, P)

if delta_L[0,-1] > 0:
    print('Tube length: %f m' %(L_final))
