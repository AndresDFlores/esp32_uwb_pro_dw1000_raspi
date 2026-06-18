import time
import os
from dotenv import load_dotenv
from collections import deque
import socket, struct, time, math

from uwb_module import UWB1000UART

load_dotenv()


HOST = os.getenv("HOST")
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


uwb_class = UWB1000UART()


idx=0
try:
    while True:

        #  collect measurement from from uwb tag module
        anchor_address, anchor_distance = uwb_class.read_distance()

        data = struct.pack('f', anchor_distance)  # Pack as float
        sock.sendall(data)


        #  iteration counter
        idx+=1

except KeyboardInterrupt:
    print("Stopped.")
    plt.ioff()
    plt.show()

except Exception as e:
    print(f"Error: {e}")

finally:
    uwb_class.close()
