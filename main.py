# Basic library
import numpy as np
from CoolProp.CoolProp import PropsSI
# Thermodynamical properties functions
from thermo_props import *
# Diameter calculator
from diameter import *

# Initial data (inform here)
P_evap = 3 #bar
P_cond = 13 #bar
m_dot = 0.00282 #kg/s
d = 0.047 #in

# Unit conversion/extra calculations
d = d*0.0254 #m
Area = np.pi*(d**2)/4 #m²
Q = m_dot/Area #m³/s

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

V, h, A, B, C, x, v, mu, Vm, f, delta_L, L = np.zeros([12,1,n])

V[0,0] = v_l[0]*Q
h[0,0] = h_l[0]

# Calling the function
L_final = diameter(v_l, v_v, h_l, h_v, Q, d, Area, m_dot, P,mu_l,mu_v,n,V,h,A,B,C,x,v,mu,Vm,f,delta_L,L)

