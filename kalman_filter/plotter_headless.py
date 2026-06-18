import matplotlib.pyplot as plt
import matplotlib.animation as animation
from main_dsp import receive_and_filter, conn as dsp_conn

MAX_SAMPLES = 100

fig, ax = plt.subplots()
line, = ax.plot([], [], linewidth=1, label='Raw Data')
filtered_line, = ax.plot([], [], linewidth=1.5, color='green', label='Filtered Data')

ax.set_ylim(-1, 3)
ax.set_xlim(0, MAX_SAMPLES)
ax.axhline(y=1, color='r', linestyle='--', linewidth=1, label='1m')
ax.grid(True)
ax.legend()

def update(frame):
    try:
        data, filtered_data = receive_and_filter()

        if data is None:
            return line,filtered_line,

        line.set_data(range(len(data)), data)

        if filtered_data is not None:
            filtered_line.set_data(range(len(filtered_data)), filtered_data)
            plot_title = f'Last Measurement: {data[-1]:.2f}m | Filtered: {filtered_data[-1]:.2f}m'
        else:
            plot_title = f'Last Measurement: {data[-1]:.2f}m'

        ax.set_title(f'UWB DW1000 Data Sampling Test\n{plot_title}')

    except BlockingIOError:
        pass
    except (ConnectionResetError, BrokenPipeError):
        print("Client disconnected, waiting for new connection...")

    return line,filtered_line,

ani = animation.FuncAnimation(
    fig,
    update,
    interval=50,
    blit=False,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()