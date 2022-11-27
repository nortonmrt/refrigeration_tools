# Basic library
import numpy as np
# Thermodynamical properties functions
from thermo_props import *
# Diameter calculator
from diameter import *
# Equilibrium temperatures calculator
from Eq_temps import *


####
# Project requirements (heat pump in this case)
Q_H = 57000 #W
# Temperature of the hot and cold sources
t_h = 35 #oC
t_l = 0 #oC
T_H = t_h + 273.15 #K
T_L = t_l + 273.15 #K

####
# Objective: determine evaporation and condensing temperatures

# Initial guess: condensing temperature and thermal conductance of the evaporator 
t_cond = 40 #oC
UA_L = 15000 #W/K

# Recursive determination of temperatures
t_cond, t_evap = Eq_temps(UA_L,t_cond,t_l,t_h,Q_H)

# Results
print('Condensing temperature: %.3f oC' %(t_cond))
print('Evaporating temperature: %.3f oC' %(t_evap))

# Thermal conductance of the condenser
UA_H = Q_H/(t_cond - t_h)
print('Thermal conductance of the condenser: %.3f W/K' %UA_H)

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

# Calling the function
L_final = diameter(v_l, v_v, h_l, h_v, Q, d, Area, m_dot, P,mu_l,mu_v,n,V,h,A,B,C,x,v,mu,Vm,f,delta_L,L)

#print(L_final)

