# Import the required packages
import numpy as np
from scipy.fft import fft, rfft
from scipy.fft import fftfreq, rfftfreq
from scipy.signal import kaiserord, lfilter, firwin, freqz , convolve
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os


# Building a class Signal for better use.
class Signal:
  """
  Generate sinusoidal signals with specific ampltiudes, frequencies, duration,
  sampling rate, and phase.
  Example:
    signal = Signal(amplitude=10, sampling_rate=2000.0)
    sine = signal.sine()
    cosine = signal.cosine()
  """

  def __init__(self, amplitude=1, frequency=10, duration=1, sampling_rate=100.0, phase=0):
    """
    Initialize the Signal class.
    Args:
        amplitude (float): The amplitude of the signal
        frequency (int): The frequency of the signal Hz
        duration (float): The duration of the signal in second
        sampling_rate (float): The sampling per second of the signal
        phase (float): The phase of the signal in radians
    
    Additional parameters,which are required to generate the signal, are
    calculated and defined to be initialized here too:
        time_step (float): 1.0/sampling_rate
        time_axis (np.array): Generate the time axis from the duration and
                              the time_step of the signal. The time axis is
                              for better representation of the signal.
    """
    self.amplitude = amplitude
    self.frequency = frequency
    self.duration = duration
    self.sampling_rate = sampling_rate
    self.phase = phase
    self.time_step = 1.0/self.sampling_rate
    self.time_axis = np.arange(0, self.duration, self.time_step)
  
  # Generate sine wave
  def sine(self):
    """
    Method of Signal
    Returns:
        np.array of sine wave using the pre-defined variables (amplitude,
        frequency, time_axis, and phase)
    """
    return self.amplitude*np.sin(2*np.pi*self.frequency*self.time_axis+self.phase)
  
  # Generate cosine wave
  def cosine(self):
    """
    Method of Signal
    Returns:
        np.array of cosine wave using the pre-defined variables (amplitude,
        frequency, time_axis, and phase)
    """
    return self.amplitude*np.cos(2*np.pi*self.frequency*self.time_axis+self.phase)

# Building a class Fourier for better use of Fourier Analysis.






class Fourier:
  """
  Apply the Discrete Fourier Transform (DFT) on the signal using the Fast Fourier 
  Transform (FFT) from the scipy package.

  Example:
    fourier = Fourier(signal, sampling_rate=2000.0)
  """

  def __init__(self, signal, sampling_rate):
    """
    Initialize the Fourier class.

    Args:
        signal (np.ndarray): The samples of the signal
        sampling_rate (float): The sampling per second of the signal
    
    Additional parameters,which are required to generate Fourier calculations, are
    calculated and defined to be initialized here too:
        time_step (float): 1.0/sampling_rate
        time_axis (np.ndarray): Generate the time axis from the duration and
                              the time_step of the signal. The time axis is
                              for better representation of the signal.
        duration (float): The duration of the signal in seconds.
        frequencies (numpy.ndarray): The frequency axis to generate the spectrum.
        fourier (numpy.ndarray): The DFT using rfft from the scipy package.
    """
    self.signal = signal
    self.sampling_rate = sampling_rate
    self.time_step = 1.0/self.sampling_rate
    self.duration = len(self.signal)/self.sampling_rate
    self.time_axis = np.arange(0, self.duration, self.time_step)
    self.frequencies = rfftfreq(len(self.signal), d = self.time_step)
    self.fourier = rfft(self.signal)
    
  # Generate the actual amplitudes of the spectrum
  def amplitude(self):
    """
    Method of Fourier

    Returns:
        numpy.ndarray of the actual amplitudes of the sinusoids.
    """
    return 2*np.abs(self.fourier)/len(self.signal)

  # Generate the phase information from the output of rfft  
  def phase(self, degree = False):
    """
    Method of Fourier

    Args:
        degree: To choose the type of phase representation (Radian, Degree).
                By default, it's in radian. 

    Returns:
        numpy.ndarray of the phase information of the Fourier output.
    """
    return np.angle(self.fourier, deg = degree)

  # Plot the spectrum
  def plot_spectrum(self, interactive=False):
    """
    Plot the Spectrum (Frequency Domain) of the signal either using the matplotlib
    package, or plot it interactive using the plotly package.

    Args:
        interactive: To choose if you want the plot interactive (True), or not
        (False). The default is the spectrum non-interactive.

    Retruns:
        A plot of the spectrum.
    """
    # When the argument interactive is set to True:
    if interactive:
      self.trace = go.Line(x=self.frequencies, y=self.amplitude())
      self.data = [self.trace]
      self.layout = go.Layout(title=dict(text='Spectrum',
                                         x=0.5,
                                         xanchor='center',
                                         yanchor='top',
                                         font=dict(size=25, family='Arial, bold')),
                              xaxis=dict(title='Frequency[Hz]'),
                              yaxis=dict(title='Amplitude'))
      self.fig = go.Figure(data=self.data, layout=self.layout)
      return self.fig.show()
    # When the argument interactive is set to False:
    else:
      plt.figure(figsize = (10,6))
      plt.plot(self.frequencies, self.amplitude())
      plt.title('Spectrum')
      plt.ylabel('Amplitude')
      plt.xlabel('Frequency[Hz]')
  
  # Plot the Signal and the Spectrum interactively
  def plot_time_frequency(self, t_ylabel="Amplitude", f_ylabel="Amplitude",
                          t_title="Signal (Time Domain)",
                          f_title="Spectrum (Frequency Domain)"):
    """
    Plot the Signal in Time Domain and Frequency Domain using plotly.

    Args:
        t_ylabel (String): Label of the y-axis in Time-Domain
        f_ylabel (String): Label of the y-axis in Frequency-Domain
        t_title (String): Title of the Time-Domain plot
        f_title (String): Title of the Frequency-Domain plot 

    Returns:
        Two figures: the first is the time-domain, and the second is the
                     frequency-domain.
    """
    # The Signal (Time-Domain)
    self.time_trace = go.Line(x=self.time_axis, y=self.signal)
    self.time_domain = [self.time_trace]
    self.layout = go.Layout(title=dict(text=t_title,
                                       x=0.5,
                                       xanchor='center',
                                       yanchor='top',
                                       font=dict(size=25, family='Arial, bold')),
                            xaxis=dict(title='Time[sec]'),
                            yaxis=dict(title=t_ylabel),
                            width=1000,
                            height=400)
    fig = go.Figure(data=self.time_domain, layout=self.layout)
    fig.show()
    # The Spectrum (Frequency-Domain)
    self.freq_trace = go.Line(x=self.frequencies, y=self.amplitude())
    self.frequency_domain = [self.freq_trace]
    self.layout = go.Layout(title=dict(text=f_title,
                                       x=0.5,
                                       xanchor='center',
                                       yanchor='top',
                                       font=dict(size=25, family='Arial, bold')),
                            xaxis=dict(title='Frequency[Hz]'),
                            yaxis=dict(title=f_ylabel),
                            width=1000,
                            height=400)
    fig = go.Figure(data=self.frequency_domain, layout=self.layout)
    fig.show()



def main():
    if (len(sys.argv) > 1) and (os.path.exists(sys.argv[1])):
        # Load the Excel file into a pandas DataFrame
        excel_dir = sys.argv[1]
        print(f"Reading: {excel_dir}")
        df = pd.read_excel(excel_dir)
        my_sampling_rate = 240
        my_duration = 10
        # Extract raw data from the excel file.
        raw_data = df['RAW']

        # Test Signal
        signal_1hz = Signal(amplitude=5, frequency=1, sampling_rate=my_sampling_rate, duration=my_duration)
        sine_1hz = signal_1hz.sine()
        df['sine_1hz'] = pd.Series(sine_1hz)

        signal_2hz = Signal(amplitude=3, frequency=2, sampling_rate=my_sampling_rate, duration=my_duration)
        sine_2hz = signal_2hz.sine()
        df['sine_2hz'] = pd.Series(sine_2hz)

        signal_20hz = Signal(amplitude=2, frequency=20, sampling_rate=my_sampling_rate, duration=my_duration)
        sine_20hz = signal_20hz.sine()
        df['sine_20hz'] = pd.Series(sine_20hz)

        signal_50hz = Signal(amplitude=3, frequency=50, sampling_rate=my_sampling_rate, duration=my_duration)
        sine_50hz = signal_50hz.sine()
        df['sine_50hz'] = pd.Series(sine_50hz)

        signal_10hz = Signal(amplitude=3, frequency=10, sampling_rate=my_sampling_rate, duration=my_duration)
        sine_10hz = signal_10hz.sine()
        df['sine_10hz'] = pd.Series(sine_10hz)

        signal_5hz = Signal(amplitude=3, frequency=5, sampling_rate=my_sampling_rate, duration=my_duration)
        sine_5hz = signal_5hz.sine()
        df['sine_5hz'] = pd.Series(sine_5hz)


        raw_data = sine_1hz + sine_2hz + sine_20hz + sine_50hz + sine_10hz + sine_5hz
        df['combined signal'] = pd.Series(raw_data)


        # Apply the DFT using the class Fourier
        fourier = Fourier(raw_data, sampling_rate=my_sampling_rate)
        # Plot the spectrum interactively using the class Fourier
        fourier.plot_time_frequency()


        #### got it form online ####

        # # The Nyquist rate of the signal.
        nyq_rate = my_sampling_rate / 2.0

        # # The desired width of the transition from pass to stop,
        # # relative to the Nyquist rate.  We'll design the filter
        # # with a 5 Hz transition width.
        width = 1.0/nyq_rate

        # # The desired attenuation in the stop band, in dB.
        # ripple_db = 10.0

        # # Compute the order and Kaiser parameter for the FIR filter.
        # N, beta = kaiserord(ripple_db, width)

        # # The cutoff frequency of the filter.
        cutoff_hz = 0.01

        # # Use firwin with a Kaiser window to create a lowpass FIR filter.
        # taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

        taps = firwin(50, cutoff_hz/nyq_rate, window='boxcar')


        print("coefficient\n")
        print(taps)
        print("\n")

        # Use lfilter to filter x with the FIR filter.
        filtered_raw_data = lfilter(taps, 1.0, raw_data)

        filtered_fourier = Fourier(filtered_raw_data, sampling_rate=my_sampling_rate)
        filtered_fourier.plot_time_frequency()

        df['filtered_raw_data'] = pd.Series(filtered_raw_data)


        # Save the DataFrame back to the same Excel file, overwriting it
        df.to_excel(f"{excel_dir}", index=True)
        
    else:
       print("pass the file name...")


if __name__ == '__main__':
    main()








