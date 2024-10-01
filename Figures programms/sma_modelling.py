import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.optimize import curve_fit
from scipy import signal
import glob

rcParams.update({'font.family': 'Times New Roman',
                 'font.size':35,
                 'text.usetex':True})

def sigmoidal(x_data,a ,b ,c ,d ):
    y_data = a/(1 + np.exp(-b*(x_data+c))) + d
    return y_data

def force_sensor(x):
    y = -0.008694436023528596*x + 9.58689929041115
    return y-2.1 # Por el ofset de los ejes

x = np.linspace(20,60,50)

thM = 0
thm = -0

df_temp_plus = pd.Series()
df_force_plus = pd.Series()

df_temp_minus = pd.Series()
df_force_minus = pd.Series()

files = glob.glob("Dataset Force Filtered\\*.csv")

for file in files:
    measurements = pd.read_csv(file, index_col=[0])

    dt_data = measurements['Temperature derivative filtered']
    x_data_plus = measurements['SMA temperature filtered'][dt_data>=thM].reset_index(drop=True)
    y_data_plus = measurements['Force sensor filtered'][dt_data>=thM].reset_index(drop=True)
    df_temp_plus = pd.concat([df_temp_plus, x_data_plus], ignore_index=True)
    df_force_plus = pd.concat([df_force_plus, y_data_plus], ignore_index=True)

    x_data_minus = measurements['SMA temperature filtered'][dt_data<thm].reset_index(drop=True)
    y_data_minus = measurements['Force sensor filtered'][dt_data<thm].reset_index(drop=True)
    df_temp_minus = pd.concat([df_temp_minus, x_data_minus], ignore_index=True)
    df_force_minus = pd.concat([df_force_minus, y_data_minus], ignore_index=True)


x_data_minus = df_temp_minus.copy()
y_data_minus = df_force_minus.copy()

y_data_minus = y_data_minus.apply(force_sensor)


x_data_plus = df_temp_plus.copy()
y_data_plus =df_force_plus.copy()

y_data_plus = y_data_plus.apply(force_sensor)
print(y_data_plus.shape[0] + y_data_minus.shape[0])

parameters, covariance = curve_fit(sigmoidal,x_data_plus,y_data_plus,p0=[1,1,-30,200],
                                   bounds=[[-10,-10,-50,-300],[10, 10,50,300]])

a_fit = parameters[0]
b_fit = parameters[1]
c_fit = parameters[2]
d_fit = parameters[3]
print(a_fit,b_fit,c_fit,d_fit)
print(np.diag(covariance))
yfit_plus = sigmoidal(x, a_fit, b_fit, c_fit, d_fit)


parameters, covariance = curve_fit(sigmoidal,x_data_minus,y_data_minus,p0=[-1,-1,-20,200],
                                    bounds=([-10,-10,-50,-300],[10,10,50,300]))

a_fit = parameters[0]
b_fit = parameters[1]
c_fit = parameters[2]
d_fit = parameters[3]

print(a_fit,b_fit,c_fit,d_fit)
print(np.diag(covariance))
yfit_minus = sigmoidal(x,a_fit,b_fit,c_fit,d_fit)

fig, ax = plt.subplots(3,1,figsize=(12,16),dpi=300)

ax[0].scatter(x_data_plus, y_data_plus, label=r'$\dot{T}>=0$',
            s=100,c='tab:red')
ax[0].plot(x, yfit_plus,'ks', label='Model', markersize=15)
ax[0].set_ylim(0.3,1.3)
ax[0].legend(fontsize=40)
ax[0].grid(True)

ax[1].scatter(x_data_minus, y_data_minus, label=r'$\dot{T}<0$',
           s = 100, c = 'steelblue')
ax[1].plot(x, yfit_minus,'ks', label='Model', markersize=15)
ax[1].set_ylim(0.3,1.3)
ax[1].set_ylabel('Force (N)',size=45)
ax[1].legend(loc ='lower right', fontsize=40)
ax[1].grid(True)

ax[2].scatter(x, yfit_plus, marker='^', label=r'$\dot{T}>=0$',
           s = 200, c='tab:red')
ax[2].scatter(x, yfit_minus, marker = 'v', label=r'$\dot{T}<0$', 
            s = 200, c='steelblue')
ax[2].set_ylim(0.3,1.3)
ax[2].legend(loc ='lower right', fontsize=40)
ax[2].grid(True)
ax[2].set_xlabel('SMA temperature (°C)',size=45)

plt.tight_layout()
plt.savefig('.\\figs\\force_model.png', format='png')

# plt.show()