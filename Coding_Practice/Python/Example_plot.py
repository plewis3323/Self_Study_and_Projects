import matplotlib.pyplot as plt
import numpy as np

# Generate some example data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='sin(x)')
plt.title('Example Plot')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.legend()

# Save the plot with a specified filename
filename = 'example_plot.pdf'
plt.savefig(filename)

# Show the plot (optional)
plt.show()

print(f"Plot saved as {filename}")
