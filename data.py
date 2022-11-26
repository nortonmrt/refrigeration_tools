import numpy as np

P_evap = 3 #bar
P_cond = 13 #bar

m_dot = 0.00282 #kg/s
d = 0.047 #in


d = d*0.0254 #m
Area = np.pi*(d**2)/4 #m²
Q = m_dot/Area #m³/s

