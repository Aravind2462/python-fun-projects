# ########## This code for process the protocol like %1000,2000,3000$    ############################

# from threading import Thread
# import serial
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import collections
# import time
# import pandas as pd

# class SerialPlot:
#     def __init__(self, serial_port='COM3', baud_rate=9600, plot_length=100):
#         self.port = serial_port
#         self.baud = baud_rate
#         self.plot_max_length = plot_length
#         self.data = [collections.deque([0] * plot_length, maxlen=plot_length) for _ in range(3)]
#         self.is_run = True
#         self.is_receiving = False
#         self.thread = None
#         self.serial_connection = None
#         self.previous_time = 0
#         self.csvData = []
#         self.sampling_rate = 0

#         print(f'Trying to connect to {serial_port} at {baud_rate} BAUD.')
#         try:
#             self.serial_connection = serial.Serial(serial_port, baud_rate)
#             print(f'Connected to {serial_port} at {baud_rate} BAUD.')
#         except Exception as e:
#             print(f'Failed to connect with {serial_port} at {baud_rate} BAUD. Error: {e}')

#     def read_serial_start(self):
#         if self.thread is None:
#             self.thread = Thread(target=self.background_thread)
#             self.thread.start()
#             while not self.is_receiving:
#                 time.sleep(0.1)

#     def get_serial_data(self, frame, lines, line_value_texts, line_labels, time_text):
#         # current_time = time.perf_counter()
#         # plot_interval = int((current_time - self.previous_time) * 1000)
#         # self.previous_time = current_time
#         # time_text.set_text(f'Plot Interval = {plot_interval}ms')
#         time_text.set_text(f'Sampling rate = {self.sampling_rate}ms')
#         for i in range(3):
#             lines[i].set_data(range(self.plot_max_length), self.data[i])
#             line_value_texts[i].set_text(f'[{line_labels[i]}] = {self.data[i][-1]}')

#     def background_thread(self):
#         time.sleep(1.0)
#         self.serial_connection.reset_input_buffer()
#         while self.is_run:
#             line = self.serial_connection.readline().decode('ascii').strip()
#             if line.startswith('%') and line.endswith('$'):
#                 line = line[1:-1]  # Remove start and end characters
#                 values = [int(value) for value in line.split(',')]
#                 current_time = time.perf_counter()
#                 self.sampling_rate = int((current_time - self.previous_time) * 1000)
#                 self.previous_time = current_time
#                 if len(values) == 3:
#                     for i in range(3):
#                         self.data[i].append(values[i])
#                     self.is_receiving = True

#     def save_to_excel(self):
#         data_dict = {f'Channel {i+1}': self.data[i] for i in range(3)}
#         df = pd.DataFrame(data_dict)
#         df.to_excel('uart_data.xlsx', index=False)  # Save data to an Excel file
#         print('excel saved...\n')

#     def close(self):
#         self.is_run = False
#         if self.thread:
#             self.thread.join()
#         if self.serial_connection:
#             self.serial_connection.close()
#             print('Disconnected...')


# def main():
#     port_name = '/dev/ttyAMA0'
#     baud_rate = 115200
#     max_plot_length = 10000
#     s = SerialPlot(port_name, baud_rate, max_plot_length)
#     s.read_serial_start()

#     plt_interval = 1
#     xmin = 0
#     xmax = max_plot_length
#     fig = plt.figure()
#     ax = plt.axes(xlim=(xmin, xmax))
#     ax.set_title('UART Data Plot')
#     ax.set_xlabel('Time')
#     ax.set_ylabel('Value')

#     line_labels = ['Channel 1', 'Channel 2', 'Channel 3']
#     line_value_texts = [ax.text(0.50, 0.95 - i * 0.05, '', transform=ax.transAxes) for i in range(3)]
#     lines = [ax.plot([], [], label=label)[0] for label in line_labels]
#     time_text = ax.text(0.50, 0.95 - 3 * 0.05, '', transform=ax.transAxes)

#     anim = FuncAnimation(fig, s.get_serial_data, fargs=(lines, line_value_texts, line_labels, time_text),
#                          interval=plt_interval)

#     plt.legend(loc='upper left')
#     plt.show()
#     s.close()
#     s.save_to_excel()


# if __name__ == '__main__':
#     main()







########## This code for process the protocol like %1000,2000,3000$    ############################
# This code applys the fir filter for channel 1 data and stored in channel 2 data

from threading import Thread
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import collections
import time
import pandas as pd
import numpy as np
import scipy.signal as signal


class SerialPlot:
    def __init__(self, serial_port='COM3', baud_rate=9600, plot_length=100):
        self.port = serial_port
        self.baud = baud_rate
        self.plot_max_length = plot_length
        self.data = [collections.deque([0] * plot_length, maxlen=plot_length) for _ in range(3)]

        self.is_run = True
        self.is_receiving = False
        self.thread = None
        self.serial_connection = None
        self.previous_time = 0
        self.csvData = []
        self.sample_rate = 0
        
        # filter parameters
        self.fir_coeff = []
        self.num_taps = 0

        print(f'Trying to connect to {serial_port} at {baud_rate} BAUD.')
        try:
            self.serial_connection = serial.Serial(serial_port, baud_rate)
            print(f'Connected to {serial_port} at {baud_rate} BAUD.')
        except Exception as e:
            print(f'Failed to connect with {serial_port} at {baud_rate} BAUD. Error: {e}')

    def read_serial_start(self):
        if self.thread is None:
            self.thread = Thread(target=self.background_thread)
            self.thread.start()
            while not self.is_receiving:
                time.sleep(0.1)

    def get_serial_data(self, frame, lines, line_value_texts, line_labels, time_text):
        #current_time = time.perf_counter()
        #plot_interval = int((current_time - self.previous_time) * 1000)
        #self.previous_time = current_time
        #time_text.set_text(f'Plot Interval = {plot_interval}ms')
        time_text.set_text(f'Sample rate = {self.sample_rate}ms')
        for i in range(3):
            lines[i].set_data(range(self.plot_max_length), self.data[i])
            line_value_texts[i].set_text(f'[{line_labels[i]}] = {self.data[i][-1]}')

    def background_thread(self):
        time.sleep(1.0)
        self.serial_connection.reset_input_buffer()
        while self.is_run:
            line = self.serial_connection.readline().decode('ascii').strip()
            if line.startswith('%') and line.endswith('$'):
                line = line[1:-1]  # Remove start and end characters
                values = [int(value) for value in line.split(',')]
                current_time = time.perf_counter()
                self.sample_rate = int((current_time - self.previous_time) * 1000)
                self.previous_time = current_time
                if len(values) == 3:
                    #for i in range(3):
                        #self.data[i].append(values[i])
                    self.data[0].append(values[0])
                    self.data[1].append(self.apply_fir_filter(values[1]))
                    self.data[2].append(values[2])
                    self.is_receiving = True

    def save_to_excel(self):
        data_dict = {f'Channel {i+1}': self.data[i] for i in range(3)}
        df = pd.DataFrame(data_dict)
        df.to_excel('uart_data.xlsx', index=False)  # Save data to an Excel file
        print('excel saved...\n')

    def close(self):
        self.is_run = False
        if self.thread:
            self.thread.join()
        if self.serial_connection:
            self.serial_connection.close()
            print('Disconnected...')
            
    def init_filter_coeff(self, fs, num_taps, cutoff_freq, user_window):
        #FIR Filter Design
        self.num_taps = num_taps
        nyquist_rate = fs / 2
        cutoff_normalized = cutoff_freq / nyquist_rate
        self.fir_coeff = signal.firwin(num_taps, cutoff_normalized, window=user_window)
        
    def apply_fir_filter(self, val):
        if len(self.data[0]) > self.num_taps:
            filtered_signal = signal.lfilter(self.fir_coeff, 1.0, list(self.data[0])[-(self.num_taps):])
            return int(filtered_signal[-1:])
        else:
            return val
        

def main():
    # uart parameters.
    port_name = '/dev/ttyAMA0'
    baud_rate = 115200
    max_plot_length = 10000
    # filter parameters.
    sampling_freq = 100
    filter_tapings = 100
    cutoff_freq = 1
    window = 'blackman'
    """
        boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen, bohman,
        blackmanharris, nuttall, barthann, cosine, exponential, tukey, taylor, lanczos,
        kaiser (needs beta), kaiser_bessel_derived (needs beta), gaussian (needs standard deviation),
        general_cosine (needs weighting coefficients), general_gaussian (needs power, width)
        general_hamming (needs window coefficient), 
        dpss (needs normalized half-bandwidth)
        chebwin (needs attenuation)
    """
    s = SerialPlot(port_name, baud_rate, max_plot_length)
    s.init_filter_coeff(sampling_freq, filter_tapings, cutoff_freq, window)
    s.read_serial_start()

    plt_interval = 1
    xmin = 0
    xmax = max_plot_length
    fig = plt.figure()
    ax = plt.axes(xlim=(xmin, xmax))
    ax.set_title('UART Data Plot')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')

    line_labels = ['Channel 1', 'Channel 2', 'Channel 3']
    line_value_texts = [ax.text(0.50, 0.95 - i * 0.05, '', transform=ax.transAxes) for i in range(3)]
    lines = [ax.plot([], [], label=label)[0] for label in line_labels]
    time_text = ax.text(0.50, 0.95 - 3 * 0.05, '', transform=ax.transAxes)

    anim = FuncAnimation(fig, s.get_serial_data, fargs=(lines, line_value_texts, line_labels, time_text),
                         interval=plt_interval)

    plt.legend(loc='upper left')
    plt.show()
    s.close()
    s.save_to_excel()


if __name__ == '__main__':
    main()
