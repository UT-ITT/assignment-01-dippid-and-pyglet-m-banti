import socket
import time
import numpy as np
import random
import json

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# simulate accelerometer based on a sinus curve (taken from assignment hint)
def sim_accelerometer():
    t = time.time()
    # calculates accelaration parameter based on time * weight
    return {
        "x": float(np.sin(t*1.5)),
        "y": float(np.sin(t*2.5)),
        "z": float(np.sin(t*0.75))
    }

# simulate gyroscope based on a cosinus curve (same Idea as before)
def sim_gyroscope():
    t = time.time()
    # calculates orientation parameter based on time * weight
    return {
        "x": float(np.sin(t*1.5)),
        "y": float(np.sin(t*0.5)),
        "z": float(np.sin(t*1.75))
    }

def sim_button():
    # presses button randomly based on weighted probability 50%
    return random.choices([0, 1], weights=[0.5, 0.5])[0]

while True:
    # message could be print directly in a long string like this,
    # message = '{"accelerometer": {"x": ' + str(x) + ', "y": ' + str(y) + ', "z": ' + str(z) + '}, "button_1": ' + str(button) + '}'
    # but it looks ugly so I decided to use a python dictionary

    # collect data in dictionary
    sensor_data = {
        "accelorometer": sim_accelerometer(),
        "gyroscope": sim_gyroscope(),
        "button_1": sim_button()
    }
    # convert dictionary in JSON-string
    message = json.dumps(sensor_data)

    print(message)

    sock.sendto(message.encode(), (IP, PORT))
    
    time.sleep(1)
