import serial
import time


serialData = serial.Serial(
    '/dev/serial0',
    115200,
    timeout=1)


while True:
    data = serialData.readline().decode('utf-8')

    if len(data)==49:
        distance = data[19:23]
        print(f'DISTANCE: {distance}m')