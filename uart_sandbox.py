import serial
import time


class UWB1000UART:

    @classmethod
    def set_distance(cls, distance):
        cls.distance = distance


    def __init__(self, port='/dev/serial0', baudrate=115200, timeout=1):

        self.serialData = serial.Serial(port, baudrate, timeout=timeout)
        self.set_distance(distance=None)

        time.sleep(2)  # time for the serial connection to initialize


    def read_distance(self):

        data = self.serialData.readline().decode('utf-8').strip()

        #  remove string characters
        for char in ['', '(', ')']:
            data=data.strip(char)

        #  split remaining string chars at the comma
        data_vals = data.split(',')

        #  convert split string chars into numeric types and put in tuple
        anchor_address = int(data_vals[0].strip())
        anchor_distance = float(data_vals[-1].strip())

        return (anchor_address, anchor_distance)


    def close(self):
        self.serialData.close()



if __name__ == '__main__':

    uwb_class = UWB1000UART()

    try:
        while True:
            uwb_data = uwb_class.read_distance()

            if uwb_data[-1]>=0:
                print(f'ANCHOR {uwb_data[0]//100}: {uwb_data[-1]}m')

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        uwb_class.close()