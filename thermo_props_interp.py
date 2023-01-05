import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

def curv():

    # x values:
    t_sat = np.array([-20,-18,-16,-14,-12,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]) #oC
    # y values:
    p_sat = np.array([244.83,264.29,284.93,306.78,329.89,354.30,367.01,380.06,393.47,407.23,421.35,435.84,450.70,465.94,481.57,497.59,514.01,530.83,548.06,565.71,583.78,602.28,621.22,640.59,660.42,680.70,701.44,722.65,744.33,766.50,789.15,812.29,835.93,860.08,884.75,909.93]) #kPa

    # Objective functions
    def obj(t_sat,A,B):
        return 1000*np.exp(A - B/(t_sat + 273.15))


    w, _ = curve_fit(obj, t_sat, p_sat)


    return w, p_sat,t_sat


m, p_sat, t_sat = curv()

print(m)

plt.plot(t_sat,p_sat)
plt.show()

#w0, w1, w2, w3, w4, w5 = popt

T = PropsSI('T','P',101325,'Q', 1, 'water')

print(T)