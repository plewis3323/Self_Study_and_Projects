import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def wavelength_to_rgb(wavelength):
    """Converts a wavelength in nm to an RGB color."""
    gamma = 0.8
    intensity_max = 255
    factor = 0.0
    R = G = B = 0
    
    if (wavelength >= 300) and (wavelength < 440):
        R = -(wavelength - 440) / (440 - 300)
        G = 0.0
        B = 1.0
    elif (wavelength >= 440) and (wavelength < 490):
        R = 0.0
        G = (wavelength - 440) / (490 - 440)
        B = 1.0
    elif (wavelength >= 490) and (wavelength < 510):
        R = 0.0
        G = 1.0
        B = -(wavelength - 510) / (510 - 490)
    elif (wavelength >= 510) and (wavelength < 580):
        R = (wavelength - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif (wavelength >= 580) and (wavelength < 645):
        R = 1.0
        G = -(wavelength - 645) / (645 - 580)
        B = 0.0
    elif (wavelength >= 645) and (wavelength <= 1050):
        R = 1.0
        G = 0.0
        B = 0.0
    
    if (wavelength >= 300) and (wavelength < 420):
        factor = 0.3 + 0.7*(wavelength - 300) / (420 - 300)
    elif (wavelength >= 420) and (wavelength < 645):
        factor = 1.0
    elif (wavelength >= 645) and (wavelength <= 1050):
        factor = 0.3 + 0.7*(1050 - wavelength) / (1050 - 645)
    
    R = round(intensity_max * (R * factor)**gamma)
    G = round(intensity_max * (G * factor)**gamma)
    B = round(intensity_max * (B * factor)**gamma)
    
    return (R / 255, G / 255, B / 255)


def create_Kr1_spectrum(save_pdf=None, save_png=None):
    # Read the text file into a DataFrame
    data = pd.read_table('Kr_1.txt', delimiter='\\s+', names=['Wave_L', 'Intensity'], header=17, skipfooter=1)
    Kr1_lines = data['Wave_L'].values
    intensities = data['Intensity'].values

    # Create a wavelength range from 300 nm to 1050 nm
    wavelength = np.linspace(300, 1050, 5000)
    spectrum = np.zeros_like(wavelength)

    # Plot the spectrum
    plt.figure(figsize=(10, 6))

    plt.style.use('dark_background')  # Set the plot style to dark background

    # Add the helium emission lines to the spectrum
    for line, intensity in zip(Kr1_lines, intensities):
        if intensity >= 1000:  # Only plot if intensity is greater than or equal to 5000
            color = wavelength_to_rgb(line)
            peak = intensity * np.exp(-0.5 * ((wavelength - line) / 0.5)**2)
            plt.plot(wavelength, peak, color=color, linewidth=2)

    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title('Kr_1 Light Spectrum')
    plt.grid(True, color='gray')  # Set the grid color to gray
    plt.show()

 # Save the plot if filenames are provided
    if save_pdf:
        plt.savefig(save_pdf, format='pdf')
    if save_png:
        plt.savefig(save_png, format='png')

# Example usage:
create_Kr1_spectrum(save_pdf='Kr1_spectrum.pdf', save_png='Kr1_spectrum.png')
