import serial
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import sys
from scipy.signal import butter, sosfiltfilt

# Self made modules
from control_functions import control_application as ctrl_utils
from control_functions.algorithms import STA
from control_functions import serial_utils as se_ut

### functions
sos = butter(5, 0.2, 'lowpass', fs=10, output = 'sos')
    
def filter_data(data, new_values):
    data[:-1] = data[1:]
    data[-1] = new_values
    data = sosfiltfilt(sos,data)
    return data[-1], data

def trayec(i,offset):
    #return 45
    sigmoid_1 = 30*(np.exp(-((i-(2000 + syncornize))**2)/500000))
    sigmoid_2 = 30*(np.exp(-((i-(4500 + syncornize))**2)/500000))
    a =  sigmoid_1 + sigmoid_2 + offset
    return a

reference = []
reference_B = []
pwm = []
sma_temp = []
distance = []

measurments = {
    'temp_amb':[],
    'temp_amb_B':[],
    'PWM':[],
    'PWM_B':[],
    'temp_SMA_A':[],
    'Dtemp_SMA_A':[],
    'temp_SMA_B':[],
    'Dtemp_SMA_B':[],
    'dist_SMA_A':[],
    'delta_distance':[]
}

"""
Parametros iniciales
"""

Tau = 0.01

u_bottom = 0
u_top = 0

dot_delta_temp_A = 0
dot_delta_temp_B = 0

STA_bottom = STA(Tau, l1 = 5, l2 = 3, w1 = 20)
STA_delta_temp_A = STA(Tau, l1 = 5, l2 = 3, w1 = 0)

STA_top = STA(Tau, l1 = 5, l2 = 3, w1 = 20)
STA_delta_temp_B = STA(Tau, l1 = 5, l2 = 3, w1 = 0)

STA_delta_distance = STA(Tau, l1 = 40, l2 = 34, w1 = 0)


#serial_port = input('Puerto Serial: ').upper()
#offset_input = int(input('Offset: '))

serial_port = sys.argv[1].upper()
offset_input = int(sys.argv[2])
syncornize = int(sys.argv[3])

distance_stores = np.ones((20,))*offset_input

# Dummy variable
delta_temp_bottom = []
force_bottom = []
delta_temp_top = []
force_top = []

print('Preparación de variables lista')
tiempo = time.time()


with serial.Serial() as ser:
    # Information regarding the conexión to the serial interface
    ser.baudrate = 115200
    ser.port = serial_port
    ser.timeout = 2
    ser.open()
    time.sleep(5)
    print('Conexión exitosa')
    for i in range(4000):
        time.sleep(Tau)
        if i > 500:
            se_ut.send_data(ser, u_bottom, u_top)
        else:
            se_ut.send_data(ser, 0, 0)

        #se_ut.send_data(ser, u_bottom, 0)
        input_data = se_ut.obtain_data(ser,measurments)
        sma_temp_A, amb_temp, distance_A, sma_temp_B, amb_temp_B = input_data
        
        distance_A,distance_stores = filter_data(distance_stores,distance_A)
        measurments['dist_SMA_A'][-1] = distance_A
        dist_star = trayec(i,offset_input)
        
        reference.append(dist_star)
        delta_dist = dist_star-distance_A

        measurments['delta_distance'].append(delta_dist)

        # STA Disance
        dot_delta_distance = STA_delta_distance.derivative(delta_dist)
        # ST A
        dSMA_A = STA_bottom.derivative(sma_temp_A)  
        measurments['Dtemp_SMA_A'].append(dSMA_A)
        # ST B
        dSMA_B = STA_top.derivative(sma_temp_B)
        measurments['Dtemp_SMA_B'].append(dSMA_B)
        # ST
        u_bottom,v_bottom,delta_temp_A = ctrl_utils.PD_backstepping(
            sma_temp_A, dot_delta_temp_A, delta_dist,dot_delta_distance
            )
        # Este es el PD
        # u_bottom = ctrl_utils.PD(delta_dist, dot_delta_distance)
        
        dot_delta_temp_A = STA_delta_temp_A.derivative(delta_temp_A)

        u_top, v_top, delta_temp_B = ctrl_utils.PD_backstepping(
            sma_temp_B, dot_delta_temp_B, -delta_dist, -dot_delta_distance
            )
        # Este el PD 
        # u_top = ctrl_utils.PD(-delta_dist,-dot_delta_distance)

        dot_delta_temp_B = STA_delta_temp_B.derivative(delta_temp_B)



      
        # delta_temp_bottom.append(delta_temp_A)
        # force_bottom.append(v_bottom)
        # delta_temp_top.append(delta_temp_B)
        # force_top.append(v_top)
        if(sma_temp_A>50 and sma_temp_B >50):
            print("Apagalo Otto!!!!")
            print(i,sma_temp_A,sma_temp_B)
            break
        elif(i%50==0):
            print(i,sma_temp_A,sma_temp_B,distance_A)
        elif(sma_temp_A>65):
            u_bottom = 0
        elif(sma_temp_B>65):
            u_top = 0

        
        
duration = time.time()-tiempo
print(duration)

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3,2)

ax1.plot(measurments['dist_SMA_A'], label='Actuator')
ax1.plot(reference,label='Reference')
ax1.set_ylabel('Distancia (mm)')
ax1.grid(True)
#
ax2.plot(measurments['temp_SMA_A'],label = 'Temperature SMA bottom')
ax2.set_ylabel('Temperature (°C)')
ax2.legend()
ax2.grid(True)
#
ax3.plot(delta_temp_bottom,label = 'Delta temperature bottom ')
ax3.plot(delta_temp_top,label = 'Delta temperature top ')
ax3.set_ylabel('Delta temperature (°C)')
ax3.grid(True)
#
ax4.plot(STA_delta_distance.w2, label = 'Delta distance derivative')
ax4.set_ylabel('Distance derivative')
ax4.legend()
ax4.grid(True)
#
ax5.plot(force_bottom, label = 'Force bottom')
ax5.plot(force_top, label = 'Force top')
ax5.set_ylabel('Force (N)')
ax5.grid(True)
#
ax6.plot(measurments['temp_SMA_B'],label = 'Temperature difference SMA top')
ax6.set_ylabel('Temperature (°C)')
ax6.legend()
ax6.grid(True)
#
fig.suptitle(serial_port)
plt.show()
# Saving the data

csv_file = 'Resultados Control\\'+serial_port+'parallel_PD_10mm.csv'

answer = sys.argv[4]
df = pd.DataFrame(measurments)
# df['force_bottom'] = force_bottom
# df['force_top'] = force_top


if answer.upper()[0] == 'Y':
    print('El documento se guardo como {}'.format(csv_file))
    df.to_csv(csv_file)


# Z is one line
# X are two lines
