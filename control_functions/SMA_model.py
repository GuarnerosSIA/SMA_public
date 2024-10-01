#Constants
import math

Am_SMA = -0.6867167875464785 
Bm_SMA = -0.2781578976479685 
Cm_SMA = -41.85316514147054  
Dm_SMA = 1.2133794612378597

Aa_SMA = -0.7322407135089287 
Ba_SMA = -0.3873942710985167
Ca_SMA = -43.927799648917535 
Da_SMA = 1.2751425690110774

def SMA_force(force,derivative):
    """
    This function returns the temperature of an SMA for a desire force
    """
    if derivative >= 0.0:
        if force <= Am_SMA + Dm_SMA:
            # Si es menor que esta fuerza, la temperatura deberia ser 0
            force = (Am_SMA + Dm_SMA)*1.01
            return 0.0 # Temperatura igual a cero
        elif force >= Dm_SMA:
            force = Dm_SMA*0.99
        
        argument = Am_SMA/(force-Dm_SMA)-1
        natural_logarithm = -math.log(argument)/Bm_SMA
        temperature = natural_logarithm - Cm_SMA
    else:
        if force <= Aa_SMA + Da_SMA:
            # Si es menor que esta fuerza, la temperatura deberia ser 0
            force = (Aa_SMA + Da_SMA)*1.01
            return 0.0
        elif force >= Da_SMA:
            force = Da_SMA*0.99
        
        argument = Aa_SMA/(force-Da_SMA)-1
        natural_logarithm = -math.log(argument)/Ba_SMA
        temperature = natural_logarithm - Ca_SMA
    return temperature