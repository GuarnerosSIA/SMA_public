
import numpy as np


def store(dictionary, measures):
    """Accomodates the obtain data into a dictionary"""
    try:
        dictionary['temp_amb'].append(float(measures[0]))
    except:
        dictionary['temp_amb'].append(
            dictionary['temp_amb'][-1]
        )
    try:
        dictionary['temp_amb_B'].append(float(measures[1]))
    except:
        dictionary['temp_amb_B'].append(
            dictionary['temp_amb_B'][-1]
        )
    try:
        dictionary['PWM'].append(float(measures[2]))
    except:
        dictionary['PWM'].append(
            dictionary['PWM'][-1]
        )
    try:
        dictionary['PWM_B'].append(float(measures[3]))
    except:
        dictionary['PWM_B'].append(
            dictionary['PWM_B'][-1]
        )
    try:
        dictionary['temp_SMA_A'].append(float(measures[4]))
    except:
        dictionary['temp_SMA_A'].append(
            dictionary['temp_SMA_A'][-1]
        )
    try:
        dictionary['temp_SMA_B'].append(float(measures[5]))
    except:
        dictionary['temp_SMA_B'].append(
            dictionary['temp_SMA_B'][-1]
        )
    try:
        dictionary['dist_SMA_A'].append(float(measures[6]))
    except:
        dictionary['dist_SMA_A'].append(
            dictionary['dist_SMA_A'][-1]
        )
    return (dictionary['temp_SMA_A'][-1],dictionary['temp_amb'][-1],
             dictionary['dist_SMA_A'][-1], dictionary['temp_SMA_B'][-1],
             dictionary['temp_amb_B'][-1])



