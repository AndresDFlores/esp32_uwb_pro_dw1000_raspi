import serial
import time


class UWB1000UART:

    @classmethod
    def set_distance(cls, distance):
        cls.distance = distance


    def __init__(self, port='/dev/serial0', baudrate=115200, timeout=1):

        self.serialData = serial.Serial(port, baudrate, timeout=timeout)
        self.set_distance(distance=None)

        time.sleep(2)  # Allow time for the serial connection to initialize


    def read_distance(self):

        data = self.serialData.readline().decode('utf-8').strip()
        if len(data) == 49:

            distance = data[19:23]

            self.set_distance(
                float(distance)
                )


    def close(self):
        self.serialData.close()


if __name__ == '__main__':
    
    uwb_class = UWB1000UART()

    try:
        while True:
            uwb_class.read_distance()
            print(f'DISTANCE: {uwb_class.distance}m')

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        uwb_class.close()