import numpy as np
from compressor_curve import *

def Eq_temps(UA_L,t_cond,t_l,t_h,Q_H):

    # Function to generate the compressor curves, based on the compressor datasheet
    w, u = compressor_curve()
    y = u + w

    for i in range(15):
        
        # solve the polynomial
        a1 = w[3] #second degree coefficient
        b1 = w[1] + w[4]+UA_L #first degree coef.
        c1 = w[0] + w[2]*t_cond + w[5]*t_cond**2 - UA_L*t_l #constant coef.
    
        t_evap_roots = np.roots([a1,b1,c1])
        # Conditions of physical meaning of the solution
        t_evap = t_evap_roots[(t_evap_roots > -273) & (t_evap_roots < t_l)][0]

        d1 = y[5]
        e1 = y[2] + y[4]*t_evap
        f1 = y[0] + y[1]*t_evap + y[3]*t_evap**2 - Q_H
        
        t_cond_roots = np.roots([d1,e1,f1])
        # Conditions of physical meaning of the solution
        t_cond = t_cond_roots[(t_cond_roots > -273) & (t_cond_roots > t_h)][0]
        
    return t_cond, t_evap


