import socket
import struct
from collections import deque


import dsp_algorithms as dsp


HOST = ""
PORT = 5005
MAX_SAMPLES = 100

# --- Socket setup ---

# Create a TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP — reliable, ordered delivery)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the port to be reused immediately if the script restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the HOST and PORT — claims that address for this script
sock.bind((HOST, PORT))

# Start listening for incoming connections; 1 = max number of queued connections
sock.listen(1)

# Non-blocking mode: socket calls return immediately instead of waiting
# This prevents the plot from freezing while waiting for data
sock.setblocking(False)


# --- Data buffer ---
data = deque(maxlen=MAX_SAMPLES)
filtered_data=deque(maxlen=MAX_SAMPLES)

conn = None

def receive_and_filter():
    """Read one sample from socket, append to buffer, return (raw_data, filtered_data or None)."""
    global conn
    try:
        if conn is None:
            conn, addr = sock.accept()
            conn.setblocking(False)
            print(f"Connected: {addr}")

        raw = conn.recv(4)
        if raw and len(raw) == 4:

            value = struct.unpack('f', raw)[0]
            filtered_value = dsp.dsp_kalman(value)

            data.append(value)
            filtered_data.append(filtered_value)

            return data, filtered_data


    except BlockingIOError:
        pass
    except (ConnectionResetError, BrokenPipeError):
        print("Client disconnected, waiting for new connection...")
        conn = None

    return None, None