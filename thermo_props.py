import numpy as np
from CoolProp.CoolProp import PropsSI

# Returns the temperature in K
def Temp(P, fluid):
    T = PropsSI('T','P', P*10**5, 'Q', 0, fluid) #K
    return T

# Returns the pressure in bar
def Press(T, fluid):
    P = PropsSI('P','T', T, 'Q', 0, fluid)/(10**5) #bar (unit used only for convention)
    return P

# Thermodynamical properties
def Props(T,P,fluid):
    v_l = 1.0/PropsSI('D','T',T,'Q',0,fluid) #m³/kg
    v_v = 1.0/PropsSI('D','T',T,'Q',1,fluid) #m³/kg
    h_l = PropsSI('H','T',T,'Q',0,fluid) #J/kg
    h_v = PropsSI('H','T',T,'Q',1,fluid) #J/kg
    mu_l = PropsSI('V','T',T,'Q',0,fluid) #Pas
    mu_v = PropsSI('V','T',T,'Q',1,fluid) #Pas

    # In the first iteration the properties must be zero
    v_v[0] = 0
    h_v[0] = 0
    mu_v[0] = 0

    return(v_l, v_v, h_l, h_v, mu_l, mu_v)