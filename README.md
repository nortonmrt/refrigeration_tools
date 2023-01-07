# Refrigeration tools
Simple routines to get valuable information for the project of refrigeration systems. There are two main codes, one for determining an estimated length of a capillary tube (```main```), and the other one to determine the evaporating and condensing temperatures, given the requirements of the system (```main_temperatures```). Both are detailed below.

## Capillary tube (main)
This routine estimate the length of a capillary tube, for a refrigeration system using a specified refrigerant. The input data is:
- Mass flow rate of refrigerant (kg/s);
- Evaporation/condensing pressures (bar);
- Refrigerant fluid.

There are four common capillary diameters already implemented (units in inches). More diameteres can be added by the user, if necessary. The routine evaluate each one of the diameters, getting the smaller one for which the system works properly, as it will be explained further in this text. The temperature and thermodynamical properties are given by CoolProp library. 
``` 
d = np.array([0.036, 0.047, 0.055, 0.063]) #in
``` 
The mathematical model won't be detailed here, but can be consulted in "Refrigeration and Air Conditioning" by Stoecker and Jones (McGraw-Hill, 1985), in the chapter of expansion devices. The main idea is to divide the tube in small sections and evaluate the quality of the biphase mixture at each one, based on the saturated thermodynamical properties and mass flow. With the quality factor it is possible to obtain the properties in that section and calculate the friction factor. The conservation of mass and momentum allows the obtaining of an expression for the length of the section of the tube, as shown below:

![image](https://user-images.githubusercontent.com/108631583/205524173-75661154-12d2-413a-9bc5-48740e9aa6f2.png)

In the equation the subscript (1) denotes a property in the inlet of the section, and (2) at the outlet. 

Finally, adding all the lengths, it is possible to obtain the total length of the tube. It is important to notice that the theory assumes an adiabatic tube.

An important observation is that the length of the section may become negative (case in which the flow becomes supersonic). The reason is, as the cross section of the tube is constant, the velocity of the flow only increases beyond the speed of sound for a negative entropy, which leads to a negative length of the tube. In case that happens, the routine select the next higher tube diameter and restart the process.

## Equilibrium of the condensing and evaporation temperatures (main_temperatures)
In this case, the mass flow rate of refrigerant, the condensing and evaporating temperatures and the thermal conductance of the heat exchangers are obtained. The code is written as the project requirement is the heat rejected by the condenser (heat pump), but in further versions it will be possible to have the heat absorbed bu the evaporator as a requirement. The input data is:
- An estimative of the condensing temperature (in oC);
- The heat rejected by the condenser (in W);
- An estimative of the thermal conductance of the evaporator (in W/K);
- The ambient temperatures (in oC);
- Refrigerant fluid.

Another entry data is the compressor curves for absorbed heat and consumption, generated for a specific compressor (in this case an Embraco ESX55C - datasheet at the end of the text). If necessary, these data can be changed, in case another compressor model is used:
```
t_cond = np.array([35,35,35,35,35,35,45,45,45,45,45,45,55,55,55,55,55]) #oC
t_evap = np.array([-35,-30,-25,-20,-15,-10,-35,-30,-25,-20,-15,-10,-30,-25,-20,-15,-10]) #oC
Q_L = np.array([98,131,171,218,274,338,89,122,161,207,263,327,112,150,196,250,314]) #W
W_comp = np.array([63,72,82,91,100,109,64,75,86,98,111,123,75,89,103,118,134]) #W
```
Based on the data above, the curves were generated using the curve_fit function:
```
# Objective functions
def capacity(x_data, w0, w1, w2, w3, w4, w5):
    return w0 + w1*x_data[1] + w2*x_data[0] + w3*x_data[1]**2 + w4*x_data[1]*x_data[0] + w5*x_data[0]**2

def consumption(x_data, u0, u1, u2, u3, u4, u5):
    return u0 + u1*x_data[1] + u2*x_data[0] + u3*x_data[1]**2 + u4*x_data[1]*x_data[0] + u5*x_data[0]**2

w, _ = curve_fit(capacity, x_data, Q_L)
u, _ = curve_fit(consumption, x_data, W_comp)
```
The function ```compressor_curve``` performs this operation. With all this information, the evaporating and condensing temperature polynomials can be evaluated, and with a recursive procedure it is possible to obtain the equilibrium temperatures. This functionality was implemented in the ```Eq_temps``` function.

Finally, the CoolProp library was used to determine the other properties and hence evaluate the mass flow rate of refrigerant:
```
m_dot = Q_H/(h2 - h3)
```
The information obtained by this second routine can even be evaluated in the previous one (to determine the length of the capillary tube for this system). In future versions both functionalities will be implemented in a single routine.

Obs: the author does not take responsibility for the usage of this routine in real projects.

Datasheet: 
https://productsapi.embraco.com/datasheet/compressor/ESX55CBC/518100011/?kit_number=5&standard=ASHRAE&test_application=LBP&refrigerant=R-600a&compressor_speed=3600&unit_system=w&measurement_system=metric&language=pt-BR
