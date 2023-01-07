# Basic library
import numpy as np
# Thermodynamical properties functions
from thermo_props import *
# Diameter calculator
from diameter import *

# Initial data (inform here)
P_evap = 3 #bar
P_cond = 13 #bar
m_dot = 0.00282 #kg/s
d = np.array([0.036, 0.047, 0.055, 0.063]) #in
fluid = 'R290' #please specify in this format

# Unit conversion/extra calculations
d = d*0.0254 #m
Area = np.pi*(d**2)/4 #m²
Q = m_dot/Area #m³/s

# Function Temp calculates the temperature, given the pressure
T_evap = Temp(P_evap,fluid)
T_cond = Temp(P_cond,fluid)

# Vector T: divide the temperature in small parts, correspondig to sections of the tube
T = np.linspace(T_cond, T_evap,int((T_cond - T_evap)))

# calculate the pressure for each temperature
P = Press(T,fluid)

# thermodynamical properties
v_l, v_v, h_l, h_v, mu_l, mu_v = Props(T,P,fluid)

# empty vectors
n = np.size(P)

V, h, A, B, C, x, v, mu, Vm, f, delta_L, L = np.zeros([12,1,n])

# Calling the function

for j in range(np.size(d)):
    L_final,mu = diameter(v_l, v_v, h_l, h_v, Q, d, Area, m_dot, P, mu_l, mu_v, n, V, h, A, B, C, x, v, mu, Vm, f, delta_L, L, j)
    if L_final != 0:
            print('Tube length: %.3f m' %(L_final))
            print('Capillary tube diameter: %.3f in' %(d[j]/0.0254))
            break

if L_final == 0:
    print('Sorry, not found.')
