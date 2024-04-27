import pandas as pd
from scipy.signal import firwin, convolve, lfilter
import sys
import os

""" windows:
    boxcar, triang, blackman, hamming, hann, bartlett, flattop, parzen, bohman,
    blackmanharris, nuttall, barthann, cosine, exponential, tukey, taylor, lanczos,
    kaiser (needs beta), kaiser_bessel_derived (needs beta), gaussian (needs standard deviation),
    general_cosine (needs weighting coefficients), general_gaussian (needs power, width)
    general_hamming (needs window coefficient), 
    dpss (needs normalized half-bandwidth)
    chebwin (needs attenuation)
"""
sampling_freq = 100
# you can edit this lookup table as you need.
filter_config_lookup = [
#   tap, cf, window
    [50, 0.1, "blackman"],
    [50, 0.1, "hamming"],
    [50, 0.1, "boxcar"],
    [50, 0.1, "triang"],
    [50, 0.1, "hann"],
    [50, 0.1, "bartlett"],
    [50, 0.1, "flattop"],
    [50, 0.1, "parzen"],
    [50, 0.1, "bohman"]
]

def generate_filter_coeff(fs, num_taps, cutoff_freq, user_window):
    #FIR Filter Design
    nyquist_rate = fs / 2
    cutoff_normalized = cutoff_freq / nyquist_rate
    return firwin(num_taps, cutoff_normalized, window=user_window)

        
def main():
    if (len(sys.argv) > 1) and (os.path.exists(sys.argv[1])):
        # Load the Excel file into a pandas DataFrame
        excel_dir = sys.argv[1]
        print(f"Reading: {excel_dir}")
        df = pd.read_excel(excel_dir)
        # Extract raw data from the first column
        raw_data = df['RAW']

        low_oscilation = 0
        low_oscilation_config = "not initilized"

        for config in filter_config_lookup:
            coeff = generate_filter_coeff(sampling_freq, config[0], config[1], config[2])
            filtered_data = lfilter(coeff, 1.0, raw_data)
            filtered_data = list(map(int, filtered_data))
            print_data = f"taps = {config[0]}, CF = {config[1]}, win = {config[2]}, PP = {min(filtered_data[config[0]:])} - {max(filtered_data[config[0]:])}, OSC = {max(filtered_data[config[0]:]) - min(filtered_data[config[0]:])}"
            print("Generating : " + print_data)
            df[print_data] = filtered_data
            if (low_oscilation_config == "not initilized") or low_oscilation > max(filtered_data[config[0]:]) - min(filtered_data[config[0]:]):
                low_oscilation = max(filtered_data[config[0]:]) - min(filtered_data[config[0]:])
                low_oscilation_config = print_data


        # Save the DataFrame back to the same Excel file, overwriting it
        df.to_excel(f"{excel_dir}", index=False)
        
        print("Result : The minimum oscillation noticed in the below configuration")
        print(f"{low_oscilation_config}")
        print(f"{excel_dir} file updated...")
    else:
        print("Pass the excel file directory")
        print("EXAMPLE : python graph_from_excel example.xlsx")


if __name__ == '__main__':
    main()