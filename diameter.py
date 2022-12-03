import numpy as np

def diameter(v_l, v_v, h_l, h_v, Q, d, Area, m_dot, P, mu_l, mu_v, n, V, h, A, B, C, x, v, mu, Vm, f, delta_L, L, j):

    V[0,0] = v_l[0]*Q[j]
    h[0,0] = h_l[0]

    for i in range(n):
        if i<(n-1):
            # Coefficients of the quality polynomium
            A[0,i+1] = 0.5*Q[j]**2*(v_v[i+1] - v_l[i+1])**2
            B[0,i+1] = (h_v[i+1] - h_l[i+1])*1000 + v_l[i+1]*(v_v[i+1] - v_l[i+1])*Q[j]**2
            C[0,i+1] = (h_l[i+1] - h[0,i])*1000 + 0.5*Q[j]**2*(v_l[i+1]**2) - 0.5*(V[0,i]**2)
            # Roots
            # Only the first one is used since the second one is negative (no physical meaning)
            x[0,i+1] = np.roots([A[0,i+1],B[0,i+1],C[0,i+1]])[1]

            # Properties in the section
            h = h_l + x*(h_v - h_l)
            v = v_l + x*(v_v - v_l)
            mu = mu_l + x*(mu_v - mu_l)

            # Average velocity and friction factor
            V = v*Q[j]
            Vm[0,i+1] = 0.5*(V[0,i+1] + V[0,i])
            f[0,i+1] = 0.33/(Vm[0,i+1]*d[j]/(v[0,i+1]*mu[0,i+1]*10**-6))**0.25

            # delta_L: length of the section of the tube
            delta_L[0,i+1] = (d[j]*2*v[0,i+1]/(f[0,i+1]*Vm[0,i+1]**2))*((P[i] - P[i+1])*10**5 - m_dot*(V[0,i+1] - V[0,i])/Area[j])
            
            # In case the flow gets the speed of sound (in this case, for greater values of delta_L, the entropy becomes negative: physically impossible)
            if delta_L[0,i+1] < 0:
                L_final = 0
                break
            else:
                L[0,i+1] = delta_L[0,i+1] + L[0,i] # Add delta_L to the total length of the tube
                L_final = L[0,-1]


    return L_final