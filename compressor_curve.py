import numpy as np
from scipy.optimize import curve_fit

def compressor_curve():

    # Compressor chosen: Embraco ESX55C
    # Datasheet: 
    # https://productsapi.embraco.com/datasheet/compressor/ESX55CBC/518100011/?kit_number=5&standard=ASHRAE&test_application=LBP&refrigerant=R-600a&compressor_speed=3600&unit_system=w&measurement_system=metric&language=pt-BR

    # "x" data: condensing and evaporating temperatures 
    t_cond = np.array([35,35,35,35,35,35,45,45,45,45,45,45,55,55,55,55,55]) #oC
    t_evap = np.array([-35,-30,-25,-20,-15,-10,-35,-30,-25,-20,-15,-10,-30,-25,-20,-15,-10]) #oC
    # Concatenating x data
    x_data = np.vstack((t_cond,t_evap))

    # y values (for capacity and consumption curves)
    Q_L = np.array([98,131,171,218,274,338,89,122,161,207,263,327,112,150,196,250,314]) #W
    W_comp = np.array([63,72,82,91,100,109,64,75,86,98,111,123,75,89,103,118,134]) #W

    # Objective functions
    def capacity(x_data, w0, w1, w2, w3, w4, w5):
        return w0 + w1*x_data[1] + w2*x_data[0] + w3*x_data[1]**2 + w4*x_data[1]*x_data[0] + w5*x_data[0]**2

    def consumption(x_data, u0, u1, u2, u3, u4, u5):
        return u0 + u1*x_data[1] + u2*x_data[0] + u3*x_data[1]**2 + u4*x_data[1]*x_data[0] + u5*x_data[0]**2

    w, _ = curve_fit(capacity, x_data, Q_L)
    u, _ = curve_fit(consumption, x_data, W_comp)

    return w, u
