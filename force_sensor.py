from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def line(x,a,b):
    return a*x + b
force = np.array(
    [
        1.5,2,3.1,3.6,4,1.5,1.7,2.4,4.2,1,1.5,2.1,2.5,3,2.9,
        2.1,2.6,3.5,4,1.1,2.1,0.8,0.4,1.4,1.7,2.1,2.5
]
)
bits = np.array(
    [
    879,848,720,713,708,720,940,804,732,1021,995,874,809,780,769,
    825,784,715,699,960,880,958,990,957,919,886,836
]
)
volts = bits*5/1023
(a,b), pcov = curve_fit(line,bits,force)
volts_fit = np.linspace(500,1000,1000)
y_fit = volts_fit*a + b
print(a,b)


plt.scatter(bits,force)
plt.plot(volts_fit, y_fit)
plt.show()