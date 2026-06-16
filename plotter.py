import numpy as np
import os
from operator import itemgetter

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import scipy.signal as signal


class Plotter:

    def __init__(self, save_figs:bool=False):

        #  save animation_frames (EZGIF)
        self.save_figs=save_figs

        #  initialize plot figure
        self.fig, self.ax = plt.subplots()
        plt.ion()


        # low-pass Butterworth filter
        # creates second-order Sections for numerical stability
        self.sos = signal.butter(4, 10, 'low', fs=1000, output='sos')
        


    def main(self, data:list):

        #  clear axis to redraw figure iteration
        self.ax.cla()

        x=list(map(itemgetter(0), data))
        y=list(map(itemgetter(1), data))
        self.ax.plot(x, y, color='blue')


        #  low-pass filter
        if len(y)>24:

            # apply zero-phase filtering
            filtered_y = signal.sosfiltfilt(self.sos, y)

            self.ax.plot(x, filtered_y, color='green')
            plot_title=f'UWB DW1000 Data Sampling Test\nLast Measurement: {y[-1]}m | Filtered: {filtered_y[-1]:.2f}m'

        else:
            plot_title=f'UWB DW1000 Data Sampling Test\nLast Measurement: {y[-1]}m'

            
        #  plot target line
        self.ax.axhline(y=1, color='r', linestyle='--', linewidth=1, label='1m')


        #  format plot
        # self.ax.set_xlim([-5, 4])
        self.ax.set_ylim([-1, 3])

        self.ax.grid(True)
        self.ax.set_title(plot_title)


        #  redraw figure
        plt.draw()
        plt.pause(.0001)


        #  save figure iteration
        if self.save_figs:
            file_save_path = os.path.join(os.getcwd(), 'figs', f'{iteration}.png')
            plt.savefig(file_save_path, dpi=500)
