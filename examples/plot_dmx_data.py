# Plot data from DMX formatted file
import argparse
import numpy as np
import matplotlib.pyplot as plt

import csv
import os

# FigureCanvasAgg is non-interactive, and thus cannot be shown
# This is required to save plots to file


# Load data from file
def load_and_plot_data(filename):
    if os.path.exists(filename) == False:
        print('File does not exist')
        return
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # First 2 lines are 
    #SampleRate=X
    #CenterFrequency=X

    # Extract sample rate and center frequency
    sample_rate = float(data[0][0].split('=')[1])
    center_frequency = float(data[1][0].split('=')[1])

    # Remaining lines are data in complex format: I,Q
    i_data = []
    q_data = []
    for line in data[2:]:
        i_data.append(float(line[0]))
        q_data.append(float(line[1]))

    # Convert to numpy array
    i_data = np.array(i_data)
    q_data = np.array(q_data)
    iq_data = i_data + 1j*q_data

    # Plot log fft of data
    plt.figure()
    fft_data = np.fft.fft(iq_data)
    fft_data = np.fft.fftshift(fft_data)
    fft_data = np.abs(fft_data)
    fft_data = 20*np.log10(fft_data)
    freqs = np.fft.fftfreq(len(iq_data), 1/sample_rate)
    freqs = np.fft.fftshift(freqs)
    plt.plot(freqs, fft_data)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('FFT of IQ Data')
    plt.grid()
    # plt.show()
    plt.savefig('fft.png')

if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Plot data from DMX formatted file')
    parser.add_argument('filename', type=str, help='Name of file to load')
    args = parser.parse_args()

    # Load and plot data
    load_and_plot_data(args.filename)