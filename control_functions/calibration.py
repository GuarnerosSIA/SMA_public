"""This script converts between the sensor and the actual results"""

# Equation  left 1.21*x - 62.6

M_IZQ = 1.21
B_IZQ = -62.6

# Equation right 1.08*x -33.8
M_DER = 1.08
B_DER = -33.8


def convert_izq(x):
    y = M_IZQ*x + B_IZQ
    return y

def convert_der(x):
    y = M_DER*x + B_DER
    return y
