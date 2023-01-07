# Basic library
import numpy as np
from CoolProp.CoolProp import PropsSI
# Thermodynamical properties functions
from thermo_props import *
# Equilibrium temperatures calculator
from Eq_temps import *

####
# Project requirements (heat pump in this case)
Q_H = 400 #W
# Temperature of the hot and cold sources. t = [oC] and T = [K]
t_h = 35 #oC
t_l = 0 #oC
fluid = 'R290'

####
# Objective: determine evaporation and condensing temperatures

# Initial guess: condensing temperature and thermal conductance of the evaporator 
t_cond = 40 #oC
#UA_L = 15000 #W/K
UA_L = 13000 #W/K

# Recursive determination of temperatures
t_cond, t_evap = Eq_temps(UA_L, t_cond, t_l, t_h, Q_H)

# Results
print('Condensing temperature: %.3f oC' %(t_cond))
print('Evaporating temperature: %.3f oC' %(t_evap))

# Thermal conductance of the condenser and evaporator heat rate
UA_H = Q_H/(t_cond - t_h)
print('Thermal conductance of the condenser: %.3f W/K' %UA_H)
Q_L = UA_L*(t_l - t_evap)
print('Absorbed heat by the evaporator: %.3f W' %Q_L)

T_evap = t_evap + 273.15
T_cond = t_cond + 273.15

# Pressures
P_evap = Press(T_evap)
P_cond = Press(T_cond)

# mass flow rate of refrigerant:
# there's no equation for properties at the maximum temperature, so we use CoolProp 
h1 = PropsSI("H","T",T_evap,"Q",1,fluid)
s1 = PropsSI("S","T",T_evap,"Q",1,fluid)
s2 = s1
h2 = PropsSI("H","T",T_cond,"S",s2,fluid)
h3 = PropsSI("H","P",P_evap,"Q",0,fluid)

m_dot = Q_H/(h2 - h3)
print('Mass flow rate of refrigerant: %.6f kg/s' %m_dot)