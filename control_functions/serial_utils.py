from control_functions import data_management as dm


def send_data(serial, x, y):
    """Sends acommodate data the arduino"""
    x += 10000
    y += 10000
    foo = 'x' + str(x) + str(y)
    serial.write(foo.encode('utf-8'))


def obtain_data(serial, measurments):
    """Returns information from the arduino"""
    line = serial.readline()
    values = line.decode('utf-8')[:-2]
    val_list = values.split(',')

    return dm.store(measurments,val_list)