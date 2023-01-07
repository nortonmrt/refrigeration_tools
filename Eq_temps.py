import numpy as np
from compressor_curve import *

def Eq_temps(UA_L,t_cond,t_l,t_h,Q_H):

    # Function to generate the compressor curves, based on a compressor datasheet
    w, u = compressor_curve()
    y = u + w

    for i in range(15):
        
        # resolver o polinômio (constantes para Q_L)
        a1 = w[3] #coeficiente de segundo grau
        b1 = w[1] + w[4]+UA_L #coeficiente de primeiro grau
        c1 = w[0] + w[2]*t_cond + w[5]*t_cond**2 - UA_L*t_l #coeficiente constante
    
        t_evap_roots = np.roots([a1,b1,c1])
        t_evap = t_evap_roots[(t_evap_roots > -273) & (t_evap_roots < t_l)][0]

        d1 = y[5]
        e1 = y[2] + y[4]*t_evap
        f1 = y[0] + y[1]*t_evap + y[3]*t_evap**2 - Q_H
        
        t_cond_roots = np.roots([d1,e1,f1])
        t_cond = t_cond_roots[(t_cond_roots > -273) & (t_cond_roots > t_h)][0]
        
    return t_cond, t_evap


