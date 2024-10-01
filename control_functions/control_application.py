import numpy as np
from control_functions.SMA_model import SMA_force

# Control contants
Kp = 50
Kd = 25

Kp_dis = 1.4
Kd_dis = 0.12

Kp_temp = 3.1
Kd_temp = 1.5


# SuperTwisting



def u_conditioning(u):
    """Force the control into a given range"""
    if u > 255:
        u = 255
    elif u < 0:
        u = 0
    
    return int(u)


def PD(delta,d_delta):
    """Applies a PD control"""
    u = delta*Kp + d_delta*Kd
    u = u_conditioning(u)
    return u



def PD_backstepping(SMA_temp, dot_delta_temp, delta_distancia, dot_delta_distancia):
    """Applies a pseudo backstepping control"""
    v = Kp_dis*delta_distancia + Kd_dis*dot_delta_distancia
    # Solo la parte positiva del modelo
    temperature = SMA_force(v,dot_delta_temp) + 10
    delta_temperature = temperature-SMA_temp
    u = Kp_temp*(delta_temperature) + Kd_temp*dot_delta_temp 
    return u_conditioning(u),v,delta_temperature
