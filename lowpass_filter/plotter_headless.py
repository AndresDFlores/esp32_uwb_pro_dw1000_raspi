import socket
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import scipy.signal as signal

HOST = ""       # Listen on all interfaces
PORT = 5005
MAX_SAMPLES = 100

# --- Socket setup ---

# Create a TCP socket (AF_INET = IPv4, SOCK_STREAM = TCP — reliable, ordered delivery)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the port to be reused immediately if the script restarts
# Without this, you'd get "Address already in use" for ~60s after closing
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


# --- Sci-Kit Learn ---
sos = signal.butter(4, 10, 'low', fs=1000, output='sos')


# --- Plot setup ---
fig, ax = plt.subplots()
line, = ax.plot([], [], linewidth=1, label='Raw Data')
filtered_line, = ax.plot([], [], linewidth=1.5, color='green', label='Filtered Data')

ax.set_ylim(-1, 3)
ax.set_xlim(0, MAX_SAMPLES)
ax.axhline(y=1, color='r', linestyle='--', linewidth=1, label='1m')
ax.grid(True)
ax.legend()

# Holds the active connection from the Pi — starts as None (no client connected yet)
conn = None

def update(frame):
    global conn
    try:
        if conn is None:
            conn, addr = sock.accept()
            conn.setblocking(False)
            print(f"Connected: {addr}")


        # Try to read exactly 4 bytes from the Pi (a 32-bit float is 4 bytes)
        raw = conn.recv(4)
        if raw and len(raw) == 4:
            value = struct.unpack('f', raw)[0]
            data.append(value)
            line.set_data(range(len(data)), data)


            #  required data length to perform filtering
            if len(data)>15:
                filtered_data = signal.sosfiltfilt(sos, data)
                filtered_line.set_data(range(len(filtered_data)), filtered_data)
                plot_title=f'Last Measurement: {data[-1]:.2f}m | Filtered: {filtered_data[-1]:.2f}m'
            else:
                plot_title=f'Last Measurement: {data[-1]:.2f}m'

            ax.set_title(f'UWB DW1000 Data Sampling Test\n{plot_title}')


    except BlockingIOError:
        pass
    except (ConnectionResetError, BrokenPipeError):
        print("Client disconnected, waiting for new connection...")
        conn = None

    return line,


#  animation loop
ani = animation.FuncAnimation(
    fig,                    # The figure window to animate
    update,                 # The function to call on every frame
    interval=50,            # Milliseconds between frames (50ms = 20 frames per second)
    blit=False,             # False = redraw the entire plot each frame (required for this backend)
    cache_frame_data=False  # Don't cache frames — we're reading live data, not replaying
)


plt.tight_layout()  # Automatically adjust subplot spacing so labels/title aren't clippedv
plt.show()  # Open the plot window and start the animation loop — blocks here until window is closed

