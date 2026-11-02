import numpy as np
import matplotlib.pyplot as plt

def main():
    # Define the sampling parameters
    t_min = 0
    t_max = 1
    num_samples = 500
    t = np.linspace(t_min, t_max, num_samples, endpoint=False)
    
    # Input the signal (example: a combination of sine waves)
    freq1 = float(input("Enter the first frequency of the signal (in Hz): "))
    freq2 = float(input("Enter the second frequency of the signal (in Hz): "))
    signal = np.sin(2 * np.pi * freq1 * t) + np.sin(2 * np.pi * freq2 * t)
    
    # Compute the Fourier Transform
    ft_signal = np.fft.fft(signal)
    ft_signal = np.fft.fftshift(ft_signal)  # Shift zero frequency component to the center
    freq = np.fft.fftfreq(num_samples, d=(t_max - t_min) / num_samples)
    freq = np.fft.fftshift(freq)  # Shift zero frequency component to the center

    # Plot the original signal
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(t, signal)
    plt.title('Original Signal')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.grid()
    
    # Plot the Fourier Transform (magnitude)
    plt.subplot(2, 1, 2)
    plt.plot(freq, np.abs(ft_signal))
    plt.title('Fourier Transform')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude')
    plt.grid()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


# Save the plot with a specified filename
filename = 'fourier.pdf'
plt.savefig(filename)

