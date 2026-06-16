import numpy as np
import threading
import time
from collections import deque

import matplotlib.pyplot as plt

from uwb_module import UWB1000UART
from plotter import Plotter


# ── shared state ──────────────────────────────────────────
sample_length = 100
dq_idx = deque(maxlen=sample_length)
dq_dist = deque(maxlen=sample_length)

stop_event = threading.Event()  # signals the reader thread to stop
idx = 0


# ── serial reader thread ──────────────────────────────────
def serial_reader(uwb: UWB1000UART):
    global idx
    while not stop_event.is_set():
        try:
            anchor_address, anchor_distance = uwb.read_distance()
            dq_idx.append(idx)
            dq_dist.append(anchor_distance)
            idx += 1
        except Exception as e:
            print(f"[Reader] Error: {e}")


# ── main ──────────────────────────────────────────────────
uwb_class = UWB1000UART()
plotter_class = Plotter(save_figs=False)

# start reader in background thread
reader_thread = threading.Thread(target=serial_reader, args=(uwb_class,), daemon=True)
reader_thread.start()

try:
    while True:
        # wait until we have at least 2 points to plot
        if len(dq_idx) < 2:
            time.sleep(0.01)
            continue

        # snapshot the deques (thread-safe for deque)
        plot_data = list(zip(dq_idx, dq_dist))

        plotter_class.main(plot_data)

except KeyboardInterrupt:
    print("Stopped.")

    stop_event.set()
    plt.ioff()
    plt.show()

except Exception as e:
    print(f"[Main] Error: {e}")

    stop_event.set()

finally:
    stop_event.set()
    reader_thread.join(timeout=2)
    uwb_class.close()